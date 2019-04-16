class pilha():
    def __init__(self,mat1,mat2,massa1,massa2):
        self.mat1 = mat1
        self.mat2 = mat2
        self.ddp = calcula_DDP(mat1,mat2)
        self.cap_carga = calcula_cap(mat1,mat2,massa1,massa2)
        self.potencia = calcula_potencia(mat1,mat2)
        self.tempo_ligado = calcula_tempo(mat1,mat2)

def calcula_DDP(mat1,mat2):
    maior = mat1.E

    if (mat2.E > maior):
        ddp = mat2.E - maior
        return ddp
    
    ddp = maior - mat2.E
    return ddp

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

    total_mol_e = (material["eletron"] * limitante * contra_mat["eletron"]) / (material["massa"])

    Ah = F * total_mol_e / 3600
    #print(Ah)
    return Ah

def calcula_potencia():
    pass

def calcula_tempo():
    pass