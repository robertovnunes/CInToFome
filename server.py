from socket import *
from threading import *


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
        return self.numero, self.clientes, self.total


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
Mesas = []
comandos = ['Digite uma das opções','1 - cardápio', '2 - pedir', '3 - conta individual', '4 - pagar', '5 - levantar', '6 - conta da mesa']
# response = {1:'Digite sua mesa', 2:'Digite seu nome', 3:'Digite uma opção', 4:'Digite qual o item que gostaria', 5:}
while 1:
    comando, clientAddress = serverSocket.recvfrom(2048)
    if comando.decode() == 'chefia':
        serverSocket.sendto('Digite a mesa:'.encode(), clientAddress)
        n_mesa, clientAddress = serverSocket.recvfrom(2048)
        serverSocket.sendto('Digite seu nome:'.encode(), clientAddress)
        nome, clientAddress = serverSocket.recvfrom(2048)
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
            # fim da adição de um novo cliente
    ##elif comando.decode() == 'cardapio':
    for i in len(comandos):
        serverSocket.sendall(comandos[i].encode(), clientAddress)


# serverSocket.sendto(response.encode(), clientAddress)
