#Programa que cria arquivos .csv a partir de amostras da saída de um modelo baseado em agentes
# para geração de dados de entrada de demanda a ser usado em um modelo hidrológico do WEAP
# Autoria: Déborah Santos de Sousa

import numpy as np # package de manipulação de listas e matrizes
import pandas as pd # package de leitura de csv
import math # funções matemáticas
import matplotlib.pyplot as plt # Plotagem de gráficos
import statistics as sts # funções estatísticas
import csv
from itertools import chain

#Matriz original que será completada
matrix_weap = pd.read_csv('my-template-matrix.csv', sep=";", decimal=".",header=None)
matrix_weap = np.array(matrix_weap)

# Extrair listas de demanda observada de D1,D2,D3
##Oferta
matrix_oferta = np.array(pd.read_csv('oferta_urubu.csv', sep=";", decimal="."))
serie_chuva2 = matrix_oferta[:,[0,1]] # data e precipitação #26798500 #estacao ref
serie_datas = serie_chuva2[:,0]
## Demanda
matriz_carac = np.array(pd.read_csv('matriz_caract.csv',sep=";",header=None))
###Volume
matriz_demanda = np.array(pd.read_csv('volume_demanda_urubu.csv', sep=";", decimal="."))
matriz_demanda = matriz_demanda[:, 1:]  # retira colunas de datas
for i in range(len(matriz_demanda)):
    for j in range(len(matriz_demanda[0])):  # 37 columns, from 0 to 36
        if matriz_demanda[i, j] == 'None' : # filtrando dados 'None'
            matriz_demanda[i, j] = np.nan
matriz_demanda = matriz_demanda.astype(np.float)
for i in range(len(matriz_demanda)):
    for j in range(len(matriz_demanda[0])):  # 37 columns, from 0 to 36
        if matriz_demanda[i, j] == 'None' or matriz_demanda[i, j] >= 2.5e5 : # filtrando dados de volume muito alto (outliers)
            matriz_demanda[i, j] = np.nan
matriz_demanda = matriz_demanda.astype(np.float)

#organizar para WEAP - pega a matriz correspondente às colunas de D1,D2,D3
ix_D1 = [i for i, v in enumerate(matriz_carac[2, :]) if v == 'D1']
m_D1 = matriz_demanda[:, ix_D1]
ix_D2 = [i for i, v in enumerate(matriz_carac[2, :]) if v == 'D2']
m_D2 = matriz_demanda[:, ix_D2]
ix_D3 = [i for i, v in enumerate(matriz_carac[2, :]) if v == 'D3']
m_D3 = matriz_demanda[:, ix_D3]
#Lista Somas de D1,D2,D3
serie_soma_D1 = []
for i in range(len(m_D1)):
    serie_soma_D1.append(np.nansum(m_D1[i,:]))
serie_soma_D2 = []
for i in range(len(m_D2)):
    serie_soma_D2.append(np.nansum(m_D2[i,:]))
serie_soma_D3 = []
for i in range(len(m_D3)):
    serie_soma_D3.append(np.nansum(m_D3[i,:]))
#matriz com data,D1,D2,D3 somado observado, incluindo a seca

matrix_observada_gd = np.zeros((len(serie_datas),4),dtype=None)
list = 7*(np.arange(1,373).tolist())
list = np.array(list)
list = list.astype(int)
matrix_observada_gd[:,0] = list
matrix_observada_gd[:,1] = serie_soma_D1
matrix_observada_gd[:,2] = serie_soma_D2
matrix_observada_gd[:,3] = serie_soma_D3
linhas_WEAP = [i for i, v in enumerate(matrix_observada_gd[:, 0]) if v not in [61,62,124,186,279,341]] #dias que não existem nos meses fevereiro (29 e 30), 31: abril, junho, outubro e novembro
matrix_observada_weap = matrix_observada_gd[linhas_WEAP,:]
matrix_observada_weap[:,0] = 7*(np.arange(1,367).tolist())
matrix_observada_weap = matrix_observada_weap[366:,:] # a partir de 2017, assim como a matriz weap que estou usando como template
matrix_observada_weap[:, 0] = 6 * (np.arange(1, 367).tolist()) # a partir de 2017, assim como a matriz weap que estou usando como template

