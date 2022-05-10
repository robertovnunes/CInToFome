import time
from struct import *
from socket import *
from utilidades import *

class Cliente:
    def __init__(self, nomeCli, endereco):
        self.id = nomeCli
        self.valor_individual = 0
        self.porta = endereco[1]
        self.pedidos = {}

    def addpedido(self, descricao, valor):
        self.pedidos[descricao] = valor
        self.valor_individual = self.valor_individual + valor


    def getvalor(self):
        return self.valor_individual

    def getidr(self):
        return self.id

    def getvalues(self):
        return self.getidr(), self.pedidos, self.porta, self.getvalor()

    def __str__(self):
        return f'nome {self.id} valor {self.valor_individual}'




serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive")
Mesas = {}


serverPort = 12000
bufferSize = 512

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
serverSocket.settimeout(10.0)

comandos = dict(zip([1, 2, 3, 4, 5, 6], ['cardapio', 'pedir', 'conta individual', 'pagar', 'levantar', 'conta da mesa']))
cardapio = dict(zip(['Bife a milanesa', 'Frango a passarinha', 'Parmegiana', 'Bife à cavalo'], [35.00, 39.99, 20.00, 28.00]))

comando = ''

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
        response = createpkt("Digite a mesa", nextack, clientAddress[1])
        serverSocket.sendto(response, clientAddress)
        start = time.time()
        if time.time() - start == serverSocket.gettimeout() - 1:
            serverSocket.settimeout(10.0)
            start = time.time()
            serverSocket.sendto(response, clientAddress)

        #inicio rdt3.0 transmissor
        if ack == nextack:
            serverSocket.sendto(response, clientAddress)
        #fim rdt3.0

        #recebendo numero da mesa
        # inicio rdt3.0 receptor
        start = time.time()
        if time.time() - start == serverSocket.gettimeout() - 1:
            serverSocket.settimeout(10.0)
            start = time.time()
        datamesa = serverSocket.recvfrom(512)
        ack, nextack, mesastr = udpextract(datamesa[0])
        if ack == nextack:
            ackpkt = createpkt('.', ack, clientAddress[1])
            serverSocket.sendto(ackpkt, clientAddress)
            datamesa = serverSocket.recvfrom(18)
            ack, nextack, n_mesa = udpextract(datamesa[0])
        #fim rdt3.0

        n_mesaint = int(mesastr.strip())
        if len(Mesas) == 0 or n_mesaint not in Mesas:
            Mesas[n_mesaint] = {
                'numero': n_mesaint,
                'clientes': [],
                'total': 0.0
            }


        #Enviando pedido de nome do cliente
        pedirNome = createpkt('Digite seu nome', int(nextack), clientAddress[1])
        serverSocket.sendto(pedirNome, clientAddress)
        # inicio rdt3.0 transmissor
        start = time.time()
        if time.time() - start == serverSocket.gettimeout() - 1:
            serverSocket.settimeout(10.0)
            start = time.time()
            serverSocket.sendto(pedirNome, clientAddress)

        # inicio rdt3.0 transmissor
        if ack == nextack:
            serverSocket.sendto(pedirNome, clientAddress)
        # fim rdt3.0
        #fim rdt3.0

        #Recebendo nome do cliente
        # inicio rdt3.0 receptor
        start = time.time()
        if time.time() - start == serverSocket.gettimeout() - 1:
            serverSocket.settimeout(10.0)
            start = time.time()
        nomedata = serverSocket.recvfrom(512)
        ack, nextack, nome = udpextract(nomedata[0])
        if ack == nextack:
            ackpkt = createpkt('.', ack, clientAddress[1])
            serverSocket.sendto(ackpkt, clientAddress)
            nomedata = serverSocket.recvfrom(512)
            ack, nextack, nome = udpextract(nomedata[0])

        # fim rdt3.0
        #adicionando ou buscando cliente na tabela das mesas
        if Mesas[n_mesaint]['clientes'] == []:
            novocli = Cliente(nome, clientAddress)
            Mesas[n_mesaint]['clientes'].append(novocli)

        for cli in Mesas[n_mesaint]['clientes']:
            if nome == cli.getidr():
                achou = cli
            else:
                achou = []
        if achou == []:
            novocli = Cliente(nome, clientAddress)
            Mesas[n_mesaint]['clientes'].append(novocli)
        else:
            print(achou)
            menu = createpkt('menu', 0, clientAddress[1])
            serverSocket.sendto(menu, clientAddress)
            # inicio rdt3.0 transmissor
            start = time.time()
            if time.time() - start == serverSocket.gettimeout() - 1:
                serverSocket.settimeout(10.0)
                start = time.time()
                serverSocket.sendto(menu, clientAddress)
            # fim rdt3.0
            ackResponse = serverSocket.recv(512)
            ack, nextack, ackdata = udpextract(ackResponse)
            while ack != nextack:
                titulo = createpkt('Digite uma das opções a seguir: ', int(nextack), clientAddress[1])
                serverSocket.sendto(titulo, clientAddress)
                for ncommand in comandos:
                    cmdpkt = createpkt(f'{ncommand} - {comandos[ncommand]}', nextack, clientAddress[1])
                    serverSocket.sendto(cmdpkt, clientAddress)
                    # inicio rdt3.0 transmissor
                    start = time.time()
                    ackResponse = serverSocket.recv(512)
                    ack, nextack, ackdata = udpextract(ackResponse)

                cmdpkt = createpkt('#', nextack, clientAddress[1])
                serverSocket.sendto(cmdpkt, clientAddress)
    if comando == 'cardapio' or comando == '1':
        card = createpkt('cardapio', 0, clientAddress[1])
        serverSocket.sendto(card, clientAddress)
        # inicio rdt3.0 transmissor
        start = time.time()
        if time.time() - start == serverSocket.gettimeout() - 1:
            serverSocket.settimeout(10.0)
            start = time.time()
            serverSocket.sendto(card, clientAddress)
        # fim rdt3.0
        ackResponse = serverSocket.recv(512)
        ack, nextack, ackdata = udpextract(ackResponse)
        while ack != nextack:
            titulo = createpkt('Cardápio: ', int(nextack), clientAddress[1])
            serverSocket.sendto(titulo, clientAddress)
            for ncard in cardapio:
                cardpkt = createpkt(f'{ncard} - {cardapio[ncard][0]} '+f'{cardapio[ncard][1]}', nextack, clientAddress[1])
                serverSocket.sendto(cmdpkt, clientAddress)
                # inicio rdt3.0 transmissor
                start = time.time()
                ackResponse = serverSocket.recv(512)
                ack, nextack, ackdata = udpextract(ackResponse)

            cmdpkt = createpkt('#', nextack, clientAddress[1])
            serverSocket.sendto(cmdpkt, clientAddress)



serverSocket.close()