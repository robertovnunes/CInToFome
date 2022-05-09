from struct import *

import pickle
import time

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
    if isinstance(msg, str):
        checkSum = checksum(msg)
        data_len = len(msg)
        udp_header = pack("!III", port, data_len, checkSum)
        if sequencia % 2 == 0:
            pkt = b'0' + udp_header + msg.encode()
        else:
            pkt = b'1' + udp_header + msg.encode()
    elif isinstance(msg, int):
        udp_header = pack("!III", port, 4, 0)
        if sequencia % 2 == 0:
            pkt = b'0' + udp_header + msg.to_bytes(4, "little")
        else:
            pkt = b'1' + udp_header + msg.to_bytes(4, "little")
    return pkt

def udpextract(pacote):
    ack = pacote[0]
    udp_header = pacote[1:13]
    data = pacote[13:]
    udp_header = unpack('!III', udp_header)
    correct_checksum = udp_header[2]
    checksumr = checksum(data.decode())
    if correct_checksum == checksumr:
        # print("Checksum OK!")
        return ack, (ack+1) % 2, data.decode()
    else:
        # print("Checksum ERROR!")
        return ack, ack, ''


def createPkt(msg, nextAck):
    pkt = {
        "head": {
            "ack" : nextAck,
            "checksum": checksum(msg)
            },
        "msg": msg
    }
    return pickle.dumps(pkt)

def checkPkt(pkt):
    if(checksum(pkt["msg"]) == pkt["head"]["checksum"]):
        replyPkt = {
            "head": {
                "ack" : pkt["head"]["ack"],
                "checksum": ''
                },
            "msg": ''
        }
        replyPkt = pickle.dumps(replyPkt)
        return (replyPkt, True)
    else:
        wrongAck = 0
        if pkt["head"]["ack"] == 0:
            wrongAck = 1
        replyPkt = {
            "head": {
                "ack" : wrongAck,
                "checksum": 0
                },
            "msg": ''
        }
        replyPkt = pickle.dumps(replyPkt)
        return (replyPkt, False)

def nextAck(actualAck):
    if(actualAck == 0):
        return 1
    else:
        return 0;

def waitConfirmation(socket, nextAck):
    start = time.time()
    socket.settimeout(2.0)
    times = 1
    
    while True:
        # print("Esperando confimação...")
        try:
            reply, senderAddress = socket.recvfrom(2048)
            reply = pickle.loads(reply)
            # print(reply)
            if reply["head"]["ack"] == nextAck:
                if nextAck == 0:
                    nextAck = 1
                else:
                    nextAck = 0
                break
            else:
                print("ack incorreto!")
                print(f"tempo restante: {socket.gettimeout() - (time.time() - start)}")
                socket.settimeout(socket.gettimeout() - (time.time() - start))
        except Exception as e: # Não consegui fazer com exceção de timeout
            if times > 4:
                print(f"Esgotadas tentativas de reenvio")
                break
            times += 1
            print(f"{times}ª tentativa de envio")
    socket.settimeout(None)
    return nextAck
