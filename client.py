from datetime import datetime
from socket import *

def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
comando = '0'
while(comando != '6' or comando != 'conta da mesa'):
    apresentacao = f'{datetime.now().hour}:{datetime.now().minute}'
    comando = input(f'{apresentacao} Cliente:')
    clientSocket.sendto(comando.encode(), (serverName, serverPort))
    response, serverAddress = clientSocket.recvfrom(2048)
    print(f'{apresentacao} CInToFome:', response.decode())

clientSocket.close()
