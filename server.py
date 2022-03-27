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

class Mesa:
    def __init__(self, n_mesa):
        self.numero = n_mesa
        self.clientes = []


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))Mesas = []

comandos = dict(zip([1, 2, 3, 4, 5, 6], ['cardápio', 'pedir', 'conta individual', 'pagar', 'levantar', 'conta da mesa']))

while 1:
    comando, clientAddress = serverSocket.recvfrom(2048)
    if comando.decode() == 'chefia':








    #serverSocket.sendto(response.encode(), clientAddress)