import time
from struct import *
from socket import *
from utilidades import *

class Cliente:
    def __init__(self, nomeCli, endereco):
        self.id = nomeCli
        self.valor_individual = 0
        self.porta = endereco[1]
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
Mesa = {
    'numero': 0,
    'clientes': [],
    'total_mesa': 0.0
}


serverPort = 12000
bufferSize = 512

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
serverSocket.settimeout(10.0)

comandos = dict(zip([1, 2, 3, 4, 5, 6], ['cardápio', 'pedir', 'conta individual', 'pagar', 'levantar', 'conta da mesa']))

comando = ''
Mesas = []

while comando != 'sair':
    #recebendo comando do cliente
    start = time.time()
    if time.time() - start == serverSocket.gettimeout() - 1:
        serverSocket.settimeout(10.0)
        start = time.time()
        ackpkt = createpkt('.', ack, clientAddress[1])
        serverSocket.sendto(ackpkt, clientAddress)
    data, clientAddress = serverSocket.recvfrom(512)

    # inicio rdt3.0 receptor
    ack, nextack, comando = udpextract(data)
    if ack == nextack:
        ackpkt = createpkt('.', ack, clientAddress[1])
        serverSocket.sendto(ackpkt, clientAddress)
        data = serverSocket.recv(512)
        ack, nextack, comando = udpextract(data)
    #fim rdt3.0
    #tratando cada comando
    print(comando)
    if comando == 'chefia':
        #enviando pedido do numero da mesa
        response = createpkt("Digite a mesa", int(nextack), clientAddress[1])
        serverSocket.sendto(response, clientAddress)
        start = time.time()
        if time.time() - start == serverSocket.gettimeout() - 1:
            serverSocket.settimeout(10.0)
            start = time.time()
            serverSocket.sendto(response, clientAddress)

        #inicio rdt3.0 transmissor
        while (ack == nextack or time.time() - start == serverSocket.gettimeout()) and not received(ackResponse):
            if time.time() - start == serverSocket.gettimeout() - 1:
                serverSocket.settimeout(10.0)
                start = time.time()
                serverSocket.sendto(response, clientAddress)
            elif ackResponse == 0:
                serverSocket.sendto(response, clientAddress)
            ackResponse = serverSocket.recv(512)
            ack, nextack, ackdata = udpextract(ackResponse)
        #fim rdt3.0

        #recebendo numero da mesa
        # inicio rdt3.0 receptor
        start = time.time()
        datamesa = serverSocket.recvfrom(512)[0]
        ack, nextack, n_mesa = udpintextract(datamesa)
        while (ack == nextack or time.time() - start == serverSocket.gettimeout()) and not received(datamesa):
            if time.time() - start == serverSocket.gettimeout() - 1:
                serverSocket.settimeout(10.0)
                start = time.time()
                datamesa = serverSocket.recvfrom(18)
            elif ackResponse == 0:
                datamesa = serverSocket.recvfrom(18)
            ack, nextack, n_mesa = udpintextract(datamesa)
        #fim rdt3.0

        print('Mesa: ', n_mesa)

        #Enviando pedido de nome do cliente
        pedirNome = createpkt('Digite seu nome', int(nextack), clientAddress[1])
        serverSocket.sendto(pedirNome, clientAddress)
        # inicio rdt3.0 transmissor
        start = time.time()
        ackResponse = serverSocket.recv(18)
        ack, nextack, ackdata = udpextract(ackResponse)
        while (ack == nextack or time.time() - start == serverSocket.gettimeout()) and not received(ackResponse):
            if time.time() - start == serverSocket.gettimeout() - 1:
                serverSocket.settimeout(10.0)
                start = time.time()
                serverSocket.sendto(pedirNome, clientAddress)
            elif ackResponse == 0:
                serverSocket.sendto(pedirNome, clientAddress)
            ackResponse = serverSocket.recv(18)
            ack, nextack, ackdata = udpextract(ackResponse)
        #fim rdt3.0

        #Recebendo nome do cliente
        # inicio rdt3.0 receptor
        start = time.time()
        nomedata = serverSocket.recvfrom(512)
        ack, nextack, nome = udpextract(nomedata)
        while (ack == nextack or time.time() - start == serverSocket.gettimeout()) and not received(nomedata):
            if time.time() - start == serverSocket.gettimeout() - 1:
                serverSocket.settimeout(10.0)
                start = time.time()
                nomedata = serverSocket.recvfrom(512)
            elif ack == nextack:
                nomedata = serverSocket.recvfrom(512)
            ack, nextack, nome = udpextract(nomedata)
            ackResponse = serverSocket.recv(18)
            ack, nextack, ackdata = udpextract(ackResponse)
        # fim rdt3.0
        #adicionando ou buscando cliente na tabela das mesas
        if len(Mesas) == 0:
            Mesa['numero'] = n_mesa;
            Mesa['clientes'] = Cliente(nome, clientAddress)
            Mesas = Mesa
        elif len(Mesas) == 1:
            if n_mesa == Mesas['numero']:
                for cliente in Mesas['clientes']:
                    if cliente.id == nome:
                        # Enviando menu de pedidos para o cliente
                        menu = createpkt(' Digite uma das opções a seguir ', int(nextack), clientAddress[1])
                        serverSocket.sendto(menu, clientAddress)
                        # inicio rdt3.0 transmissor
                        start = time.time()
                        ackResponse = serverSocket.recv(18)
                        ack, nextack, ackdata = udpextract(ackResponse)
                        while (ack == nextack or time.time() - start == serverSocket.gettimeout()) and not received(
                                ackResponse):
                            if time.time() - start == serverSocket.gettimeout() - 1:
                                serverSocket.settimeout(10.0)
                                start = time.time()
                                serverSocket.sendto(pedirNome, clientAddress)
                            elif ackResponse == 0:
                                serverSocket.sendto(pedirNome, clientAddress)
                            ackResponse = serverSocket.recv(18)
                            ack, nextack, ackdata = udpextract(ackResponse)
                        # fim rdt3.0
                        for command in comandos:
                            cmdpkt = createpkt(f'{command[0]} - {command[1]}', int(nextack), clientAddress[1])
                            serverSocket.sendto(cmdpkt, clientAddress)
                            # inicio rdt3.0 transmissor
                            start = time.time()
                            ackResponse = serverSocket.recv(18)
                            ack, nextack, ackdata = udpextract(ackResponse)
                            while (ack == nextack or time.time() - start == serverSocket.gettimeout()) and not received(
                                    ackResponse):
                                if time.time() - start == serverSocket.gettimeout() - 1:
                                    serverSocket.settimeout(10.0)
                                    start = time.time()
                                    serverSocket.sendto(cmdpkt, clientAddress)
                                elif ackResponse == 0:
                                    serverSocket.sendto(cmdpkt, clientAddress)
                                ackResponse = serverSocket.recv(18)
                                ack, nextack, ackdata = udpextract(ackResponse)
                            # fim rdt3.0

        
    
    nextpkt = createpkt('', nextack, clientAddress[1])
    serverSocket.sendto(nextpkt, clientAddress)


serverSocket.close()