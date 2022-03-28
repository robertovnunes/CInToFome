from datetime import datetime
from socket import *

def checksum(stri) :
    a=0
    stri = str(stri)
    for c in stri:
       a += ord(c)

    return a%2


serverName = 'localhost'
serverPort = 12000
bufferSize = 1024
clientSocket = socket(AF_INET, SOCK_DGRAM)
cmd = ''

while cmd != 'conta da mesa':
    apresentacao = f'{datetime.now().hour}:{datetime.now().minute}'
    cmd = input(f'{apresentacao} Cliente:')
    comando = str.encode(cmd)
    clientSocket.sendto(comando, (serverName, serverPort))
    clientSocket.sendto(str.encode(str(checksum(comando))), (serverName, serverPort))
    response, serverAddress = clientSocket.recvfrom(bufferSize)
    ok = 'ok'

    while response.decode() != 'ok':
        clientSocket.sendto(comando, (serverName, serverPort))
        clientSocket.sendto(str.encode(str(checksum(comando))), (serverName, serverPort))
        response, serverAddress = clientSocket.recvfrom(bufferSize)
        checkedResponse = clientSocket.recvfrom(bufferSize)

    if response.decode() == 'ok':
        clientSocket.sendto(comando, (serverName, serverPort))
    print(f'{apresentacao} CInToFome:', response.decode())


clientSocket.close()
