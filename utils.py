from math import *

class pilha():
    def __init__(self,mat1,mat2,massa1,massa2,con_sol1,con_sol2,temp,vol1,vol2):
        self.mat1 = mat1
        self.mat2 = mat2
        self.ddp = calcula_DDP(mat1,mat2,con_sol1,con_sol2,temp)
        self.cap_carga = calcula_cap(mat1,mat2,massa1,massa2)
        self.tempo_ligado = calcula_tempo(mat1,mat2)
        self.m_total = calc_massa_total(massa1,massa2,vol1,vol2)
        self.den_carga = cal_dens_carga(self.cap_carga,self.m_total)
        self.den_ene = cal_dens_ene(self.cap_carga,self.ddp)
        self.preco = calc_preco(mat1, mat2, massa1, massa2,con_sol1,con_sol2)

#Return densidade de carga [C/g]
def cal_dens_carga(Q, m_total):
    Dq = Q / m_total
    return Dq

#Return densidade de energia [Wh]
def cal_dens_ene(Dq, V):
    De = Dq * V
    return De

#Entradas:
#massa1 [g]
#massa2 [g]
#vol1 [L]
#vol2 [L]
#Return massa total [g]
def calc_massa_total(massa1,massa2,vol1,vol2):
    #Tranforma os volumes em L para g baseado na densidade da agua
    m_total = massa1 + massa2 + (vol1 * 1000) + (vol2 * 1000)

    return m_total


def calc_preco(mat1, mat2, massa1, massa2, con_sol1,con_sol2):
    #preco da solucao: por kg por 500 ml
    #preco do metal por kg 
    preco_metais =  (mat1["precoM"]*massa1/1000)+(mat2["precoM"]*massa2/1000)
    preco_solucoes = (mat1["precoS"]* ((con_sol1/2)*mat1["Msol"])/1000) + (mat2["precoS"]* ((con_sol2/2)*mat2["Msol"])/1000)
    preco_total = preco_metais + preco_solucoes
    return preco_total

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

    massaP1 = mat2["eletrons"]*mat1["M"]
    massaP2 = mat1["eletrons"]*mat2["M"]

    razP = massaP1/massaP2
    razR = massa1/massa2
    
    if(razP < razR):
        limitante = massa2
        material = mat2
        contra_mat = mat1
    else:
        limitante = massa1
        material = mat1
        contra_mat = mat2

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

def calcula_tempo(mat1,mat2): # não parece necessário - ela apenas pede o tempo para a segunda parte
    return 1

class Bateria_Escolhida():
    def __init__(self, ddp_usuario, pot_usuario, tempo_usuario, limite_mais, limite_menos):
        self.ddp = ddp_usuario
        self.pot = pot_usuario
        self.tempo = tempo_usuario
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
            quantS = serie(self.ddp, dic[item], self.limite_mais, self.limite_menos)
        
            if (not (quantS == -1)):
                nova_tensao = quantS * dic[item]["ddp"]
                quantP = paralelo(self.pot,self.tempo,dic[item],nova_tensao)
                quantT = quantP*quantS
                preco = quantT*dic[item]["preco"]

                lista_modelo.append(dic[item]["nome"])
                lista_preco_individual.append(dic[item]["preco"])
                lista_preco.append(preco)
                lista_quantidade.append(quantT)
                lista_serie.append(quantS)
                lista_paralelo.append(quantP)
        return lista_modelo, lista_preco, lista_preco_individual, lista_quantidade, lista_serie, lista_paralelo

def paralelo(pot_usuario,tempo_usuario,item,tensao):
    # i = pot_usuario/tensao
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
        quant = ddp_usuario/item["ddp"]

        if (int(quant) < quant and quant < int(quant)+1):
            quant = int(quant)+1
        else:
            quant = int(quant)
        
        #Verifica que a tensao calculada e valida para a aplicacao do usuario
        if (quant*item["ddp"] > ddp_usuario+limite_mais):
            return -1
        return int(quant)
    #Se a tensao ja for maior do que o necessario pelo usuario,
    #essa opcao sera descartada 
    else:
        return -1