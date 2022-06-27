from socket import *
import threading
import os
import time

serverPort = 80
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
client_count = 0


def threaded_client(connection):
    sentence = connection.recv(1024)
    decoded_string = sentence.decode('utf-8')
    fields = decoded_string.split('\r\n')
    print(fields)
    method, url, version, serverName, serverPort = fields[0].split(' ')
    if method == 'GET':
        if url is not None:
            url = url.strip('/')
            with open(url) as f:
                fread = f.read()
                print(fread)
            # file = open(url, 'r')
            # fread = file.read()
            f.close()
            ok_response = "HTTP/1.0 200 OK\r\n" + "\r\n" + fread
            print(ok_response)
            connection.sendall(str.encode(ok_response))
        else:
            error_response = "HTTP/1.0 404 Not Found\r\n"
            connection.sendall(str.encode(error_response))

    elif method == 'POST':
        file = open('post.txt', 'w')
        file.write(fields[-1])
        file.close()
        ok_response = "HTTP/1.0 200 OK\r\n" + "\r\n"
        connection.sendall(str.encode(ok_response))
    else:
        unspecified_response = "Unspecified Method\r\n"
        connection.sendall(str.encode(unspecified_response))
    connection.close()


while True:
    serverSocket.listen()
    print('The server is ready to receive')
    connectionSocket, addr = serverSocket.accept()

    thread = threading.Thread(target=threaded_client(connectionSocket), args=(connectionSocket,))
    try:
        connectionSocket.settimeout(10000)
    except:
        print("timeout")
    # thread.join(timeout=100/client_count)

    # thread.is_alive()
    thread.start()


