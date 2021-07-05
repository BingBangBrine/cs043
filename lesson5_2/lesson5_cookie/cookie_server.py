# import wsgiref.simple_server
# import http.cookies
#
#
# def application(environ, start_response):
#     headers = [('Content-Type', 'text/plain; charset=utf-8')]
#
#     # Set cookies here . . .
#     cookies = http.cookies.SimpleCookie()
#     cookies.load('session=Car; weight=2000; tire=5')
#
#     # Cookie parser goes here . . .
#     message = ''
#     if 'session' in cookies:
#         message = message + 'Session: ' + cookies['session'].value
#
#     if 'weight' in cookies:
#         message = message + '\nWeight: ' + cookies['weight'].value
#
#     if 'tire' in cookies:
#         message = message + '\nTire: ' + cookies['tire'].value
#
#     # for key in cookies:
#     #     print(key + '=' + cookies[key].value)
#     start_response('200 OK', headers)
#     return [message.encode(), '\nDone'.encode()]
#
#
# httpd = wsgiref.simple_server.make_server('', 8000, application)
#
# print("Serving on port 8000...")
#
# httpd.serve_forever()


# import wsgiref.simple_server
# import http.cookies
#
#
# def application(environ, start_response):
#     headers = [('Content-Type', 'text/plain; charset=utf-8'),
#                ('Set-Cookie', 'name=Jason'),
#                ('Set-Cookie', 'favoriteNumber=4'),
#                ('Set-Cookie', 'favoriteColor=red')]
#     start_response('200 OK', headers)
#     if 'HTTP_COOKIE' in environ:
#         cookies = http.cookies.SimpleCookie()
#         cookies.load(environ['HTTP_COOKIE'])
#         res = ""
#         for key in cookies:
#             res += (key + ": " + cookies[key].value + "\n")
#         return [res.encode()]
#     else:
#         start_response('404 Not Found', headers)
#         return ['Status 404: Resource not found'.encode()]
#
#
# httpd = wsgiref.simple_server.make_server('', 8000, application)
#
# print("Serving on port 8000...")
#
# httpd.serve_forever()


import wsgiref.simple_server
import http.cookies


def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8'),
               ('Set-Cookie', 'session=Car'),
               ('Set-Cookie', 'weight=2000'),
               ('Set-Cookie', 'tire=5')]

    # Set cookies here . . .
    if 'HTTP_COOKIE' in environ:
        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        # Cookie parser goes here . . .
        message = ''
        if 'session' in cookies:
            message = message + 'Session: ' + cookies['session'].value

        if 'weight' in cookies:
            message = message + '\nWeight: ' + cookies['weight'].value

        if 'tire' in cookies:
            message = message + '\nTire: ' + cookies['tire'].value

        # for key in cookies:
        #     print(key + '=' + cookies[key].value)
        start_response('200 OK', headers)
        return [message.encode(), '\nDone'.encode()]
    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)

print("Serving on port 8000...")

httpd.serve_forever()
