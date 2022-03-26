import socket

 

msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024

ClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


exit = 1

while exit != 0:
    mensagem =   input( "mensagem: " )
    men      =   str.encode(mensagem)

    ClientSocket.sendto(men, serverAddressPort)
    #msgFromServer = ClientSocket.recvfrom(bufferSize)


ClientSocket.close()