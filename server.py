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
    # 5 - esperando pagamento

opcoesMsg = ("Escolha uma das opções:\n" + 
            "\t|1 - cardapio\n" +
            "\t|2 - pedir\n" +
            "\t|3 - conta individual\n" +
            "\t|4 - não fecho com robô, chame seu gerente\n" +
            "\t|5 - nada não, tava só testando\n" +
            "\t|6 - conta da mesa:\n" + 
            "\t|7 - pagar\n" +
            "\t|8 - levantar\n:")

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
    pkt, clientAddress = serverSocket.recvfrom(2048) # fica esperando uma mensagem recebida por algum cliente
    pkt = pickle.loads(pkt) # remonta o objeto dicionário pkt recebido
    replyPkt, isOK = checkPkt(pkt) # faz a checagem do pacote. Se ocorreu tudo bem isOK = True
                                    # replyPkt é o pacote criado para responder. Se deu certo, replyPkt terá ack igual a mensagem recebida
    serverSocket.sendto(replyPkt, clientAddress) # responde ao cliente com o pacote respostas
    # Se ocorreu tudo bem, a partir daqui começa a verificação da mensagem recebida e criação do resposta a requisição
    if(isOK):
        # se a mensagem recebida foi 'chefia' significa que um novo cliente está começando a se cadastrar
        if(pkt["msg"] == "chefia"):
            ip, porta = clientAddress
            id = f"{ip}:{porta}" # o cliente será indexado pelo seu IP e Porta
            if not (id in clients): # se ainda não existe um cliente com esse IP e Porta, cria um novo
                clients[id] = {
                    "mesa" : '',
                    "nome": '',
                    "contaIndividual": 0,
                    "pedidos": [],
                    "estado": 1
                }
                # criação do pacote resposta com o ack que o servidor irá enviar
                reqRes = createPkt("Informe sua mesa (número): ", nextAck) # cria pacote resposta a requisição
        
        else:
            ip, porta = clientAddress 
            id = f"{ip}:{porta}"
            # se um cliente não cadastrado manda mensagem, é pedido que ele comece o cadastro
            if ( not (id in clients)):
                reqRes = createPkt("Envie \'chefia\' para começar o cadastro: ", nextAck) # cria pacote resposta a requisição
            else:
                currentClient = clients[id] # pega de 'clientes' os dados do 'cliente que mandou a requisição
                #ESTADO 1: ESPERANDO O NUMERO DA MESA
                if(currentClient["estado"] == 1):
                    mesa = pkt["msg"] # atribuindo a mesa o valor enviado pelo cliente
                    currentClient["mesa"] = mesa
                    currentClient["estado"] = 2
                    clients[id] = currentClient
                    #Se essa mesa ainda não existe no objeto mesas, é criada uma nova
                    if not (mesa in mesas):
                        mesas[mesa] = {"pedidos": [], "conta": 0, "clientes": [id]}
                    # Se já existe a mesa, é adicionado o novo cliente a ela
                    else:
                        mesas[mesa]["clientes"].append(id)
                        print(mesas)
                    reqRes = createPkt("Informe seu nome: ", nextAck) # cria pacote resposta a requisição
                
                #ESTADO 2: ESPERANDO O NOME
                elif(currentClient["estado"] == 2):
                    currentClient["nome"] = pkt["msg"]
                    currentClient["estado"] = 3
                    clients[id] = currentClient
                    reqRes = createPkt(opcoesMsg, nextAck) # cria pacote resposta a requisição
                
                #ESTADO 3: CLIENTE REGISTRADO
                #A partir daqui o cliente pode fazer várias requisições
                elif(currentClient["estado"] == 3):
                    #REQUISIÇÃO DO CARDÁPIO
                    if(pkt["msg"] == "1" or pkt["msg"] == "1 - cardapio" or pkt["msg"] == "cardapio"):
                        reqRes = createPkt(f"{cardapioMsg}", nextAck) # cria pacote resposta a requisição
                    
                    #REQUISIÇÃO PARA PEDIR ALGO
                    elif(pkt["msg"] == "2" or pkt["msg"] == "2 - pedir" or pkt["msg"] == "pedir"):
                        currentClient["estado"] = 4
                        clients[id] = currentClient
                        reqRes = createPkt(f"Informe o numero ou nome do prato (0 - voltar para opcoes): ", nextAck) # cria pacote resposta a requisição
                    
                    #REQUISIÇÃO DO CONTA INDIVIDUAL
                    elif(pkt["msg"] == "3" or pkt["msg"] == "3 - conta individual" or pkt["msg"] == "conta individual"):
                        valorIndividual = currentClient["contaIndividual"]
                        reqRes = createPkt(f"O valor da sua conta atual é: {valorIndividual}\n{opcoesMsg}", nextAck) # cria pacote resposta a requisição
                    
                    elif(pkt["msg"] == "4" or pkt["msg"] == "4 - não fecho com robô, chame seu gerente" or pkt["msg"] == "não fecho com robô, chame seu gerente"):
                        reqRes = createPkt(f"Bora sair na mão então", nextAck) # cria pacote resposta a requisição

                    elif(pkt["msg"] == "5" or pkt["msg"] == "5 - nada não, tava só testando" or pkt["msg"] == "nada não, tava só testando"):
                        reqRes = createPkt(f"OK!", nextAck) # cria pacote resposta a requisição

                    #REQUISIÇÃO DO CARDÁPIO
                    elif(pkt["msg"] == "6" or pkt["msg"] == "6 - conta da mesa" or pkt["msg"] == "conta da mesa"):
                        msgCM = ""
                        currentMesa = mesas[currentClient["mesa"]]
                        #Construção da mensagem contendo os valores de conta e os pedidos de cada cliente da mesa
                        for idCliente in currentMesa["clientes"]:
                            cliente = clients[idCliente]
                            clienteNome = cliente["nome"]
                            clienteContaI = cliente["contaIndividual"]
                            msgCM += f"\n|\t{clienteNome}\t|\n"
                            for pedido in cliente["pedidos"]:
                                pedidoNome, pedidoPreco = pedido
                                msgCM += f"{pedidoNome} => {pedidoPreco}\n"
                            msgCM += f"Total - {clienteContaI}\n----------------------\n"
                        
                        totalMesa = currentMesa["conta"]
                        msgCM += f"Total da mesa - {totalMesa}\n----------------------\n"
                        reqRes = createPkt(f"{msgCM}\n{opcoesMsg}", nextAck) # cria pacote resposta a requisição
                    
                    #Requisição de pagamento
                    #Nesse estado o cliente pode mudar para o estado 5: esperando pagamento
                    elif(pkt["msg"] == "7" or pkt["msg"] == "7 - pagar" or pkt["msg"] == "pagar"):
                        currentClient["estado"] = 5
                        clients[id] = currentClient
                        valorIndividual = currentClient["contaIndividual"]
                        reqRes = createPkt(f"O valor da sua conta individual é: {valorIndividual}\nQuanto deseja pagar? (0 -caso queira voltar)", nextAck) # cria pacote resposta a requisição

                    #Requisição para se levantar
                    elif(pkt["msg"] == "8" or pkt["msg"] == "8 - levantar" or pkt["msg"] == "levantar"):
                        #verifica se o cliente já pagou a conta
                        if(currentClient["contaIndividual"] == 0):
                            currentMesa = mesas[currentClient["mesa"]]
                            currentMesa["clientes"].remove(id)
                            if (len( currentMesa["clientes"]) == 0):
                                del mesas[currentClient["mesa"]]
                            del clients[id]
                            reqRes = createPkt(f"Até a próxima!", nextAck) # cria pacote resposta a requisição
                        else:
                            reqRes = createPkt(f"Você ainda não pagou sua conta!\n{opcoesMsg}", nextAck) # cria pacote resposta a requisição

                #ESTADO 4: Esperando o pedido
                elif(currentClient["estado"] == 4):
                    #Se a mensagem for 0, o cliente retorna ao estado 3 e retorna ao menu de opções
                    if(pkt["msg"] == "0"):
                        currentClient["estado"] = 3
                        clients[id] = currentClient
                        reqRes = createPkt(opcoesMsg, nextAck) # cria pacote resposta a requisição
                    #Verifica se o que foi enviado pelo cliente pode ser encontrado no cardápio
                    elif not (pkt["msg"] in cardapio):
                        reqRes = createPkt(f"Código não reconhecido. Insira novamente: ", nextAck) # cria pacote resposta a requisição
                    #Registra o pedido na conta individual do cliente e na mesa em que ele está
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
                        reqRes = createPkt(f"Pedido confirmado!!\n {opcoesMsg}", nextAck) # cria pacote resposta a requisição
                
                #ESTADO 5: Esperando pagamento
                elif(currentClient["estado"] == 5):
                    valor = pkt["msg"]
                    # verifica se o que foi enviado pelo cliente é um valor numérico
                    if not (valor.isnumeric()):
                        reqRes = createPkt(f"Insira um valor numérico: ", nextAck) # cria pacote resposta a requisição
                    # se sim, verifica se o valor está de acordo com a conta e faz a dedução da conta individual e da mesa
                    else:
                        valor = float(valor)
                        print (valor < currentClient["contaIndividual"])
                        if(valor == 0):
                            currentClient["estado"] = 3
                            clients[id] = currentClient
                            reqRes = createPkt(f"{opcoesMsg}", nextAck) # cria pacote resposta a requisição
                        elif(valor < currentClient["contaIndividual"]):
                            reqRes = createPkt(f"Valor inferior ao da conta! Insira novo valor: ", nextAck) # cria pacote resposta a requisição
                        elif(valor > currentClient["contaIndividual"]):
                            currentClient["contaIndividual"] = 0
                            currentClient["estado"] = 3
                            clients[id] = currentClient
                            reqRes = createPkt(f"Valor superior. O restante será descontado da conta da mesa!\n{opcoesMsg}", nextAck) # cria pacote resposta a requisição
                        else:
                            currentClient["contaIndividual"] = 0
                            currentClient["estado"] = 3
                            clients[id] = currentClient
                            reqRes = createPkt(f"Valor recebido!\n{opcoesMsg}", nextAck) # cria pacote resposta a requisição
                        
                        currentMesa = mesas[currentClient["mesa"]]
                        currentMesa["conta"] -= valor
                        if currentMesa["conta"] < 0 :
                            currentMesa["conta"] = 0
                        mesas[currentClient["mesa"]] = currentMesa

        
        # Enviaresposta da requisição
        serverSocket.sendto(reqRes, clientAddress)
        # a função 'waitConfirmation' aguarda a confirmação da mensagem e também tenta reenviala caso tenha acontecido algum problema
        nextAck = waitConfirmation(serverSocket, nextAck)
                
    else:
        print("Erro no recebimento da mensagem")

