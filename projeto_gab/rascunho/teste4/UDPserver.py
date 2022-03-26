import socket
from datetime import datetime
 
def checksum(stri) :
    a=0
    stri = str(stri)
    for c in stri:
       a += ord(c)

    return a%2


localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Listen for incoming datagrams
clientMsg = ""
message=""

while message !=b'tchau' :
    
    message , address = UDPServerSocket.recvfrom(bufferSize)
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    checkmessage = bytesAddressPair[0]
    checkaddress = bytesAddressPair[1]

    check = str(checksum(message)).encode()
    error = "error"
    ok = "ok"

    while check != checkmessage:
        UDPServerSocket.send( error.encode()  ,  address )
        mens = UDPServerSocket.recvfrom(bufferSize)
        messsage = mens[0]
        address = mens[1]
        checkmessage , checkaddress = UDPServerSocket.recvfrom(bufferSize)
        check = str(checksum(message)).encode()
    

    UDPServerSocket.sendto( b'ok'  ,  checkaddress )


    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    clientMsg =  "{\n\tip: \"" + str(address) + "\" ; \n\tdate and time : " + dt_string +" ; \n\tmensagem : "+  message.decode()+"\n}"
    
    print(clientMsg)