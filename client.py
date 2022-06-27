from socket import *

# from click._compat import raw_input

serverName = 'localhost'
serverPort = 80
caching = {}

while True:
    input_file = input('Input file: ')
    file = open(input_file, 'r')
    requests = file.read()
    file.close()
    # request = input('Input data:') + '\r\n'
    request = requests.strip('\r\n').split('\n')
    print(request)
    for i in range(len(request)):
        method, url, version, serverName, serverPort = request[i].split(' ')
        print(method, url, version, serverName, serverPort)
        request += '\r\n'
        serverPort = int(serverPort)
        if method == 'POST':
            url = url.strip('/')
            file = open(url, 'r')
            fread = file.read()
            file.close()
            request += fread
        if request[i] in caching.keys():
            response = caching.get(request[i])
            print("in cache")
        else:
            print("getting response from server")
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))
            clientSocket.sendall(request[i].encode())
            result = clientSocket.recv(1024).decode('utf-8')
            response = result.split('\r\n')
            caching[request[i]] = response
        response_msg, response_data = response[0], response[-1]
        print(response_msg)
        if method == 'GET':
            file = open("response.txt", 'w')
            print(response_data)
            file.write(response_data)
            file.close()
    clientSocket.close()
