import socket
from datetime import datetime
 

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

 

# Listen for incoming datagrams
clientMsg = ""
message=""
while str(message)!="tchau" :

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    clientMsg =  "{\n\tip: " + str(address) + " ; \n\tdate and time : " + dt_string +" ; \n\tmensagem : "+ str(message)+"\n}"
    
    print(clientMsg)

   

    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)