# Extrair listas de demanda simulada de D1,D2,D3 para os dias (dia/mês) especificados
def organiza_matriz_simulada(arquivo):
    retirada_sim1 = np.array(np.genfromtxt(arquivo,delimiter=',',dtype=float))
    retirada_sim2 = np.array(np.genfromtxt(arquivo,delimiter=',',dtype=str))
    retirada_sim3 = np.zeros((len(retirada_sim1),len(retirada_sim1[0])),dtype=object)
    retirada_sim3[:,0] = (retirada_sim1[:,0]).astype(int)
    retirada_sim3[:,1]= (retirada_sim1[:,1]).astype(int)
    retirada_sim3[:,2] = (retirada_sim2[:,2])
    retirada_sim3[:,3:] = retirada_sim1[:,3:]
    retirada_sim = retirada_sim3
    # ordenar por ciclo e por simulação
    retirada_sim = retirada_sim[np.lexsort((retirada_sim[:, 0], retirada_sim[:, 1]))]
    retirada_sim = retirada_sim[:, 3:]
    return retirada_sim

# retirada_sim0 = organiza_matriz_simulada("daily_withdrawalS0.csv")
# retirada_sim1 = organiza_matriz_simulada("daily_withdrawalS1.csv")
# retirada_sim2 = organiza_matriz_simulada("daily_withdrawalS2.csv")
# retirada_sim3 = organiza_matriz_simulada("daily_withdrawalS3.csv")
# retirada_sim4 = organiza_matriz_simulada("daily_withdrawalS4.csv")
# retirada_sim4max = organiza_matriz_simulada("daily_withdrawalS4-max.csv")
# retirada_sim4min = organiza_matriz_simulada("daily_withdrawalS4-min.csv")
# retirada_sim5 = organiza_matriz_simulada("daily_withdrawalS5.csv")
# retirada_sim6 = organiza_matriz_simulada("daily_withdrawalS6.csv")
retirada_sim7 = organiza_matriz_simulada("daily_withdrawalS7.csv")
# retirada_sim8 = organiza_matriz_simulada("daily_withdrawalS8.csv")
# retirada_sim9 = organiza_matriz_simulada("daily_withdrawalS9.csv")
# retirada_sim10 = organiza_matriz_simulada("daily_withdrawalS10.csv")
retirada_sim11 = organiza_matriz_simulada("daily_withdrawalS11.csv")
retirada_sim12 = organiza_matriz_simulada("daily_withdrawalS12.csv")
retirada_sim13 = organiza_matriz_simulada("daily_withdrawalS13.csv")
# retirada_sim14 = organiza_matriz_simulada("daily_withdrawalS14.csv")
# retirada_sim15 = organiza_matriz_simulada("daily_withdrawalS15.csv")

colunas_D1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] #16
colunas_D2 = [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34] #19
colunas_D3 = [35,36] #2

n_1amostra = 100 # quantidade de simulações para a amostra #exemplo: 10
n_amostra = 6*n_1amostra # multiplica pelo numero de anos de simulação do WEAP
n_cenarios = 4 #numero de cenários do MBA a serem analisados
my_init = 100 #número inteiro até o limite 1000 - n_amostra
my_i_range = (123*my_init) # inicio da contagem
my_f_range = (n_amostra*123) + my_i_range# final da contagem

#1
retirada_simulada = retirada_sim7 #cenário de onde vou retirar as minhas amostras # S7
matrizD1 = retirada_simulada[:,colunas_D1]
matrizD2 = retirada_simulada[:,colunas_D2]
matrizD3 = retirada_simulada[:,colunas_D3]
amostraD1 = []
amostraD2 = []
amostraD3 = []
for i in range(my_i_range,my_f_range):
    amostraD1.append(sum(matrizD1[i,:]))
    amostraD2.append(sum(matrizD2[i,:]))
    amostraD3.append(sum(matrizD3[i,:]))
