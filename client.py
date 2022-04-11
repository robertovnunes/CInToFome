from struct import *
from datetime import datetime
from socket import *

import utilidades
from utilidades import *


serverName = 'localhost'
serverPort = 12000
bufferSize = 1024
clientSocket = socket(AF_INET, SOCK_DGRAM)
cmd = ''

while cmd != 'sair':
    apresentacao = f'{datetime.now().hour}:{datetime.now().minute}'
    cmd = input(f'{apresentacao} Cliente:')
    comando = createpkt(cmd, serverPort)
    clientSocket.sendto(comando, (serverName, serverPort))

    #recebe do servidor
    ACKresponse, serverAddress = clientSocket.recvfrom(bufferSize)
    while ACKresponse == b'0':
        clientSocket.sendto(comando, (serverName, serverPort))
    print(ACKresponse)


clientSocket.close()
