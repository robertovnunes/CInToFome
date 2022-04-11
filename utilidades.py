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


def createpkt(msg, port):
    checkSum = checksum(msg)
    data_len = len(msg)
    udp_header = pack("!III", port, data_len, checkSum)
    pkt = udp_header + msg.encode()
    return pkt

#def udpextract(pacote):
#    udp_header = pacote[:12]
#    data = pacote[12:]
#    udp_header = unpack('!III', udp_header)
#    correct_checksum = udp_header[2]
#    correct_checksum = int(correct_checksum)
#    checksumr = checksum(data.decode())
#    return data.decode()
