# --------------------------------------------------------------------------- #
# Imports
import equacoes_trafo as eq
import numpy as np
import pandas as pd
from loguru import logger
import sys
import pdb

# --------------------------------------------------------------------------- #
# Configurações
def config_logger():
    logger.remove()
    logger.add(sys.stdout, colorize=True, format="> <level>{message}</level>")
    new_level = logger.level("Title", no=38, color="<green>")
    logger.add("resultados_trafo_trifasico.log", colorize=True, format="<level>{message}</level>")


# --------------------------------------------------------------------------- #
# Dados do transformador

Pn = 45e3 # Potência nominal do transformador em VA
f = 60 # Frequência da rede elétrica em Hz
Vat_list = [13.8e3, 13.2e3, 12.6e3] #delta
Vbt_map = {
    "Vf": 220,
    "Vl": 380
} #estrela 

Bn = np.mean([1.2, 1.7]) # Densidade de fluxo no núcleo em Gauss
ke = 0.95 # Fator de empilhamento do núcleo

# --------------------------------------------------------------------------- #
# Funções auxiliares

# --------------------------------------------------------------------------- #
# Cálculos

if __name__ == '__main__':
    config_logger()
    
    # 1 - Determinação das correntes de fase de cada enrolamento
    logger.log('Title', '1 - Determinação das correntes de fase de cada enrolamento')
    At = eq.Enrolamento(max(Vat_list), 'delta')
    Bt = eq.Enrolamento(Vbt_map['Vl'], 'estrela')

    Il_at = eq.calcular_Il(Pn, At.Vl)
    logger.info(f'Il_at: {Il_at:.3f} A')
    Il_bt = eq.calcular_Il(Pn, Bt.Vl)
    logger.info(f'Il_bt: {Il_bt:.3f} A')

    If_at = eq.calcular_If(Il_at, At.ligacao)
    logger.info(f'If_at: {If_at:.3f} A')
    If_bt = eq.calcular_If(Il_bt, Bt.ligacao)
    logger.info(f'If_bt: {If_bt:.3f} A')

    # 2 - Cálculo de espiras por bobina (para cada enrolamento, N)
    logger.log('Title', '2 - Cálculo de espiras por bobina (para cada enrolamento, N)')
    V_esp = eq.calcular_espiras_por_bobina(Pn)
    logger.info(f'Número de espiras por bobina: {V_esp:.3f}')

    N_at = eq.calcular_numero_de_espiras(At.Vf, V_esp)
    logger.info(f'Número de espiras do enrolamento A-T: {N_at:.3f}')

    N_bt = eq.calcular_numero_de_espiras(Bt.Vl, V_esp)
    logger.info(f'Número de espiras do enrolamento B-T: {N_bt:.3f}')

    # 3 - Cálculo da Seção Magnética do Núcleo (Smag ou Sn)
    logger.log('Title', '3 - Cálculo da Seção Magnética do Núcleo (Smag ou Sn)')
    Sn = eq.calcular_secao_magnetica_do_nucleo(V_esp, Bn, f)
    # rn = eq.calcular_raio_do_nucleo(Sn)
    logger.info(f'Seção magnética do núcleo: {Sn:.3f} cm2')

    # 4 - Seção Geométrica do Núcleo e seu Diâmetro
    logger.log('Title', '4 - Seção Geométrica do Núcleo e seu Diâmetro')
    Sg = eq.calcular_secao_geometrica_nucleo(Sn, ke)
    rg = eq.calcular_raio_do_nucleo(Sg)
    logger.info(f'Seção geométrica do núcleo: {Sg:.3f} cm2, raio geométrico do núcleo: {rg:.3f} cm')

    # 5 - Escalonamento do Núcleo
    logger.log('Title', '5 - Escalonamento do Núcleo')
    numero_de_degraus = eq.numero_de_degraus_do_nucleo(rg) 
    kf = eq.obter_kf(numero_de_degraus)
    logger.info(f'Número de degraus do núcleo: {numero_de_degraus:.3f}, fator de preenchimento: {kf:.3f}')

    # 6 - Seção onde o núcleo se insere (Sg-in), considerando o fator de preenchimento (kf)
    logger.log('Title', '6 - Seção onde o núcleo se insere (Sg-in), considerando o fator de preenchimento (kf)')
    Sg_in = eq.calcular_secao_nucleo_in(Sg, kf)
    r_in = eq.calcular_raio_nucleo_in(Sg_in)
    logger.info(f'Seção onde o núcleo se insere: {Sg_in:.4f} cm2, raio mínimo do carretel: {r_in:.3f}')

    # 7 - Altura da Janela
    logger.log('Title', '7 - Altura da Janela')
    Hj = eq.calcular_altura_janela(Pn)
    logger.info(f'Altura da janela: {Hj:.3f} mm')

    Vs = Bt.Vl
    
    # 8 - Número de espiras do secundário
    logger.log('Title', '8 - Número de espiras do secundário')
    Ns = eq.calcular_numero_espiras_secundario(Vs, Bn, Sn, f)
    logger.info(f'Número de espiras do secundário: {Ns:.3f}')

    Vp = At.Vl

    # 9 - Número de espiras do primário
    logger.log('Title', '9 - Número de espiras do primário')
    Np = eq.calcular_numero_espiras_primario(Vp = Vp, Vs = Vs, Ns = Ns)
    logger.info(f'Número de espiras do primário: {Np:.3f}')

    # 10 - Bitola (AWG) ou Seção (mm2) e Diâmetro do condutor primário
    logger.log('Title', '10 - Bitola (AWG) ou Seção (mm2) e Diâmetro do condutor primário')
    Ip = If_at
    # logger.warning(f'Ip = Il_at no momento')
    Jp = eq.obter_densidade_pela_potencia(Pn)
    Sp = eq.calcular_secao_condutor_primario(Ip=Ip, Jp=Jp)
    hp = eq.calcular_diametro_condutor_primario(Sp)
    awg_p = eq.obter_diametro_condutor_awg(hp)
    logger.info(f'Bitola do condutor primário: {awg_p} AWG, seção do condutor primário: {Sp:.3f} mm2, diâmetro do condutor primário: {hp:.3f} mm')

    # 11 - Bitola (AWG) ou Seção (mm2) e Diâmetro do condutor secundário
    logger.log('Title', '11 - Bitola (AWG) ou Seção (mm2) e Diâmetro do condutor secundário')
    Is = Il_bt #ATENCAO ----------------------
    # logger.warning(f'Is = Il_bt no momento')
    Js = eq.obter_densidade_pela_potencia(Pn)
    Ss = eq.calcular_secao_condutor_secundario(Is=Is, Js=Js)
    hs = eq.calcular_diametro_condutor_secundario(Ss)
    awg_s = eq.obter_diametro_condutor_awg(hs)
    logger.info(f'Bitola do condutor secundário: {awg_s} AWG, seção do condutor secundário: {Ss:.3f} mm2, diâmetro do condutor secundário: {hs:.3f} mm')

    # 12 - Dimensionamento do Secundário (bobina interna)
    logger.log('Title', '12 - Dimensionamento do Secundário (bobina interna)')
    Nebs = Ns
    Hc = 10 # mm
    Necs = eq.calcular_numero_espiras_por_camada_secundario(Hj, Hc, hs)
    logger.info(f'Número de espiras por camada do secundário: {Necs:.3f}')
    Ncs = eq.calcular_numero_camadas_secundario(Nebs, Necs)
    logger.info(f'Número de camadas do secundário: {Ncs:.3f}')
    epsilons = 0.20 #mm
    ds = eq.calcular_espessura_radial_enrolamento_secundario(Ncs, hs, epsilons)
    logger.info(f'Espessura radial do secundário: {ds:.3f} mm')
    
    # 13 - Dimensionamento do Primário (bobina externa)
    logger.log('Title', '13 - Dimensionamento do Primário (bobina externa)')
    Nebp = Np
    Necp = eq.calcular_numero_espiras_por_camada_primario(Hj, Hc, hp)
    logger.info(f'Número de espiras por camada do primário: {Necp:.3f}')
    Ncp = eq.calcular_numero_camadas_primario(Nebp, Necp)
    logger.info(f'Número de camadas do primário: {Ncp:.3f}')
    epsilonp = 0.20 # mm
    dp = eq.calcular_espessura_radial_enrolamento_primario(Ncp, hp, epsilonp)
    logger.info(f'Espessura radial do primário: {dp:.3f} mm')

    # 14 - Comprimento médio dos enrolamentos
    logger.log('Title', '14 - Comprimento médio dos enrolamentos')
    dn = 0.5 # mm
    logger.info(f'Distância do diâmetro do\
    núcleo ao diâmetro interno do enrolamento secundário {dn:.3f} mm')
    # 14.a - Enrolamentos do secundário
    logger.log('Title', '14.a - Enrolamentos do secundário')
    # Carretel circular
    phi_int_carr = eq.calcular_diametro_interno_carretel(r_in, dn)
    Ls = eq.calcular_comprimento_medio_enrolamentos_secundario_circular(phi_int_carr, ds)
    logger.info(f'Comprimento médio dos enrolamentos do secundário: {Ls:.3f} mm')

    # 14.b - Enrolamentos do primário
    logger.log('Title', '14.b - Enrolamentos do primário')
    do = 16 # mm
    logger.info(f'Distância entre os enrolamentos: {do:.3f} mm')
    # Carretel circular
    phi_ext_sec = eq.calcular_diametro_externo_carretel(phi_int_carr, ds)
    Lp = eq.calcular_comprimento_medio_enrolamentos_primario_circular(phi_ext_sec, do, dp)
    logger.info(f'Comprimento médio dos enrolamentos do primário: {Lp:.3f} mm')

    # 15 - Massa de cobre do primário
    logger.log('Title', '15 - Massa de cobre do primário')
    Mp = eq.calcular_massa_cobre_primario(Lp, Np, Sp)
    logger.info(f'Massa de cobre do primário: {Mp:.3f} kg')

    # 16 - Massa de cobre do secundário
    logger.log('Title', '16 - Massa de cobre do secundário')
    Ms = eq.calcular_massa_cobre_secundario(Ls, Ns, Ss)
    logger.info(f'Massa de cobre do secundário: {Ms:.3f} kg')

    # 17 - Resistência do primário
    logger.log('Title', '17 - Resistência do primário')
    Rp = eq.calcular_resistencia_primario(Lp, Np, Sp)
    Rp_corr = eq.calcular_resistencia_primario_corrigida(Rp, Top = 75, Tref = 30)
    logger.info(f'Resistência do primário corrigida: {Rp_corr:.3f} ohms/fase')

    # 18 - Resistência do secundário
    logger.log('Title', '18 - Resistência do secundário')
    Rs = eq.calcular_resistencia_secundario(Ls, Ns, Ss)
    Rs_corr = eq.calcular_resistencia_secundario_corrigida(Rs, Top = 75, Tref = 30)
    logger.info(f'Resistência do secundário corrigida: {Rs_corr:.3f} ohms/fase')

    # 19 - Perdas elétricas nos enrolamentos (primário + secundário)
    logger.log('Title', '19 - Perdas elétricas nos enrolamentos (primário + secundário)')
    kp = 0.05 # Pior caso
    logger.info(f'Perda suplementar: {kp:.3f}')
    We = eq.calcular_perdas_eletricas_enrolamentos(Rp_corr, Ip, Rs_corr, Is, kp) 
    logger.info(f'Perdas elétricas nos enrolamentos: {We:.3f} W')

    # 20 - Quantificação do Núcleo
    logger.log('Title', '20 - Quantificação do Núcleo')
    # 20.a - Largura da Janela
    Defa = 10 # mm
    logger.info(f'Distância entre fases: {Defa:.3f} mm')
    Lj = eq.calcular_largura_janela(ds, do, dp, dn, Defa)
    logger.info(f'Largura da janela: {Lj:.3f} mm')

    # 21 - Massa do núcleo
    logger.log('Title', '21 - Massa do núcleo')
    Mn = eq.calcular_massa_nucleo(Sn=Sn, Hj=Hj, Lj=Lj, phi_n=2*r_in)
    logger.info(f'Massa do núcleo: {Mn:.3f} kg')

    # 22 - Perdas no núcleo
    logger.log('Title', '22 - Perdas no núcleo')
    Wn = eq.obter_perdas_nucleo(Pn)
    logger.info(f'Perdas no núcleo: {Wn:.3f} W')







# V_esp = 2.68

