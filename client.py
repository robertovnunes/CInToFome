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
while True:
    message = input(appMessage)
    agora = datetime.now().strftime('%H:%M')
    print (f"{agora} Clientee:{message}")
    pkt = createPkt(message, nextAck)
    
    clientSocket.sendto(pkt, (serverName, serverPort))
    
    nextAck =  waitConfirmation(clientSocket, nextAck)
    reqRes, serverAddress = clientSocket.recvfrom(2048)
    reqRes = pickle.loads(reqRes)
    replyPkt, isOK = checkPkt(reqRes)
    clientSocket.sendto(replyPkt, serverAddress)
    if (isOK):
        agora = datetime.now().strftime('%H:%M')
        msgServer = reqRes["msg"] 
        appMessage = f"{agora} CINtoFome: {msgServer}"

clientSocket.close()
