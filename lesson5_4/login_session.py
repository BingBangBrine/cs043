import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies

connection = sqlite3.connect('users.db')
cursor = connection.cursor()
# connection.execute('CREATE TABLE users (username, password)')


def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    un = params['username'][0] if 'username' in params else None
    pw = params['password'][0] if 'password' in params else None

    if path == '/register' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ?', [un]).fetchall()
        if user:
            start_response('200 OK', headers)
            return ['Sorry, username {} is taken'.format(un).encode()]
        else:
            connection.execute('INSERT INTO users VALUES (?, ?)', [un, pw])
            connection.commit()
            return ['Username {} and password registered'.format(un).encode()]
            # INSERT CODE HERE. Use SQL commands to insert the new username and password
            # into the table that was created.

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            return ['User {} successfully logged in. <a href="/account">Account</a>'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password'.encode()]

    elif path == '/logout':
        headers.append(('Set-Cookie', 'session=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'))
        start_response('200 OK', headers)
        return ['Logged out. <a href="/">Login</a>'.encode()]

    elif path == '/account':
        start_response('200 OK', headers)

        if 'HTTP_COOKIE' not in environ:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if 'session' not in cookies:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        [un, pw] = cookies['session'].value.split(':')
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            return ['Logged in: {}. <a href="/logout">Logout</a>'.format(un).encode()]
        else:
            return ['Not logged in. <a href="/">Login</a>'.encode()]

    elif path == '/':
        users = cursor.execute('SELECT * FROM users').fetchall()
        page = '''<!DOCTYPE html>
        <html>
        <head><title>Login / Register</title></head>
        <body>
        <h1>Login and Register</h1>
        <form action="/login">
            Username <input type="text" name="username" value="Enter username"><br>
            Password <input type="password" name="password"><br>
            <input type="submit" name="loginbutton" value="Login">
        </form>
        <form action="/register">
            Username <input type="text" name="username" value="Enter username"><br>
            Password <input type="password" name="password"><br>
            <input type="submit" name="registerbutton" value="Register">
        </form>
        <hr>
        <p>PATH_INFO: {}</p>
        <p>QUERY_STRING: {}</p>
        <p>users: {}</p>
        </body></html>'''.format(environ['PATH_INFO'], environ['QUERY_STRING'], users)

        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

        return [page.encode()]

    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()
