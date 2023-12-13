# --------------------------------------------------------------------------- #
# Bibliotecas
import numpy as np
import pandas as pd
import pdb

# --------------------------------------------------------------------------- #
# Representações
class Enrolamento:
    def __init__(self, Vl, ligacao):
        self.ligacao = ligacao
        self.Vl = Vl
        self.Vf = self.calcular_Vf()

    def calcular_Vf(self):
        return calcular_Vf(self.Vl, self.ligacao)

    def __str__(self):
        return f'Vl: {self.Vl}\nligacao: {self.ligacao}'

# --------------------------------------------------------------------------- #
# Auxiliar
def calcular_Vf(Vl, ligacao):
    if ligacao == 'estrela':
        return Vl / np.sqrt(3)
    elif ligacao == 'delta':
        return Vl


# --------------------------------------------------------------------------- #
# Fórmulas

# 1 - Determinação das correntes de fase de cada enrolamento
def calcular_Il(Pn, Vl):
    return Pn / (np.sqrt(3) * Vl)

def calcular_If(Il, ligacao):
    if ligacao == 'estrela':
        return Il 
    elif ligacao == 'delta':
        return Il / np.sqrt(3)

# 2 - Cálculo de espiras por bobina (para cada enrolamento, N)
def calcular_espiras_por_bobina(Pn):
    return np.sqrt(0.24 * (Pn/1000))

def calcular_numero_de_espiras(Vf, V_esp):
    return Vf / V_esp

# 3 - Cálculo da Seção Magnética do Núcleo (Smag ou Sn)
def calcular_secao_magnetica_do_nucleo(V_esp, Bn, f):
    return (V_esp * 10000) / (4.44 * Bn * f)

# -- Tabela de referência (exemplo) -- 

# 4 - Seção Geométrica do Núcleo e seu Diâmetro
def calcular_secao_geometrica_nucleo(Sn, ke):
    return Sn / ke ## Em cm2

def calcular_raio_do_nucleo(Sg):
    return np.sqrt(Sg / np.pi) # Em cm

# 5 - Escalonamento do Núcleo
def numero_de_degraus_do_nucleo(r):
    # Tabela 2
    r_mm = r * 10 # Em mm
    d = 2 * r_mm # Em mm
    if d <= 50:
        return 2
    elif 50 < d <= 70:
        return 3
    elif 70 < d  <= 100:
        return 4
    elif 100 < d <= 140:
        return 5
    elif 140 < d <= 200:
        return 6
    elif 200 < d <= 300:
        return 7
    elif 300 < d <= 400:
        return 8
    elif 400 < d <= 550:
        return 9
    else:
        return 10

def obter_kf(numero_de_degraus):
    # Tabela 3
    match numero_de_degraus:
        case 1:
            return 0.64
        case 2:
            return 0.73
        case 3:
            return 0.79
        case 4:
            return 0.82
        case 5:
            return 0.84
        case 6:
            return 0.86
        case 7:
            return 0.87
        

# 6 - Seção onde o núcleo se insere (Sg-in), considerando o fator de preenchimento (kf)
def calcular_secao_nucleo_in(Sg, kf):
    return Sg / kf

def calcular_raio_nucleo_in(Sg_in):
    return np.sqrt(Sg_in / np.pi) # Em cm

# 7 - Altura da Janela (Hj)
def calcular_altura_janela(Pn):
    return 120 * (Pn/3)**(1/4) # em mm

# 8 - Número de espiras do secundário
def calcular_numero_espiras_secundario(Vs, Bn, Sn, f):
    return (Vs * 1e4) / (4.44 * Bn * Sn * f) # espiras

# 9 - Número de espiras do primário
def calcular_numero_espiras_primario(Vp, Ns, Vs):
    return (Vp * Ns) / Vs # espiras

# 10 - Bitola (AWG) ou Seção (mm2) e Diâmetro do condutor primário
# def calcular_densidade_corrente_primario(Ip, Sp):
#     return Ip / Sp

MAPA_POTENCIA_DENSIDADE_CORRENTE = {
    5e3: 1.8,
    10e3: 2.0,
    15e3: 2.2,
    30e3: 2.5,
    45e3: 2.7,
    75e3: 3.0,
    112.5e3: 3.5,
    150e3: 3.7
}

TABELA_AWG_PATH = 'TabelaAWG.csv'
STRING_COLUMNS = ['Numero AWG']

def obter_densidade_pela_potencia(Pn):
    if Pn not in MAPA_POTENCIA_DENSIDADE_CORRENTE:
        raise ValueError(f'Potência {Pn} não encontrada na tabela.')
    return MAPA_POTENCIA_DENSIDADE_CORRENTE[Pn]

def calcular_secao_condutor_primario(Ip, Jp):
    return Ip / Jp

def calcular_diametro_condutor_primario(Sp):
    return np.sqrt((4 * Sp) / np.pi)


def obter_tabela_awg():
    df = pd.read_csv(TABELA_AWG_PATH, dtype=str)
    colunas_para_float = [coluna for coluna in df.columns if coluna not in STRING_COLUMNS]
    df[colunas_para_float] = df[colunas_para_float].astype(float)
    df[STRING_COLUMNS] = df[STRING_COLUMNS].astype(str)
    return df

