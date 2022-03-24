from datetime import datetime
from socket import *
from threading import Thread


class Cliente:
    def __init__(self, nomeCli, endereco):
        self.id = nomeCli
        self.valor_individual = 0
        self.porta = endereco
        self.pedidos = []

    def setpedido(self, descricao, valor):
        self.pedidos[descricao] = valor

    def setid(self, nomeCliente):
        self.id = nomeCliente


    def cardapio(self):

        return

    def getvalor(self):
        return self.valor_total

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive")
Mesas = {
    'numero': '',
    'clientes': [],
    'total_mesa': 0
}

comandos = dict(zip([1, 2, 3, 4, 5, 6], ['cardápio', 'pedir', 'conta individual', 'pagar', 'levantar', 'conta da mesa']))

while 1:
    comando, clientAddress = serverSocket.recvfrom(2048)
    if comando.decode() == 'chefia':
        response = "Digite a mesa"
        serverSocket.sendto(response.encode(), clientAddress)
        n_mesa, clientAddress = serverSocket.recvfrom(2048)
        print('Mesa: ', n_mesa)
        if len(Mesas) > 0:
            pedirNome = 'Digite seu nome'
            serverSocket.sendto(pedirNome.encode(), clientAddress)
            nome, clientAddress = serverSocket.recvfrom(2048)
            cliente = Cliente(nome, n_mesa, clientAddress)
            Clientes.append(cliente)







    #serverSocket.sendto(response.encode(), clientAddress)