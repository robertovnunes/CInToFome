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
    udp_header = message[:12]
    data = message[12:]
    udp_header = unpack("!III", udp_header)
    correct_checksum = udp_header[2]
    checkSum = checksum(data.decode())
    if correct_checksum == checkSum:
        comando = data.decode()
        print(comando)
        serverSocket.sendto(b'1', clientAddress)
    else:
        serverSocket.sendto(b'0', clientAddress)
