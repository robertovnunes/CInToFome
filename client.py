from socket import *

from urllib3 import Timeout
from utilidades import *
import pickle
import time
from datetime import datetime

serverName = 'localhost'
serverPort = 12000

nextAck = 0

clientSocket = socket(AF_INET, SOCK_DGRAM)


# messages = ["Hello!", "My name is HR", "How's going?"]
agora = datetime.now().strftime('%H:%M')

appMessage = f"{agora} CINtoFome:Bem vindo ao CintoFome!\n:"
msgServer = ''

while not (msgServer == "Até a próxima!"): # vai executar até que o servidor envie 'Até a próxima!'
    message = input(appMessage) # captura a mensagem do cliente
    
    agora = datetime.now().strftime('%H:%M')
    print (f"{agora} Cliente:{message}")
    
    pkt = createPkt(message, nextAck) # cria o pacote com o ack a ser enviado
    
    clientSocket.sendto(pkt, (serverName, serverPort)) # envia o pacote
    
    nextAck =  waitConfirmation(clientSocket, nextAck) # aguarda confirmação de recebimento do servidor

    reqRes, serverAddress = clientSocket.recvfrom(2048) # Aguarda a resposta da requisição enviada a servidor
    reqRes = pickle.loads(reqRes) # remonta o pacote recebido
    replyPkt, isOK = checkPkt(reqRes) # verifica se o checksum bate e retorna o pacote de resposta

    clientSocket.sendto(replyPkt, serverAddress) # manda o pacote de resposta(se deu certo ou nao) ao servidor
    
    if (isOK): # se deu certo, apresenta a mensagem recebida ao cliente
        agora = datetime.now().strftime('%H:%M')
        msgServer = reqRes["msg"] 
        appMessage = f"{agora} CINtoFome: {msgServer}"

agora = datetime.now().strftime('%H:%M')
print(f"{agora} CINtoFome:Até a próxima")
clientSocket.close() # encerra o socket
