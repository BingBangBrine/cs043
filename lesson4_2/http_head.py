def http_head(host, page):
    import socket
    sock = socket.create_connection((host, 80))
    #sock.sendall("HEAD /CScourses/03b1_minimal.html HTTP/1.1\r\nHost: indstudy1.org\r\n\r\n".encode())
    sock.sendall(('HEAD ' + page + ' HTTP/1.1\r\nHost: ' + host + '\r\n\r\n').encode())
    print(sock.recv(1000).decode())
    sock.close()

#http_head('50.87.178.13', '/CScourses/03b1_minimal.html')
#http_head('indstudy1.org', '/CScourses/03b1_minimal.html')
#http_head('www.google.com', '/')
http_head("localhost:8000", '')