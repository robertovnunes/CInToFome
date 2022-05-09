from socket import *
import pickle
from utilidades import *
from utilidades import checkPkt, checksum, udpextract

clients = {}

# ESTADOS DO CLIENT
    # 1 - esperando o número da mesa
    # 2 - esperando o nome
    # 3 - registrado

opcoesMsg = ("Escolha uma das opções:\n" + 
            "1 - cardápio\n" +
            "2 - pedido\n" +
            "3 - conta individual\n" +
            "4 - não fecho com robô, chame seu gerente\n" +
            "5 - nada não, tava só testando\n" +
            "6 - conta da mesa")

serverName = 'localhost'
serverPort = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

nextAck = 0

while True:
    print('Esperando mensagem do client')
    pkt, clientAddress = serverSocket.recvfrom(2048)
    pkt = pickle.loads(pkt)
    # print(pkt)
    replyPkt, isOK = checkPkt(pkt)
    serverSocket.sendto(replyPkt, clientAddress)
    if(isOK):
        # print("Mensagem recebida com sucesso: ", pkt["msg"])
        if(pkt["msg"] == "chefia"):
            ip, porta = clientAddress
            id = f"{ip}:{porta}"
            # print(id in clients)
            if ~(id in clients):
                clients[id] = {
                    "mesa" : '',
                    "contaIndividual": 0,
                    "pedidos": {},
                    "estado": 1
                }
                reqRes = createPkt("Informe sua mesa: ", nextAck) # cria pacote resposta a requisição
                # print (nextAck)
        else:
            ip, porta = clientAddress 
            id = f"{ip}:{porta}"
            if ( not (id in clients)):
                reqRes = createPkt("Envie \'chefia\' para começar o cadastro: ", nextAck) # cria pacote resposta a requisição
            else:
                currentClient = clients[id]
                if(currentClient["estado"] == 1):
                    # !! Falta verificação se a mensagem mandada foi int !!
                    currentClient["mesa"] = pkt["msg"]
                    currentClient["estado"] = 2
                    clients[id] = currentClient
                    reqRes = createPkt("Informe seu nome: ", nextAck) # cria pacote resposta a requisição
                elif(currentClient["estado"] == 2):
                    currentClient["nome"] = pkt["msg"]
                    currentClient["estado"] = 3
                    clients[id] = currentClient
                    reqRes = createPkt(opcoesMsg, nextAck) # cria pacote resposta a requisição
        
        print(clients)
        # Enviaresposta da requisição
        serverSocket.sendto(reqRes, clientAddress)
        nextAck = waitConfirmation(serverSocket, nextAck)
                
    else:
        print("Erro no recebimento da mensagem")

