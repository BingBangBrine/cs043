import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies

connection = sqlite3.connect('users.db')
cursor = connection.cursor()


# connection.execute('CREATE TABLE users (un, pw)')


def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    un = params['username'][0] if 'username' in params else None
    pw = params['password'][0] if 'password' in params else None

    if path == '/register' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE un = ?', [un]).fetchall()
        # ## YOUR CODE HERE TO CHECK IF USERNAME IS TAKEN ###

        if user:
            start_response('200 OK', headers)
            return ['Sorry, username {} is taken'.format(un).encode()]
        else:
            connection.execute('INSERT INTO users VALUES (?, ?)', [un, pw])
            connection.commit()
            # ## YOUR CODE HERE TO INSERT A NEW USERNAME AND PASSWORD ###
            # ## AND COMMIT THE INSERT ###
            start_response('200 OK', headers)
            return ['Username {} was successfully registered'.format(un).encode()]

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE un = ? AND pw = ?', [un, pw]).fetchall()
        # CHECK USERNAME AND PASSWORD
        # save cookie when successful login
        if user:
            headers.append(
                ('Set-Cookie', 'session={}:{}; expires=24 Dec 2150 00:15:49 PST'.format(un, pw))
            )
            start_response('200 OK', headers)
            return ['User {} successfully logged in'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password'.encode()]

    elif path == '/logout':
        headers.append(
            ('Set-Cookie', 'session={}; expires=24 Dec 1919 00:15:49 PST')
        )
        start_response('200 OK', headers)
        return ['You were successfully logged out'.encode()]

    elif path == '/account':
        session = False
        if 'HTTP_COOKIE' in environ:
            cookies = http.cookies.SimpleCookie()
            cookies.load(environ['HTTP_COOKIE'])
            if 'session' in cookies:
                session = True
        start_response('200 OK', headers)
        if session:
            return ['You are logged in'.encode()]
        else:
            return ['You are not logged in'.encode()]

    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()
