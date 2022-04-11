from struct import *
from datetime import datetime
from socket import *

def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)


def checksum(msg):
    s = 0
    for i in range(0, len(msg)-2, 2):
        w = ord(msg[i]) + (ord(msg[i + 1]) << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff



serverName = 'localhost'
serverPort = 12000
bufferSize = 1024
clientSocket = socket(AF_INET, SOCK_DGRAM)
cmd = ''

while cmd != 'sair':
    apresentacao = f'{datetime.now().hour}:{datetime.now().minute}'
    cmd = input(f'{apresentacao} Cliente:')
    checkSum = checksum(cmd)
    data_len = len(cmd)
    udp_header = pack("!III", serverPort, data_len, checkSum)
    comando = udp_header + cmd.encode()
    clientSocket.sendto(comando, (serverName, serverPort))

    #recebe do servidor
    response, serverAddress = clientSocket.recvfrom(bufferSize)
    udp_header = response[:12]
    data = response[12:]
    udp_header = unpack('!III', udp_header)
    correct_checksum = udp_header[2]
    checkSumR = checksum(data.decode())
    if correct_checksum == checkSumR:
        print(f'{apresentacao} Servidor:', data.decode())


clientSocket.close()
