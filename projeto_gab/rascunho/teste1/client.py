import socket

c = socket.socket()
c.connect( ('127.0.0.1', 9999) )
name = ""

while name != 'tchau':
    
    name = input("mensage: ")
    c.send(bytes(name , 'utf-8'))
    print(c.recv(1024).decode())

