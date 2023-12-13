# Projeto Transformador Trifásico
**Autores**: Ian Lucas Fiaux Harfuch, Leonardo Gabriel Rosa e Pedro Miguel Odebrecht Nassif

**Data**: 13 de Dezembro, 2023

**Disciplina**: TRANSFORMADORES - 1ELE924

**Docente**: Prof. José Fernando Mangili Júnior

## Descrição
Esse projeto tem como objetivo dimensionar um transformador trifásico com os seguintes parâmetros:
- **Potência nominal: 45 kVA**
- **AT: 13,8/13,2/12,6 kV - Delta**
- **BT: 380/220 V - Estrela**
- **Frequência: 60 Hz**

## Metodologia e Estrutura
O projeto foi feito utilizando a linguagem de programação Python.
Os códigos são separados em dois módulos:
- ***equacoes_trafo.py***: Módulo que contém todas as fórmulas/equações de dimensionamento do transformador, assim como dados
de tabelas e também funções auxiliares.
  - *Obs.:* Neste módulo, também há a presença do método *obter_tabela_awg()*, responsável por ler o arquivo *TabelaAWG.csv*.
- ***projeto_trafo_trifasico.py***: Módulo que contém o algoritmo do projeto em si, cascateando os passos e cálculos necessários para realizar o dimensionamento.

Além disso, há a presença de mais dois arquivos:
- ***resultados_trafo_trifasico.log***: Arquivo que contém os resultados do dimensionamento.
- ***TabelaAWG.csv***: Arquivo que contém a tabela AWG, utilizada para dimensionar os enrolamentos.

## Execução
### Pacotes necessários
Há alguns pacotes necessários para executar esse código Python. Abaixo está uma lista desses pacotes e também o comando necessário para baixá-los:
- **Numpy**: *pip install numpy*
- **Pandas**: *pip install pandas*
- **Loguru**: *pip install loguru*
 
Com isso, é possível executar via terminal por meio do comando:
*python3 projeto_trafo_trifasico.py*