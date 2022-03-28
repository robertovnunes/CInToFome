from socket import *


class Cliente:
    def __init__(self, nomeCli, endereco):
        self.id = nomeCli
        self.valor_individual = 0
        self.porta = endereco
        self.pedidos = {'': 0}

    def __str__(self):
        return f'{self.id, self.porta[0], self.porta[1]}'

    def setpedido(self, descricao, valor):
        self.pedidos[f'{descricao}'] = valor
        self.valor_individual = self.valor_individual+valor

    def getvalores(self):
        return self.id, self.porta[0], self.porta[1], self.pedidos, self.valor_individual



class Mesa:
    def __init__(self, numero):
        self.numero = numero
        self.clientes = []
        self.total = 0

    def getvalues(self):
        return self.numero

def checksum(stri) :
    a=0
    stri = str(stri)
    for c in stri:
       a += ord(c)

    return a%2

serverPort = 12000
bufferSize  = 1024

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

Mesas = []
clientMsg = ''
message = ''
comandos = ['Digite uma das opções','1 - cardápio', '2 - pedir', '3 - conta individual', '4 - pagar', '5 - levantar', '6 - conta da mesa']

while 1:
    message, clientAddress = serverSocket.recvfrom(bufferSize)
    bytesAddressPair = serverSocket.recvfrom(bufferSize)
    checkmessage = bytesAddressPair[0]
    checkaddress = bytesAddressPair[1]
    check = str(checksum(message)).encode()
    error = 'error'
    ok = 'ok'
    while check != checkmessage:
        serverSocket.send(error.encode(), clientAddress)
        mens = serverSocket.recvfrom(bufferSize)
        messsage = mens[0]
        address = mens[1]
        checkmessage, checkaddress = serverSocket.recvfrom(bufferSize)
        check = str(checksum(message)).encode()

    serverSocket.sendto(ok.encode(), checkaddress)

    message, clientAddress = serverSocket.recvfrom(bufferSize)
    while message.decode() != 'conta da mesa':
        print(message.decode())
        if message.decode() == 'chefia':
            serverSocket.sendto('Digite a mesa:'.encode(), clientAddress)
            n_mesa, clientAddress = serverSocket.recvfrom(bufferSize)
            serverSocket.sendto('Digite seu nome:'.encode(), clientAddress)
            nome, clientAddress = serverSocket.recvfrom(bufferSize)
            cliente = Cliente(nome.decode(), clientAddress)
            if len(Mesas) == 0:
                tMesa = Mesa(n_mesa)
                tMesa.clientes.append(cliente)
                Mesas.append(tMesa)
            else:
                for tMesa in Mesas:
                    if tMesa.numero == n_mesa:
                        tMesa.clientes.append(cliente)
                    else:
                        novaMesa = Mesa(n_mesa)
                        novaMesa.clientes.append(cliente)
                        Mesas.append(novaMesa)




