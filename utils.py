from math import *

class pilha():
    def __init__(self,mat1,mat2,massa1,massa2,con_sol1,con_sol2,temp):
        self.mat1 = mat1
        self.mat2 = mat2
        self.ddp = calcula_DDP(mat1,mat2,con_sol1,con_sol2,temp)
        self.cap_carga = calcula_cap(mat1,mat2,massa1,massa2)
        self.potencia = calcula_potencia(self,mat1,mat2)
        self.tempo_ligado = calcula_tempo(mat1,mat2)

def calcula_DDP0(mat1,mat2,con_sol1,con_sol2):
    maior = mat1["E"]

    if (mat2["E"] > maior):
        E0 = mat2["E"] - maior
        return E0, mat2, mat1, con_sol2, con_sol1
    
    E0 = maior - mat2["E"]
    return E0, mat1, mat2, con_sol1, con_sol2

def calcula_cap(mat1,mat2,massa1,massa2):
    c_eletron = 1.6021 * (10 ** (-19))
    mol = 6.0225 * (10 ** (23))
    F = c_eletron * mol

    limitante = massa1
    material = mat1
    contra_mat = mat2
    if (massa2 < limitante):
        limitante = massa2
        material = mat2
        contra_mat = mat1

    total_mol_e = (material["eletrons"] * limitante * contra_mat["eletrons"]) / (material["M"])

    Ah = F * total_mol_e / 3600
    return Ah

def calcula_DDP(mat1,mat2,con_sol1,con_sol2,temp):
    R = 8.314
    T = temp + 273.15
    F =  96485
    E0, cat, ano, con_cat, con_ano = calcula_DDP0(mat1,mat2,con_sol1, con_sol2)
    n = mat1["eletrons"]*mat2["eletrons"]
    K = (con_ano**ano["eletrons"])/(con_cat**cat["eletrons"])
    ddp = E0 - ((R*T)/(n*F))*log(K)
    return ddp

def calcula_potencia(self,mat1,mat2):
    pot = self.ddp * self.cap_carga
    return pot/1000

def calcula_tempo(mat1,mat2): # não parece necessário - ela apenas pede o tempo para a segunda parte
    return 1

class Bateria_Escolhida():
    def __init__(self, ddp_usuario, pot_usuario, tempo_usuario, cap_carga_usuario, limite_mais, limite_menos):
        self.ddp = ddp_usuario
        self.pot = pot_usuario
        self.tempo = tempo_usuario
        self.cap_carga = cap_carga_usuario
        self.limite_mais = limite_mais
        self.limite_menos = limite_menos
    
    def escolha(self,dic):
        quantP = 1
        quantS = 1
        quantT = 1

        lista_preco = []
        lista_preco_individual = []
        lista_modelo = []
        lista_quantidade = []
        lista_serie = []
        lista_paralelo = []
        for item in dic:
            quantP = paralelo(self.pot,self.tempo,dic[item])
            quantS = serie(self.ddp, dic[item], self.limite_mais, self.limite_menos)
            quantT = quantP*quantS
            preco = quantT*dic[item]["preco"]
            if (not (quantS == -1)):
                lista_modelo.append(dic[item]["nome"])
                lista_preco_individual.append(dic[item]["preco"])
                lista_preco.append(preco)
                lista_quantidade.append(quantT)
                lista_serie.append(quantP)
                lista_paralelo.append(quantS)
        return lista_modelo, lista_preco, lista_preco_individual, lista_quantidade, lista_serie, lista_paralelo

def paralelo(pot_usuario,tempo_usuario,item):
    i = pot_usuario/item["ddp"]
    tempo = item["cap_carga"]/i # tempo que ficara ligada
    if tempo > tempo_usuario: # se o tempo obtido e maior que o esperado tudo OK
        quant = 1 # quantidade de pilhas
        return quant
    else: # se o tempo obtido e menor que o esperado
        quant = tempo_usuario/tempo #verifica quantas pilhas em paralelo serao necessarias
        quant = int(quant)+1 # nao devolve números quebrados e sempre arredonda para cima
        return quant #devolve a quantidade de paralelos

def serie(ddp_usuario,item, limite_mais, limite_menos):
    #Verifica se a tensao esta dentro dos limites desejados pelo usuario
    #Caso esteja, apenas uma pilha e necessario, caso nao esteja, e calculado
    #quantas pilhas sao necessarias
    if ((ddp_usuario+limite_mais >= item["ddp"]) and (ddp_usuario-limite_menos <= item["ddp"])):
        return 1
    elif (item["ddp"] < ddp_usuario-limite_menos):
        quant = int(ddp_usuario/item["ddp"])+1
        return quant
    else:
        return -1