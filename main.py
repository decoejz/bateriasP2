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
        print("Não esqueça que temos apenas 10 materiais disponíeis.")
        print("O id deve ser um número entre 1 e 10")
        mat1_id = int(input("Qual o id do primeiro metal? "))
    massa_mat1 = int(input("Qual é a massa (em g) do primeiro metal? "))
    conc_sol_mat1 = int(input("Qual é a concentração da solução para primeiro metal em g/mol? "))
    while mat2_id > 10 or mat2_id < 1:
        print("Não esqueça que temos apenas 10 materiais disponíeis.")
        print("O id deve ser um número entre 1 e 10")
        mat2_id = int(input("Qual o id do metal do segundo metal? "))
    massa_mat2 = int(input("Qual é a massa (em g) do metal do segundo metal? "))
    conc_sol_mat2 = int(input("Qual é a concentração da solução para segundo metal em g/mol? "))
    temp = int(input("Qual é a temperatura em graus celcius? "))
    mat1 = dic[str(mat1_id)]
    mat2 = dic[str(mat2_id)]
    print(mat1)
    print(mat2)
    bateria = pilha(mat1, mat2, massa_mat1, massa_mat2,conc_sol_mat1,conc_sol_mat2, temp)
    return bateria

def etapa2(dic2):
        print("--------------------------------------------------------------------------------------------")
        print("ETAPA 2: SELEÇÃO DE PILHA COMERCIAL PARA PARÂMETROS DADOS")
        print("--------------------------------------------------------------------------------------------")
        ddp_usuario = int(input("Qual a DDP da pilha que você precisa, em V? "))
        pot_usuario = int(input("Qual a potência da pilha que você precisa, em W/h? "))
        tempo_usuario = int(input("Quanto tempo a pilha precisa ficar ligada, em horas? "))
        cap_carga_usuario = int(input("Qual a capacidade de carga da pilha que você precisa, em Ah? "))
        limite_usuario = int(input("Caso não seja possível conseguir a ddp exata, qual o erro que poderemos aceitar, em V? "))
        
        bateria_usu = Bateria_Escolhida(ddp_usuario,pot_usuario,tempo_usuario,cap_carga_usuario, limite_usuario)
        escolhida, total, em_paralelo, em_serie = bateria_usu.escolha(dic2)
        return escolhida, total, em_paralelo, em_serie


def __init__():
    sair = 0
    with open('data.json', 'r') as fp:
        dic1 = json.load(fp)
    with open('comerciais.json', 'r') as cm:
        dic2 = json.load(cm)
    while(sair == 0):
        resposta = menu_principal(dic1)
        if resposta == 1:
            bateria = etapa1(dic1)
            print("--------------------------------------------------------------------------------------------")
            print("A DDP dessa bateria em V será:")
            print(bateria.ddp)
            print("A Capacidade de carga dessa bateria, em mAh será:")
            print(bateria.cap_carga)
            print("A Potência dessa bateria em W/h será:")
            print(bateria.potencia)
            print("--------------------------------------------------------------------------------------------")
        if resposta == 0:
            bateria, total, em_paralelo, em_serie = etapa2(dic2)
            print(bateria)
            print("--------------------------------------------------------------------------------------------")
            print("Você pode usar a pilha", bateria["nome"])
            print("serão",em_serie," pilhas em série repetidas ",em_paralelo," vezes em paralelo")
            print("Completando um total de ",total," pilhas")
            print("cada pilha custa ",bateria["preco"]," reais, então você gastará ",bateria["preco"]*total," reais no total")
            print("--------------------------------------------------------------------------------------------")
        
        sair = int(input("Para sair digite 1, para voltar para o início digite 0: "))



__init__()