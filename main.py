import utils as ut
import sys
import json

def show_json(dic):
    for element in dic:
        print(element)
        print(dic[element])

def etapa1(dic): #Seleção de material para cátodo e anôdo
        print("--------------------------------------------------------------------------------------------")
        print("ETAPA 1: SELEÇÃO DE MATERIAIS PARA A PILHA")
        print("Comandos:")
        print("Show             -------------------       Mostra os metais disponíveis e suas semirreações")
        print("Selecionar       -------------------       Selecione o número correspondente ao metal")
        print("Sair")
        print("--------------------------------------------------------------------------------------------")
        while(True):
            comando = input("Digite o comando: ")
            if (comando == "Selecionar") or (comando == "selecionar"):
                mat_catodo_id = int(input("Qual o id do metal para o cátodo? "))
                massa_catodo = int(input("Qual é a massa (em g) do metal para o cátodo? "))
                mat_anodo_id = int(input("Qual o id do metal para o ânodo? "))
                massa_anodo = int(input("Qual é a massa (em g) do metal para o ânodo? "))
                mat_catodo = dic[mat_catodo_id]
                mat_anodo = dic[mat_anodo_id]
                pilha = ut.__init__(mat_catodo, mat_anodo, massa_catodo, massa_anodo)
                break
            elif (comando == "Show") or (comando == "show"):
                show_json(dic)
            elif (comando == "Sair") or (comando == "sair"):
                break        
            else:
                print("Comando não encontrado")
        
        return pilha

def etapa2(dic2, pilha): #Seleção de eletrólitos(soluções) e suas concentrações
        print("--------------------------------------------------------------------------------------------")
        print("ETAPA 2: SELEÇÃO DE SOLUÇÕES E SUAS CONCENTRAÇÕES")
        print("Comandos:")
        print("Show             -------------------       Mostra as soluções disponíveis")
        print("Selecionar       -------------------       Selecione o número correspondente à solução")
        print("Sair")
        print("--------------------------------------------------------------------------------------------")


def __init__():
    comando = 0
    while(True):
        with open('data.json', 'r') as fp:
            dic1 = json.load(fp)

        pilha = etapa1(dic1)


__init__()