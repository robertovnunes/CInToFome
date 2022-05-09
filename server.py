from socket import *
import pickle
from utilidades import *
from utilidades import checkPkt, checksum, udpextract

clients = {}
mesas = {}

# ESTADOS DO CLIENT
    # 1 - esperando o número da mesa
    # 2 - esperando o nome
    # 3 - registrado / pronto para requisitar algo
    # 4 - esperando o pedido

opcoesMsg = ("Escolha uma das opções:\n" + 
            "\t|1 - cardapio\n" +
            "\t|2 - pedir\n" +
            "\t|3 - conta individual\n" +
            "\t|4 - não fecho com robô, chame seu gerente\n" +
            "\t|5 - nada não, tava só testando\n" +
            "\t|6 - conta da mesa:\n")

cardapioMsg = ("\tCardapio:\n" +
                "\t1 - Bife a cavalo: 55.00\n" +
                "\t2 - Parmegiana: 20.00\n" + opcoesMsg)

cardapio = {
    "Bife a cavalo": 55.00,
    "Parmegiana": 20.00,
    "1": "Bife a cavalo",
    "2": "Parmegiana"
}

# print(cardapio)


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
            if not (id in clients):
                clients[id] = {
                    "mesa" : '',
                    "nome": '',
                    "contaIndividual": 0,
                    "pedidos": [],
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
                    mesa = pkt["msg"]
                    currentClient["mesa"] = mesa
                    currentClient["estado"] = 2
                    clients[id] = currentClient
                    if not (mesa in mesas):
                        mesas[mesa] = {"pedidos": [], "conta": 0, "clientes": [id]}
                    else:
                        mesas[mesa]["clientes"].append(id)
                        print(mesas)
                    reqRes = createPkt("Informe seu nome: ", nextAck) # cria pacote resposta a requisição
                
                elif(currentClient["estado"] == 2):
                    currentClient["nome"] = pkt["msg"]
                    currentClient["estado"] = 3
                    clients[id] = currentClient
                    reqRes = createPkt(opcoesMsg, nextAck) # cria pacote resposta a requisição
                
                elif(currentClient["estado"] == 3):
                    if(pkt["msg"] == "1" or pkt["msg"] == "1 - cardapio" or pkt["msg"] == "cardapio"):
                        reqRes = createPkt(f"{cardapioMsg}", nextAck) # cria pacote resposta a requisição
                    elif(pkt["msg"] == "2" or pkt["msg"] == "2 - pedir" or pkt["msg"] == "pedir"):
                        currentClient["estado"] = 4
                        clients[id] = currentClient
                        reqRes = createPkt(f"Informe o numero ou nome do prato (0 - voltar para opcoes): ", nextAck) # cria pacote resposta a requisição
                    elif(pkt["msg"] == "3" or pkt["msg"] == "3 - conta individual" or pkt["msg"] == "conta individual"):
                        valorIndividual = currentClient["contaIndividual"]
                        reqRes = createPkt(f"O valor da sua conta atual é: {valorIndividual}", nextAck) # cria pacote resposta a requisição
                    elif(pkt["msg"] == "6" or pkt["msg"] == "6 - conta da mesa" or pkt["msg"] == "conta da mesa"):
                        msgCM = ""
                        currentMesa = mesas[currentClient["mesa"]]
                        for idCliente in currentMesa["clientes"]:
                            cliente = clients[idCliente]
                            clienteNome = cliente["nome"]
                            clienteContaI = cliente["contaIndividual"]
                            msgCM += f"|{clienteNome}|\n"
                            for pedido in cliente["pedidos"]:
                                pedidoNome, pedidoPreco = pedido
                                msgCM += f"{pedidoNome} => {pedidoPreco}\n"
                            msgCM += f"Total - {clienteContaI}\n----------------------\n"
                        
                        totalMesa = currentMesa["conta"]
                        msgCM += f"Total da mesa - {totalMesa}\n----------------------\n"
                        reqRes = createPkt(f"{msgCM}", nextAck) # cria pacote resposta a requisição



                elif(currentClient["estado"] == 4):
                    if(pkt["msg"] == "0"):
                        currentClient["estado"] = 3
                        clients[id] = currentClient
                        reqRes = createPkt(opcoesMsg, nextAck) # cria pacote resposta a requisição
                    elif not (pkt["msg"] in cardapio):
                        reqRes = createPkt(f"Código não reconhecido. Insira novamente: ", nextAck) # cria pacote resposta a requisição
                    else:
                        keyPedido = pkt["msg"]
                        if keyPedido.isnumeric():
                            keyPedido = cardapio[keyPedido]
                                                        # nome       preço
                        currentClient["pedidos"].append((keyPedido, cardapio[keyPedido]))
                        currentClient["contaIndividual"] += cardapio[keyPedido]
                        currentClient["estado"] = 3
                        clients[id] = currentClient
                        
                        currentMesa = mesas[currentClient["mesa"]]
                        currentMesa["pedidos"].append((keyPedido, cardapio[keyPedido]))
                        currentMesa["conta"] += cardapio[keyPedido]
                        mesas[currentClient["mesa"]] = currentMesa
                        reqRes = createPkt(f"Pedido confirmado\n {opcoesMsg}", nextAck) # cria pacote resposta a requisição

                        print(mesas)


                        
                        
                
        
        # print(clients)
        # Enviaresposta da requisição
        serverSocket.sendto(reqRes, clientAddress)
        nextAck = waitConfirmation(serverSocket, nextAck)
                
    else:
        print("Erro no recebimento da mensagem")

