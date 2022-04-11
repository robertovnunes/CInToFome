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
seq = 0
while cmd != 'sair':
    apresentacao = f'{datetime.now().hour}:{datetime.now().minute}'
    cmd = input(f'{apresentacao} Cliente:')
    comando = createpkt(cmd, seq, serverPort)
    clientSocket.sendto(comando, (serverName, serverPort))
    ack, receive = udpextract(clientSocket.recvfrom(bufferSize)[0])

    #recebe do servidor

    while ACKresponse == b'0':
        clientSocket.sendto(comando, (serverName, serverPort))
    print(ACKresponse)


clientSocket.close()
