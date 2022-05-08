import time
from struct import *
from datetime import datetime
from socket import *
import os

import utilidades
from utilidades import *


serverName = 'localhost'
serverPort = 12000
serverAddress = (serverName, serverPort)
bufferSize = 1024
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.connect((serverName, serverPort))
clientSocket.settimeout(10.0)

cmd = ''
seq = 0
while cmd != 'sair':
    apresentacao = f'{datetime.now().hour}:{datetime.now().minute}'

    #le comando e envia para o servidor
    cmd = input(f'{apresentacao} Cliente:')
    comandopkt = createpkt(cmd, seq, serverPort)
    clientSocket.sendto(comandopkt, serverAddress)
    #inicio rdt3.0 transmissor
    start = time.time()
    if time.time() - start == clientSocket.gettimeout() - 1:
        clientSocket.settimeout(10.0)
        start = time.time()
        clientSocket.sendto(comandopkt, serverAddress)
    #se o comando for a conta da mesa ou conta individual, o servidor envia dois inteiros e os concatena
    if cmd == 'conta da mesa' or cmd == 'conta individual':
        #recebendo parte inteira da conta
        dataint = clientSocket.recv(18)
        timer = time.time()
        ack, nextack, intfloat = udpintextract(dataint)
        # inicio rdt3.0 receptor
        while (ack == nextack or time.time()-timer == clientSocket.gettimeout()) and not received(dataint):
            ackpkt = createpkt('.', ack, serverPort)
            if time.time()-timer == clientSocket.gettimeout()-1:
                timer = time.time()
                clientSocket.settimeout(10.0)
                clientSocket.sendto(ackpkt, serverAddress)
            elif ack == nextack:
                clientSocket.sendto(ackpkt, serverAddress)
            dataint = clientSocket.recv(18)
            ack, nextack, intfloat= udpintextract(dataint)

        #recebendo parte decimal da conta
        datadec = clientSocket.recv(18)
        timer = time.time()
        ack, nextack, decfloat = udpintextract(datadec)
        # inicio rdt3.0 receptor
        while (ack == nextack or time.time() - timer == clientSocket.gettimeout()) and not received(datadec):
            ackpkt = createpkt('.', ack, serverPort)
            if time.time() - timer == clientSocket.gettimeout() - 1:
                timer = time.time()
                clientSocket.settimeout(10.0)
                clientSocket.sendto(ackpkt, serverAddress)
            elif ack == nextack:
                clientSocket.sendto(ackpkt, serverAddress)
            datadec = clientSocket.recv(18)
            ack, nextack, decfloat = udpintextract(datadec)
        #fim rdt3.0
        print(f'{apresentacao} servidor: R${intfloat},{decfloat}')

    #se for qualquer outro comando, só imprime
    else:
        start = time.time()
        if time.time() - start == clientSocket.gettimeout() - 1:
            clientSocket.settimeout(10.0)
            start = time.time()
            ackpkt = createpkt('.', int(ack), serverPort)
            clientSocket.sendto(ackpkt, serverAddress)
        data = clientSocket.recvfrom(512)[0]
        # inicio rdt3.0 receptor
        ack, nextack, dataResponse = udpextract(data)
        if ack == nextack:
            ackpkt = createpkt('.', int(ack), serverPort)
            clientSocket.sendto(ackpkt, serverAddress)
            data = clientSocket.recv(512)
            ack, nextack, comando = udpextract(data)
        #fim rdt3.0 receptor
        print(f'{apresentacao} servidor: {dataResponse}')
    seq = seq + 1
    #nxtack = createpkt('.', nextack, serverPort)
    #clientSocket.sendto(nxtack, serverAddress)

clientSocket.close()
