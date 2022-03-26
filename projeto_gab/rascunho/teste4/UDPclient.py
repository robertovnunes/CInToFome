
import socket

def checksum(stri) :
    a=0
    stri = str(stri)
    for c in stri:
       a += ord(c)

    return a%2


serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024

ClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

mensagem = ""
while mensagem != "tchau":

    mensagem =   input( "mensagem: " )
    men      =   str.encode(mensagem)

    ClientSocket.sendto(men, serverAddressPort)
    ClientSocket.sendto( str.encode( str(checksum(men)) ), serverAddressPort)
    msgFromServer , addresserver= ClientSocket.recvfrom(bufferSize)
    ok = "ok"
    while msgFromServer != b'ok' :
        ClientSocket.sendto(men, serverAddressPort)
        ClientSocket.sendto( str.encode( str(checksum(men)) ), serverAddressPort)
        msgFromServer, addressserver = ClientSocket.recvfrom(bufferSize)



ClientSocket.close()