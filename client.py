import time
from struct import *
from datetime import datetime
from socket import *
import os

import utilidades
from utilidades import *


serverName = 'localhost'
serverPort = 12000
bufferSize = 1024
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.connect((serverName, serverPort))
clientSocket.settimeout(10.0)
path = './arquivo.txt'

#abre, em modo de leitura de byte, o arquivo a ser enviado
file = open(path, 'r')

#enviando nome do arquivo ao servidor

clientSocket.sendto(createpkt(path, 0, serverPort), (serverName, serverPort))

file_size = os.path.getsize(path)  # Size in bits
pacote_em_kilobytes = 512
pacote_em_bytes = pacote_em_kilobytes * 8

#enviando numero de pacotes
numero_de_pacotes = (file_size // pacote_em_bytes) + 14
clientSocket.sendto(numero_de_pacotes.to_bytes(4, "little"), (serverName, serverPort))

delay = 0.004
tempo_estimado = numero_de_pacotes*(delay*1.2)

for i in range(numero_de_pacotes):
    dado = file.read(pacote_em_bytes)
    pacote = createpkt(dado, i, serverPort)
    clientSocket.sendto(pacote, (serverName, serverPort))
    enviado = f"{int((i+1)*pacote_em_kilobytes)}/{int(pacote_em_kilobytes*numero_de_pacotes)}Kb"
    print('\r'+enviado, end='')
    time.sleep(delay)

clientSocket.close()
file.close()

'''
cmd = ''
seq = 0
while cmd != 'sair':
    apresentacao = f'{datetime.now().hour}:{datetime.now().minute}'
    cmd = input(f'{apresentacao} Cliente:')
    comando = createpkt(cmd, seq, serverPort)
    clientSocket.sendto(comando, (serverName, serverPort))
    ack, nextack, receive = udpextract(clientSocket.recvfrom(bufferSize)[0])
    print(receive)
    #recebe do servidor

    while ack == nextack:
        clientSocket.sendto(comando, (serverName, serverPort))
    seq = seq + 1


clientSocket.close()
'''