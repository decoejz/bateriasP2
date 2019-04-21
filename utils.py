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
    def __init__(self, ddp_usuario, pot_usuario, tempo_usuario, cap_carga_usuario, limite):
        self.ddp = ddp_usuario
        self.pot = pot_usuario
        self.tempo = tempo_usuario
        self.cap_carga = cap_carga_usuario
        self.limite = limite
    
    def escolha(self,dic):
        quantP = 1
        quantS = 1
        quantT = 1
        # for item in dic:
        #     print(item["ddp"])
        #     if item["ddp"] < 3:
        #         if abs(item["ddp"] - self.ddp) < 1:
        #             quantP = paralelo(self.pot,self.tempo,item)
        #             quantS = serie(self.ddp, item)
        #             quantT = quantP*quantS
        #             return item, quantT, quantP, quantS #devolve a pilha, a quantidade total, a quantidade em paralelo e a quantidade em série
        #     else:
        #         if abs(item["ddp"] - self.ddp) <= 3:
        #             quantP = paralelo(self.pot,self.tempo,item)
        #             quantS = serie(self.ddp, item)
        #             quantT = quantP*quantS
        #             return item, quantT, quantP, quantS
        #         if self.ddp > 15:
        #             quantP = paralelo(self.pot,self.tempo,item)
        #             quantS = serie(self.ddp, item)
        #             quantT = quantP*quantS
        #             return item, quantT, quantP, quantS

        for item in dic:
            lista_preco = []
            print(dic[item], "itemmmmmmmmmmmmmmmmmmmmmm")
            quantP = paralelo(self.pot,self.tempo,dic[item])
            quantS = serie(self.ddp, dic[item])
            quantT = quantP*quantS
            preco = quantT*dic[item]["preco"]
            lista_preco.append(preco)
            minimo = min(lista_preco)
            index_min = lista_preco.index(minimo)
            print(dic[str(index_min+1)])
            print("------------------------------------------------")
        return dic[str(index_min)], quantT, quantP, quantS

def paralelo(pot_usuario,tempo_usuario,item):
    i = pot_usuario/item["ddp"]
    tempo = item["cap_carga"]/i # tempo que ficará ligada
    if tempo > tempo_usuario: # se o tempo obtido é maior que o esperado tudo OK
        quant = 1 # quantidade de pilhas
        return quant
    else: # se o tempo obtido é menor que o esperado
        quant = tempo_usuario/tempo #verifica quantas pilhas em paralelo serão necessárias
        quant = int(quant)+1 # não devolve números quebrados e sempre arredonda para cima
        return quant #devolve a quantidade de paralelos

def serie(ddp_usuario,item):
    if(item["ddp"] >= ddp_usuario):
        return 1
    else:
        quant = int(ddp_usuario/item["ddp"])+1
        return quant


