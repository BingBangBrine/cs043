import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies
import random

connection = sqlite3.connect('users.db')
stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
cursor = connection.cursor()
result = cursor.execute(stmt)
r = result.fetchall()
if not r:
    exp = 'CREATE TABLE users (username,password)'
    connection.execute(exp)


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
            # [INSERT CODE HERE. Use SQL commands to insert the new username and password into the table that has been created. Print a message saying the username was created successfully]

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

        # This is where the game begins. This section of is code only executed if the login form works, and if the user is successfully logged in
        if user:
            correct = 0
            wrong = 0
            cookies = http.cookies.SimpleCookie()
            if 'HTTP_COOKIE' in environ:
                cookies.load(environ['HTTP_COOKIE'])
                if 'score' in cookies:
                    score = cookies['score'].value.split(':')
                    correct = int(score[0])
                    wrong = int(score[1])

            page = '<!DOCTYPE html><html><head><title>Multiply with Score</title></head><body>'
            if 'factor1' in params and 'factor2' in params and 'answer' in params:
                f1 = int(params['factor1'][0])
                f2 = int(params['factor2'][0])
                answer = int(params['answer'][0])
                if f1 * f2 == answer:
                    correct += 1
                    page = page + '<p style="background-color: lightgreen">Correct, {} x {} = {}</p>'.format(f1, f2, answer)
                else:
                    wrong += 1
                    page = page + '<p style="background-color: crimson">Wrong, {} x {} does not = {}</p>'.format(f1, f2, answer)
                    # todo validate the actual answer
                    # [INSERT CODE HERE. If the answer is right, show the “correct” message.
                    # If it’s wrong, show the “wrong” message.]

            elif 'reset' in params:
                correct = 0
                wrong = 0

            headers.append(('Set-Cookie', 'score={}:{}; expires=Thu, 01 Jan 19700 00:00:00 GMT'.format(correct, wrong)))

            f1 = random.randrange(10) + 1
            f2 = random.randrange(10) + 1

            page = page + '<h1>What is {} x {}</h1>'.format(f1, f2)

            # [INSERT CODE HERE. Create a list that stores f1*f2 (the right answer) and 3 other random answers]
            answers = [f1 * f2]
            for x in range(3):
                answers.append(random.randrange(100))
            random.shuffle(answers)

            hyperlink = '''<a href="/account?username={}&amp;password={}&amp;factor1={}&amp;factor2={}&amp;answer={}">{}: {}</a><br>'''
            page += '''<h2>
            {}
            {}
            {}
            {}
            </h2>
            '''.format(
                hyperlink.format(un, pw, f1, f2, answers[0], 'A', answers[0]),
                hyperlink.format(un, pw, f1, f2, answers[1], 'B', answers[1]),
                hyperlink.format(un, pw, f1, f2, answers[2], 'C', answers[2]),
                hyperlink.format(un, pw, f1, f2, answers[3], 'D', answers[3]))
            # [INSERT CODE HERE. Create the 4 answer hyperlinks here using string formatting.]

            page += '''<h2>Score</h2>
            Correct: {}<br>
            Wrong: {}<br>
            <a href="/account?reset=true">Reset</a>
            </body></html>'''.format(correct, wrong)

            return [page.encode()]
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
