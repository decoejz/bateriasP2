class pilha():
    def __init__(self,mat1,mat2):
        self.ddp = calcula_DDP(mat1,mat2)
        self.cap_carga = calcula_cap(mat1,mat2)
        self.potencia = calcula_potencia(mat1,mat2)
        self.tempo_ligado = calcula_tempo(mat1,mat2)

def calcula_DDP(mat1,mat2):
    maior = mat1.E

    if (mat2.E > maior):
        ddp = mat2.E - maior
        return ddp
    
    ddp = maior - mat2.E
    return ddp

def calcula_cap(mat1,mat2):
    Ah = carga * (1.93 * (10**5)) / 3600
    return Ah

def calcula_potencia():
    pass

def calcula_tempo():
    pass