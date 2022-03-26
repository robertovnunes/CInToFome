import socket

s = socket.socket()
print('socket Created')

s.bind(('127.0.0.1', 9999))

s.listen(3)
print('waiting for connections...')
names = ""

#c , addr = s.accept()
#
#name = c.recv(1024).decode()
#c.send( bytes('welcome to telusko', 'utf-8') )

c , addr = s.accept() 
print("Connected with : ", addr)
while names != 'tchau':
    
    names = c.recv(1024).decode()
    print("recevied: ", names)
    c.send( bytes('~', 'utf-8') )

c.close()


s.close()