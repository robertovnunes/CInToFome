from struct import *
from socket import *
from utilidades import *


serverPort = 12000
bufferSize = 1024

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
comando = ''

while comando != 'sair':
    message, clientAddress = serverSocket.recvfrom(bufferSize)
    ack, nextack, comando = udpextract(message)
    if ack == nextack:
          pacote = createpkt(comando, ack, clientAddress[1])
          serverSocket.sendto(pacote, clientAddress)
    else:
        pacote = createpkt(comando, nextack, clientAddress[1])
        serverSocket.sendto(pacote, clientAddress)
