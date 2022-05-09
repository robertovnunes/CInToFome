from socket import *
import pickle
from utilidades import *

clients = {}

from utilidades import checkPkt, checksum, udpextract

serverName = 'localhost'
serverPort = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

nextAck = 0;

while True:
    print('Esperando mensagem do client')
    pkt, clientAddress = serverSocket.recvfrom(2048)
    pkt = pickle.loads(pkt)
    # print(pkt)
    replyPkt, isOK = checkPkt(pkt)
    serverSocket.sendto(replyPkt, clientAddress)
    if(isOK):
        print("Mensagem recebida com sucesso: ", pkt["msg"])
        if(pkt["msg"] == "chefia"):
            ip, porta = clientAddress
            id = f"{ip}:{porta}"
            print(id in clients)
            if ~(id in clients):
                clients[id] = {
                    "mesa" : '',
                    "contaIndividual": 0,
                    "pedidos": {}
                }
                reqRes = createPkt("Informe sua mesa: ", nextAck)
                serverSocket.sendto(reqRes, clientAddress)
                nextAck = waitConfirmation(serverSocket, nextAck)
                print (nextAck)
                
    else:
        print("Erro no recebimento da mensagem")

