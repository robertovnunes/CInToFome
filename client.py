from socket import *

from urllib3 import Timeout
from utilidades import *
import pickle
import time

serverName = 'localhost'
serverPort = 12000

nextAck = 0

clientSocket = socket(AF_INET, SOCK_DGRAM)


# messages = ["Hello!", "My name is HR", "How's going?"]
appMessage = "Insira uma mensagem: "
while True:
    message = input(appMessage)
    print(f"enviando \'{message}\'")
    pkt = createPkt(message, nextAck)
    
    clientSocket.sendto(pkt, (serverName, serverPort))
    
    nextAck =  waitConfirmation(clientSocket, nextAck)
    reqRes, serverAddress = clientSocket.recvfrom(2048)
    reqRes = pickle.loads(reqRes)
    replyPkt, isOK = checkPkt(reqRes)
    clientSocket.sendto(replyPkt, serverAddress)
    if (isOK): 
        appMessage = reqRes["msg"]

clientSocket.close()
