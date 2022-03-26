import socket

sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
sock.bind( ('127.0.0.1' , 12345))

while True :
    data, addr = sock.recvfrom( 4096 )
    print(str(data))
    message = bytes("hello I am UDP server").encode('utf-8')
    sock.sendto( message , addr )