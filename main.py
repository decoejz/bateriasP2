from utils import pilha
from utils import Bateria_Escolhida
import sys
import json

def show_json(dic):
    for element in dic:
        print(element)
        print(dic[element])

def menu_principal(dic): #Seleção de material para cátodo e anôdo
        print("--------------------------------------------------------------------------------------------")
        print("Digite C para construir sua própria bateria com os materiais disponíveis.")
        print("Digite S para selecionar uma pilha comercial que sirva para o seu experimento")
        print("Depos siga as instruções para obtenção da informação desejada")
        print("--------------------------------------------------------------------------------------------")
        while(True):
            comando = input("Constrir sua própria pilha(C) ou Selecionar pilha comercial(S): ")
            if (comando == "C") or (comando == "c"):
                return 1
            elif(comando == "S") or (comando == "s"):
                return 0
            else:
                print("comando inválido escolha novamente")
                comando = input("Constrir sua própria pilha(C) ou Selecionar pilha comercial(S): ")
def etapa1(dic):
    print("\n"*100)
    print("--------------------------------------------------------------------------------------------")
    print("ETAPA 1: SELEÇÃO DE MATERIAIS PARA A PILHA")
    print("--------------------------------------------------------------------------------------------")
    print("Esta é a lista de materiais disponíveis: ")
    for element in dic:
        print(dic[element]["id"]," -> ",dic[element]["nome"])
    print("Para escolher o material você deve digitar o número que q aparece ao seu lado na lista apresentada a cima.")
    mat1_id = 100
    mat2_id = 100
    while mat1_id > 10 or mat1_id < 1:
        print("\nMETAL 1:")
        print("Não esqueça que temos apenas 10 materiais disponíveis.")
        print("O id deve ser um número entre 1 e 10")
        mat1_id = int(input("Qual o id do primeiro metal? "))
    massa_mat1 = int(input("Qual é a massa (em g) do primeiro metal? "))
    conc_sol_mat1 = int(input("Qual é a concentração da solução para primeiro metal em g/mol? "))
    while mat2_id > 10 or mat2_id < 1:
        print("\nMETAL 2:")
        print("Não esqueça que temos apenas 10 materiais disponíveis.")
        print("O id deve ser um número entre 1 e 10")
        mat2_id = int(input("Qual o id do metal do segundo metal? "))
    massa_mat2 = int(input("Qual é a massa (em g) do metal do segundo metal? "))
    conc_sol_mat2 = int(input("Qual é a concentração da solução para segundo metal em g/mol? "))
    print("\nTEMPERATURA")
    temp = int(input("Qual é a temperatura em graus celcius? "))
    print("\n"*100)
    mat1 = dic[str(mat1_id)]
    mat2 = dic[str(mat2_id)]
    bateria = pilha(mat1, mat2, massa_mat1, massa_mat2,conc_sol_mat1,conc_sol_mat2, temp)
    return bateria

def etapa2(dic2):
    print("\n"*100)
    print("--------------------------------------------------------------------------------------------")
    print("ETAPA 2: SELEÇÃO DE PILHA COMERCIAL PARA PARÂMETROS DADOS")
    print("--------------------------------------------------------------------------------------------")
    ddp_usuario = input("Qual a DDP da pilha que você precisa, em V? ")
    while (True):
        try:
            ddp_usuario = float(ddp_usuario)
            break
        except:
            ddp_usuario = input("Qual a DDP da pilha que você precisa, em V? (Coloque um número) - ")
    
    pot_usuario = input("Qual a potência da pilha que você precisa, em W? ")
    while (True):
        try:
            pot_usuario = float(pot_usuario)
            break
        except:
            pot_usuario = input("Qual a potência da pilha que você precisa, em W? (Coloque um número) - ")
    
    tempo_usuario = input("Quanto tempo a pilha precisa ficar ligada, em horas? ")
    while (True):
        try:
            tempo_usuario = float(tempo_usuario)
            break
        except:
            tempo_usuario = input("Quanto tempo a pilha precisa ficar ligada, em horas? (Coloque um número) - ")

    limite_usuario_mais = input("Caso não seja possível conseguir a ddp exata, qual o erro que poderemos aceitar para cima, em V? ")
    while (True):
        try:
            limite_usuario_mais = float(limite_usuario_mais)
            break
        except:
            limite_usuario_mais = input("Caso não seja possível conseguir a ddp exata, qual o erro que poderemos aceitar para cima, em V? (Coloque um número) - ")

    limite_usuario_menos = input("Caso não seja possível conseguir a ddp exata, qual o erro que poderemos aceitar para baixo, em V? ")
    while (True):
        try:
            limite_usuario_menos = float(limite_usuario_menos)
            break
        except:
            limite_usuario_menos = input("Caso não seja possível conseguir a ddp exata, qual o erro que poderemos aceitar para baixo, em V? (Coloque um número) - ")

    bateria_usu = Bateria_Escolhida(ddp_usuario,pot_usuario,tempo_usuario, limite_usuario_mais,limite_usuario_menos)
    # escolhida, total, em_paralelo, em_serie = bateria_usu.escolha(dic2)
    # return escolhida, total, em_paralelo, em_serie
    return (bateria_usu.escolha(dic2))


def __init__():
    sair = "0"
    with open('data.json', 'r') as fp:
        dic1 = json.load(fp)
    with open('comerciais.json', 'r') as cm:
        dic2 = json.load(cm)
    while(sair == "0"):
        resposta = menu_principal(dic1)
        if resposta == 1:
            bateria = etapa1(dic1)
            print("--------------------------------------------------------------------------------------------")
            print("A DDP dessa bateria em V será: {:.2f}".format(bateria.ddp))
            print("A Capacidade de carga dessa bateria, em mAh será: {:.2f}".format(bateria.cap_carga))
            print("A Densidade de energia dessa bateria em Wh será: {:.2f}".format(bateria.potencia))
            print("--------------------------------------------------------------------------------------------")
        if resposta == 0:
            lista_modelo, lista_preco, lista_preco_individual, lista_quantidade, lista_serie, lista_paralelo = etapa2(dic2)
            print("\n"*100)
            print("--------------------------------------------------------------------------------------------")
            counter = 4
            while (len(lista_preco) > 0):
                minimo = min(lista_preco)
                index_min = lista_preco.index(minimo)

                if (counter > 0):
                    print("Você pode usar a pilha {}".format(lista_modelo[index_min]))
                    print("Serão {0} pilhas em série, com {1} em paralelo em cada".format(lista_serie[index_min],lista_paralelo[index_min]))
                    print("Completando um total de {} pilhas".format(lista_quantidade[index_min]))
                    print("Cada pilha custa R${0:.2f}, totalizando R${1:.2f}".format(lista_preco_individual[index_min],lista_preco[index_min]))
                    print("--------------------------------------------------------------------------------------------")
                    
                    counter -= 1

                del lista_modelo[index_min]
                del lista_preco[index_min]
                del lista_preco_individual[index_min]
                del lista_quantidade[index_min]
                del lista_serie[index_min]
                del lista_paralelo[index_min]

            print("\n")



        sair = input("Para voltar para o início digite 0, para sair digite qualquer tecla: ")



__init__()