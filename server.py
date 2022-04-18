import time
from struct import *
from socket import *
from utilidades import *


serverPort = 12000
bufferSize = 512

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
serverSocket.settimeout(10.0)

#recebendo nome do arquivo
print("aguardando nome do arquivo a ser enviado")
data, clientAddress = serverSocket.recvfrom(512)
file_name = udpextract(data)[2]
file_name = file_name.split('/')
#while ack == nextack:
#    pacote = createpkt('', ack, clientAddress[1])
#    serverSocket.sendto(pacote, clientAddress)

print(f"nome do arquivo recebido {file_name}")
#recebendo quantidade de pacotes

data = serverSocket.recv(4)
numero_de_pacotes = int.from_bytes(data, "little")

comando = ''

serverSocket.settimeout(5.0)
file = open(f'./recebido/{file_name[1]}', "wb")
pacote_em_kilobytes = 512
pacote_em_bytes = pacote_em_kilobytes * 8

print(f"Recebendo {numero_de_pacotes} pacotes...")
start = time.time()
for i in range(numero_de_pacotes):
    data = serverSocket.recv(pacote_em_bytes+14)
    ack, nextack, dado = udpextract(data)
    while ack == nextack or received(data):
        serverSocket.sendto(ack, clientAddress)
        data = serverSocket.recv(pacote_em_bytes+14)
        ack, nextack, dado = udpextract(data)
    file.write(dado.encode())
    serverSocket.sendto(nextack.to_bytes(4, "little"), clientAddress)

    porcentagem = f"Baixando... {round((100*(i+1))/numero_de_pacotes, 2)}%"
    # print(porcentagem)
    print('\r'+porcentagem, end='')

tempo_de_download = round(time.time()-start, 2)
print(f"\nO download foi completo em {tempo_de_download} sec")

# Limpando buffers e sockets
file.close()
serverSocket.close()

'''
while comando != 'sair':
    message, clientAddress = serverSocket.recvfrom(bufferSize)
    ack, nextack, comando = udpextract(message)
    if ack == nextack:
          pacote = createpkt('', ack, clientAddress[1])
          serverSocket.sendto(pacote, clientAddress)
    else:
        pacote = createpkt(comando, nextack, clientAddress[1])
        serverSocket.sendto(pacote, clientAddress)
'''