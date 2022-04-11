from struct import *


def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)


def checksum(msg):
    s = 0
    for i in range(0, len(msg) - 2, 2):
        w = ord(msg[i]) + (ord(msg[i + 1]) << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff


def createpkt(msg, sequencia, port):
    checkSum = checksum(msg)
    data_len = len(msg)
    udp_header = pack("!III", port, data_len, checkSum)
    if sequencia % 2 == 0:
        pkt = b'0' + udp_header + msg.encode()
    else:
        pkt = b'1' + udp_header + msg.encode()
    return pkt


def udpextract(pacote):
    ack = pacote[0]
    udp_header = pacote[1:13]
    data = pacote[13:]
    udp_header = unpack('!III', udp_header)
    correct_checksum = udp_header[2]
    checksumr = checksum(data.decode())
    if correct_checksum == checksumr:
        return ack, ack+1, data.decode()
    else:
        return ack, ack, ''