def obter_diametro_condutor_awg(diametro_mm):
    tabela_awg = obter_tabela_awg()
    # Obter valor mais próximo acima
    diametro_awg = tabela_awg[tabela_awg['Diâmetro (mm)'] >= diametro_mm]['Numero AWG']
    return diametro_awg.iloc[-1]

# 11 - Bitola (AWG) ou Seção (mm2) e Diâmetro do condutor secundário
# def calcular_densidade_corrente_secundario(Is, Ss):

def calcular_secao_condutor_secundario(Is, Js): # mm2
    return Is / Js

def calcular_diametro_condutor_secundario(Ss): # mm
    return np.sqrt((4 * Ss) / np.pi)


# 12 - Dimensionamento do Secundário (bobina interna):
# Materiais isolantes: classe A (105°C)

def calcular_numero_espiras_por_camada_secundario(Hj, Hc, hs):
    return ((Hj - 2*Hc) / hs) - 1

def calcular_numero_camadas_secundario(Nebs, Necs):
    return Nebs / Necs

def calcular_espessura_radial_enrolamento_secundario(Ncs, hs, epsilons):
    return Ncs * (hs + epsilons)

# 13 - Dimensionamento do Primário (bobina externa):
def calcular_numero_espiras_por_camada_primario(Hj, Hc, hp):
    return ((Hj - 2*Hc) / hp) - 1

def calcular_numero_camadas_primario(Nebp, Necp):
    return Nebp / Necp

def calcular_espessura_radial_enrolamento_primario(Ncp, hp, epsilonp):
    return Ncp * (hp + epsilonp)

# 14 - Comprimento médio dos Enrolamentos
def calcular_diametro_interno_carretel(r_in, dn):
    return 2*(r_in*10) + 2*dn

def calcular_diametro_externo_carretel(phi_int_carr, ds):
    return phi_int_carr + 2*ds

# a- Enrolamentos do secundário
def calcular_comprimento_medio_enrolamentos_secundario_quadrado(ds, dn, a, b):
    return 4*ds + 8*dn + 2*(a+b)

def calcular_comprimento_medio_enrolamentos_secundario_circular(phi_int_carr, ds):
    return ((phi_int_carr/2)+(ds/2))*2*np.pi

# b- Enrolamentos do primário
def calcular_comprimento_medio_enrolamentos_primario_quadrado(dp, ds, do, dn, a, b):
    return 4*dp + 8*ds + 8*do + 8*dn + 2*(a+b)

def calcular_comprimento_medio_enrolamentos_primario_circular(phi_ext_sec, do, dp):
    return ((phi_ext_sec/2)+do+(dp/2))*2*np.pi

# 15 - Massa de cobre do primário:
def calcular_massa_cobre_primario(Lp, Np, Sp):
    return 8.89e-3 * (Lp/1000) * Np * Sp * 3 # kg

# 16 - Massa de cobre do secundário:
def calcular_massa_cobre_secundario(Ls, Ns, Ss):
    return 8.89e-3 * (Ls/1000) * Ns * Ss * 3 # kg

# 17 - Resistência do primário:
def calcular_resistencia_primario(Lp, Np, Sp, rho = 0.0216):
    return rho * ((Lp/1000) * Np) / Sp # ohms/fase

# a - Correção de temperatura do cobre a 75°C
def calcular_resistencia_primario_corrigida(Rp, Top = 75, Tref = 30, alpha = 3.9e-3):
    return Rp * (1 + alpha * (Top - Tref))

# 18 - Resistência do secundário:
def calcular_resistencia_secundario(Ls, Ns, Ss, rho = 0.0216):
    return rho * ((Ls/1000) * Ns) / Ss # ohms/fase

# a - Correção de temperatura do cobre a 75°C
def calcular_resistencia_secundario_corrigida(Rs, Top = 75, Tref = 30, alpha = 3.9e-3):
    return Rs * (1 + alpha * (Top - Tref)) # ohms/fase

# 19 - Perdas elétricas nos Enrolamentos (primário + secundário):
def calcular_perdas_eletricas_enrolamentos(Rp, Ip, Rs, Is, kp):
    return ((Rp * Ip**2) + (Rs * Is**2))*3 + kp # W

# 20 - Quantificação do Núcleo:
# a - Largura da janela
def calcular_largura_janela(ds, do, dp, dn, Defa):
    return 2*(ds + do + dp + 2*dn) + Defa

# 21 - Massa do núcleo:
def calcular_massa_nucleo(Sn, Hj, Lj, phi_n, rho = 7.655e-3):
    return rho * Sn * (3*(Hj/10) + 4*(Lj/10) + 6*(phi_n)) # kg

PERDAS_NO_NUCLEO = {
    15e3: 440,
    30e3: 740,
    45e3: 1000,
    75e3: 1470,
    112.5e3: 1990,
    150e3: 2450
}
# 22 - Perdas no núcleo:
def obter_perdas_nucleo(Pn):
    if Pn not in PERDAS_NO_NUCLEO:
        raise ValueError(f'Potência {Pn} não encontrada na tabela.')
    return PERDAS_NO_NUCLEO[Pn]
    


