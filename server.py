from struct import *
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


serverPort = 12000
bufferSize = 1024

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
message = ''

while message != 'sair':
    message, clientAddress = serverSocket.recvfrom(bufferSize)
    udp_header = message[:12]
    data = message[12:]
    udp_header = unpack("!III", udp_header)
    correct_checksum = udp_header[2]
    checkSum = checksum(data.decode())
    if correct_checksum == checkSum:
        sendmsg = f'voce digitou: {data.decode()}'
        checkSumC = checksum(sendmsg)
        data_len = len(sendmsg)
        udp_header = pack('!III', serverPort, data_len, checkSumC)
        mensagem = udp_header + sendmsg.encode()
        serverSocket.sendto(mensagem, clientAddress)
    else:
        msgString = 'ChecksumError'
        checkSumE = checksum(msgString)
        udp_error_head = pack('!IIII', serverPort, data_len, checkSumE, correct_checksum)
        msgError = udp_error_head + msgString.encode()
        serverSocket.sendto(msgError,  clientAddress)