#matriz com data,D1,D2,D3 somado simulado, para dias genéricos durante a seca. A cada 123 dias, uma simulação das minhas 1000
mysequence = np.arange(122,245).tolist()
my_counter = n_amostra*n_cenarios*mysequence
matrix_sim_gd = np.zeros((123*n_amostra*n_cenarios,4))
matrix_sim_gd[:,0] = my_counter
matrix_sim_gd[:73800,1] = amostraD1
matrix_sim_gd[:73800,2] = amostraD2
matrix_sim_gd[:73800,3] = amostraD3
#2
retirada_simulada = retirada_sim11 #cenário de onde vou retirar as minhas amostras # S11
matrizD1 = retirada_simulada[:,colunas_D1]
matrizD2 = retirada_simulada[:,colunas_D2]
matrizD3 = retirada_simulada[:,colunas_D3]
amostraD1 = []
amostraD2 = []
amostraD3 = []
for i in range(my_i_range,my_f_range):
    amostraD1.append(sum(matrizD1[i,:]))
    amostraD2.append(sum(matrizD2[i,:]))
    amostraD3.append(sum(matrizD3[i,:]))
#matriz com data,D1,D2,D3 somado simulado, para dias genéricos durante a seca. A cada 123 dias, uma simulação das minhas 1000
matrix_sim_gd[73800:147600,1] = amostraD1
matrix_sim_gd[73800:147600,2] = amostraD2
matrix_sim_gd[73800:147600,3] = amostraD3
#3
retirada_simulada = retirada_sim12 #cenário de onde vou retirar as minhas amostras # S12
matrizD1 = retirada_simulada[:,colunas_D1]
matrizD2 = retirada_simulada[:,colunas_D2]
matrizD3 = retirada_simulada[:,colunas_D3]
amostraD1 = []
amostraD2 = []
amostraD3 = []
for i in range(my_i_range,my_f_range):
    amostraD1.append(sum(matrizD1[i,:]))
    amostraD2.append(sum(matrizD2[i,:]))
    amostraD3.append(sum(matrizD3[i,:]))
#matriz com data,D1,D2,D3 somado simulado, para dias genéricos durante a seca. A cada 123 dias, uma simulação das minhas 1000
matrix_sim_gd[147600:221400,1] = amostraD1
matrix_sim_gd[147600:221400,2] = amostraD2
matrix_sim_gd[147600:221400,3] = amostraD3
#4
retirada_simulada = retirada_sim13 #cenário de onde vou retirar as minhas amostras # S13
matrizD1 = retirada_simulada[:,colunas_D1]
matrizD2 = retirada_simulada[:,colunas_D2]
matrizD3 = retirada_simulada[:,colunas_D3]
amostraD1 = []
amostraD2 = []
amostraD3 = []
for i in range(my_i_range,my_f_range):
    amostraD1.append(sum(matrizD1[i,:]))
    amostraD2.append(sum(matrizD2[i,:]))
    amostraD3.append(sum(matrizD3[i,:]))
#matriz com data,D1,D2,D3 somado simulado, para dias genéricos durante a seca. A cada 123 dias, uma simulação das minhas 1000
matrix_sim_gd[221400:295200,1] = amostraD1
matrix_sim_gd[221400:295200,2] = amostraD2
matrix_sim_gd[221400:295200,3] = amostraD3

#preencher o arquivo final com os dados de demanda na seca usando os dados simulados da amostra
# e com os dados de demanda fora da seca com os dados observados e salvar com um nome identificatorio
simulacao = 0 # uma das 1000 repetições, provinda da amostra
z = 0

for simulacao in range(int(len(matrix_sim_gd)/6)):
    for i in range(len(matrix_weap)):
        if matrix_weap[i,1] >= 1 and matrix_weap[i,1] < 122 or matrix_weap[i,1] > 244: # preenche coluna 2 com dados observados coluna 1
            matrix_weap[i,2] = matrix_observada_weap[i,1]
            matrix_weap[i,3] = matrix_observada_weap[i,2]
            matrix_weap[i,4] = matrix_observada_weap[i,3]
        else:
            matrix_weap[i,2] = matrix_sim_gd[z,1]
            matrix_weap[i,3] = matrix_sim_gd[z,2]
            matrix_weap[i,4] = matrix_sim_gd[z,3]
            z = z + 1
    np.savetxt('MySimulation'+str(simulacao + 1)+'.csv',matrix_weap, delimiter=';',fmt="%s",header='Data;Dia;D1(m³);D2(m³);D3(m³)')
    simulacao = simulacao + 1
