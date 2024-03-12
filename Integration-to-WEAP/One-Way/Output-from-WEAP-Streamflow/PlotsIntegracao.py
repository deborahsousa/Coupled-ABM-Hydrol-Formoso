#Programa que plota gráficos a partir de um arquivo .csv contendo os dados de saída de um modelo hidrológico do WEAP
# Autoria: Déborah Santos de Sousa

import numpy as np # package de manipulação de listas e matrizes
import pandas as pd # package de leitura de csv
import math # funções matemáticas
import matplotlib.pyplot as plt # Plotagem de gráficos
import statistics as sts # funções estatísticas
import csv
from itertools import chain

# parâmetros iniciais de cada cenário (1, 2, 3, 4)
# n_sim1 = 30 # número de simulações utilizadas para um gráfico (um cenário do MBA)
# n_sim2 = 30
# n_sim3 = 30
# n_sim4 = 30

n_dias = 1096
n_sim1 = 100 # número de simulações utilizadas para um gráfico (um cenário do MBA)
n_sim2 = 100
n_sim3 = 100
n_sim4 = 100
sub_matriz1 = np.zeros((n_dias, n_sim1)).astype(float) # matriz a ser preenchida com os resultados de cada cenário
sub_matriz2 = np.zeros((n_dias, n_sim2)).astype(float)
sub_matriz3 = np.zeros((n_dias, n_sim3)).astype(float)
sub_matriz4 = np.zeros((n_dias, n_sim4)).astype(float)

# definindo vetor de datas
w = 0
matrix_weap_ex = np.array(pd.read_csv('MySimulation1output.csv', header=None, sep=';', decimal=".",skiprows=[0, 1, 2, 3]))
datas = matrix_weap_ex[:, 0]

#Organizando as matrizes de entrada
#Cenário Sc1 do paper
for simulacao in range(1,n_sim1+1):
    my_file = 'MySimulation' + str(simulacao)+'output.csv'
    matrix_weap = np.array(pd.read_csv(my_file, header=None, sep=';',decimal=".", skiprows=[0,1,2,3]))
    vazao_sim1 = matrix_weap[:,1]
    w = 0
    for k in range(n_dias):
        sub_matriz1[k, simulacao - 1] = vazao_sim1[w]  # .astype(float) # linhas como dias, colunas como simulação
        w = w + 1
# Cenário Sc2 do paper
for simulacao in range(100,100+n_sim2):
    my_file = 'MySimulation'+str(simulacao + 1)+'output.csv'
    matrix_weap2 = np.array(pd.read_csv(my_file, header=None, sep=';',decimal=".", skiprows=[0,1,2,3]))
    vazao_sim2 = matrix_weap2[:,1]
    w = 0
    for k in range(n_dias):
        sub_matriz2[k, simulacao - 100] = vazao_sim2[w]  # .astype(float) # linhas como dias, colunas como simulação
        w = w + 1
# Cenário Sc3 do paper
for simulacao in range(200,200+n_sim3):
    my_file = 'MySimulation'+str(simulacao + 1)+'output.csv'
    matrix_weap3 = np.array(pd.read_csv(my_file, header=None, sep=';',decimal=".", skiprows=[0,1,2,3]))
    vazao_sim3 = matrix_weap3[:,1]
    w = 0
    for k in range(n_dias):
        sub_matriz3[k, simulacao - 200] = vazao_sim3[w]  # .astype(float) # linhas como dias, colunas como simulação
        w = w + 1
# Cenário Sc4 do paper
for simulacao in range(300,300+n_sim4):
    my_file = 'MySimulation'+str(simulacao + 1)+'output.csv'
    matrix_weap4 = np.array(pd.read_csv(my_file, header=None, sep=';',decimal=".", skiprows=[0,1,2,3]))
    if (simulacao + 1)  < 331:
        vazao_sim4 = matrix_weap4[:,1]
        w = 0
        for k in range(n_dias):
            sub_matriz4[k, simulacao - 300] = vazao_sim4[w]  # .astype(float) # linhas como dias, colunas como simulação
            w = w + 1
    else:
        vazao_sim4 = matrix_weap4[:, 18]
        w = 0
        for k in range(n_dias):
            sub_matriz4[k, simulacao - 300] = vazao_sim4[w]  # .astype(float) # linhas como dias, colunas como simulação
            w = w + 1

#parâmetros dos gráficos
lw = 0.15 # largura da linha
lw_m = 0.3 # largura da linha média
ls = '-' # estilo da linha
l90 = 'dotted'
lrem = 'dashdot'
ms = None # estilo do marcador
q90 = 1.245 # vazão de referência (Volken et al (2022), IAC apresentação)
rem = 0.25*q90 # vazão remanescente (Volken et al (2022))
min1 = np.min(sub_matriz1)
max1 = np.max(sub_matriz1)
min2 = np.min(sub_matriz2)
max2 = np.max(sub_matriz2)
min3 = np.min(sub_matriz3)
max3 = np.max(sub_matriz3)
max4 = np.max(sub_matriz4)
min_y = 0 # valor mínimo do eixo y
max_y = max(max1,max2,max3,max4) # valor máximo do eixo y
# mycolors = ['lightgrey','darkgray','dimgray','black']
# myscenarios = ['Sc1','Sc2','Sc3','Sc4']
# my_ylabel = "Daily simulated streamflow (m³/s)"
# mymonths= ['May','June','July','August']
mycolors = ['green','coral','darkkhaki','khaki']
my_ylabel = "Vazão diária simulada (m³/s)"
myscenarios = ['S7','S11','S12','S13']
mymonths= ['Maio','Junho','Julho','Agosto']

# Gráficos seca
# datas de seca em cada ano
#2018
i_18 = ([i for i, v in enumerate(datas) if   v == "01/07/2018"])[0]
f_18 = ([i for i, v in enumerate(datas) if   v == "31/08/2018"])[0] + 1
#2019
i_19 = ([i for i, v in enumerate(datas) if   v == "01/05/2019"])[0]
f_19 = ([i for i, v in enumerate(datas) if   v == "31/08/2019"])[0] + 1
#2020
i_20 = ([i for i, v in enumerate(datas) if   v == "01/05/2020"])[0]
f_20 = ([i for i, v in enumerate(datas) if   v == "31/08/2020"])[0] + 1
#2021
i_21 = ([i for i, v in enumerate(datas) if   v == "01/05/2021"])[0]
f_21 = ([i for i, v in enumerate(datas) if   v == "30/06/2021"])[0] + 1

# datas de cada mês de seca
#maio
# i_5_18 = [i for i, v in enumerate(datas) if   v == "01/05/2018"]
# f_5_18 = [i for i, v in enumerate(datas) if   v == "31/05/2018"]
i_5_19 = ([i for i, v in enumerate(datas) if   v == "01/05/2019"])[0]
f_5_19 = ([i for i, v in enumerate(datas) if   v == "30/05/2019"])[0] + 1
i_5_20 = ([i for i, v in enumerate(datas) if   v == "01/05/2020"])[0]
f_5_20 = ([i for i, v in enumerate(datas) if   v == "31/05/2020"])[0] + 1
i_5_21 = ([i for i, v in enumerate(datas) if   v == "01/05/2021"])[0]
f_5_21 = ([i for i, v in enumerate(datas) if   v == "31/05/2021"])[0] + 1
#junho
# i_6_18 = [i for i, v in enumerate(datas) if   v == "01/06/2018"]
# f_6_18 = [i for i, v in enumerate(datas) if   v == "30/06/2018"]
i_6_19 = ([i for i, v in enumerate(datas) if   v == "01/06/2019"])[0]
f_6_19 = ([i for i, v in enumerate(datas) if   v == "30/06/2019"])[0] + 1
i_6_20 = ([i for i, v in enumerate(datas) if   v == "01/06/2020"])[0]
f_6_20 = ([i for i, v in enumerate(datas) if   v == "30/06/2020"])[0] + 1
i_6_21 = ([i for i, v in enumerate(datas) if   v == "01/06/2021"])[0]
f_6_21 = ([i for i, v in enumerate(datas) if   v == "30/06/2021"])[0] + 1
#julho
i_7_18 = ([i for i, v in enumerate(datas) if   v == "01/07/2018"])[0]
f_7_18 = ([i for i, v in enumerate(datas) if   v == "31/07/2018"])[0] + 1
i_7_19 = ([i for i, v in enumerate(datas) if   v == "01/07/2019"])[0]
f_7_19 = ([i for i, v in enumerate(datas) if   v == "31/07/2019"])[0] + 1
i_7_20 = ([i for i, v in enumerate(datas) if   v == "01/07/2020"])[0]
f_7_20 = ([i for i, v in enumerate(datas) if   v == "31/07/2020"])[0] + 1
# i_7_21 = [i for i, v in enumerate(datas) if   v == "01/07/2021"]
# f_7_21 = [i for i, v in enumerate(datas) if   v == "31/07/2021"]
#agosto
i_8_18 = ([i for i, v in enumerate(datas) if   v == "01/08/2018"])[0]
f_8_18 = ([i for i, v in enumerate(datas) if   v == "31/08/2018"])[0] + 1
i_8_19 = ([i for i, v in enumerate(datas) if   v == "01/08/2019"])[0]
f_8_19 = ([i for i, v in enumerate(datas) if   v == "30/08/2019"])[0] + 1
i_8_20 = ([i for i, v in enumerate(datas) if   v == "01/08/2020"])[0]
f_8_20 = ([i for i, v in enumerate(datas) if   v == "31/08/2020"])[0] + 1
# i_8_21 = [i for i, v in enumerate(datas) if   v == "01/08/2021"]
# f_8_21 = [i for i, v in enumerate(datas) if   v == "31/08/2021"]

datas18 = datas[i_18:f_18]
datas19 = datas[i_19:f_19]
datas20 = datas[i_20:f_20]
datas21 = datas[i_21:f_21]
secas_datas = np.concatenate((datas18,datas19,datas20,datas21))

datas_5 = np.concatenate((datas[i_5_19:f_5_19],datas[i_5_20:f_5_20],datas[i_5_21:f_5_21]))
datas_6 = np.concatenate((datas[i_6_19:f_6_19],datas[i_6_20:f_6_20],datas[i_6_21:f_6_21]))
datas_7 = np.concatenate((datas[i_7_18:f_7_18],datas[i_7_19:f_7_19],datas[i_7_20:f_7_20]))
datas_8 = np.concatenate((datas[i_8_18:f_8_18],datas[i_8_19:f_8_19],datas[i_8_20:f_8_20]))

#Sc1
#periodos de seca em cada ano
sub_matriz = sub_matriz1
seca_18 = sub_matriz[i_18:f_18,:]
seca_19 = sub_matriz[i_19:f_19,:]
seca_20 = sub_matriz[i_20:f_20,:]
seca_21 = sub_matriz[i_21:f_21,:]

# seca mensal
secas_5 = np.concatenate((sub_matriz[i_5_19:f_5_19],sub_matriz[i_5_20:f_5_20],sub_matriz[i_5_21:f_5_21]))
secas_5_1 = secas_5.flatten()
secas_6 = np.concatenate((sub_matriz[i_6_19:f_6_19],sub_matriz[i_6_20:f_6_20],sub_matriz[i_6_21:f_6_21]))
secas_6_1 = secas_6.flatten()
secas_7 = np.concatenate((sub_matriz[i_7_18:f_7_18],sub_matriz[i_7_19:f_7_19],sub_matriz[i_7_20:f_7_20]))
secas_7_1 = secas_7.flatten()
secas_8 = np.concatenate((sub_matriz[i_8_18:f_8_18],sub_matriz[i_8_19:f_8_19],sub_matriz[i_8_20:f_8_20]))
secas_8_1 = secas_8.flatten()

# avg18 = [] # vetor com as médias diárias das repetições
# for i in range(len(datas18)):
#     avg18.append(sts.mean(seca_18[i, :]))
# avg19 = []
# for i in range(len(datas19)):
#     avg19.append(sts.mean(seca_19[i, :]))
# avg20 = []
# for i in range(len(datas20)):
#     avg20.append(sts.mean(seca_20[i, :]))
# avg21 = []
# for i in range(len(datas21)):
#     avg21.append(sts.mean(seca_21[i, :]))

secas = np.zeros((len(secas_datas),n_sim1))
secas = np.concatenate((seca_18,seca_19,seca_20,seca_21))
color = 'darkgrey'
for j in range(n_sim1):
    plt.plot(datas18, seca_18[:, j], linestyle=ls, color=color, linewidth=lw, marker=ms, label=myscenarios[0])
    plt.plot(datas19, seca_19[:, j], linestyle=ls, color=color, linewidth=lw, marker=ms)
    plt.plot(datas20, seca_20[:, j], linestyle=ls, color=color, linewidth=lw, marker=ms)
    plt.plot(datas21, seca_21[:, j], linestyle=ls, color=color, linewidth=lw, marker=ms)
plt.xticks(["01/07/2018","01/05/2019", "01/07/2019","01/05/2020","01/07/2020","01/05/2021","30/06/2021"])
plt.ylabel(my_ylabel)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.gcf().autofmt_xdate()
plt.axhline(y=q90, color='darkblue', linestyle=l90, linewidth=0.5, label=r'$Q_{90}$')
plt.axhline(y=rem, color='darkred', linestyle=lrem, linewidth=0.5, label='25% ' + r'$Q_{90}$')
plt.ylim(min_y+0.1,max_y)
plt.yscale('log')
plt.savefig('integração seca'+myscenarios[0]+'log .jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

for j in range(n_sim1):
    plt.plot(datas, sub_matriz1[:, j], linestyle=ls, color=color,linewidth=lw,marker=ms,label=myscenarios[0])
plt.xticks(["01/07/2018","31/08/2018","01/05/2019", "31/08/2019","01/05/2020","31/08/2020","01/05/2021","30/06/2021"])
plt.ylabel(my_ylabel)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.gcf().autofmt_xdate()
plt.axhline(y=q90, color='darkblue', linestyle=l90, linewidth=0.5, label=r'$Q_{90}$')
plt.axhline(y=rem, color='darkred', linestyle=lrem, linewidth=0.5, label='25% ' + r'$Q_{90}$')
plt.ylim(min_y+0.1,max_y)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.yscale('log')
plt.savefig('integração total'+myscenarios[0]+'log.jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

for j in range(n_sim1):
    plt.plot(datas, sub_matriz1[:, j], linestyle=ls, color=color,linewidth=lw,marker=ms,label=myscenarios[0])
plt.xticks(["01/07/2018","31/08/2018","01/05/2019", "31/08/2019","01/05/2020","31/08/2020","01/05/2021","30/06/2021"])
plt.ylabel(my_ylabel)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.gcf().autofmt_xdate()
plt.axhline(y=q90, color='darkblue', linestyle=l90, linewidth=0.5, label=r'$Q_{90}$')
plt.axhline(y=rem, color='darkred', linestyle=lrem, linewidth=0.5, label='25% ' + r'$Q_{90}$')
plt.ylim((0,1.05*max_y))
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.savefig('integração total'+myscenarios[0]+'linear.jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

# print('max S7',np.max(sub_matriz1))
# print('min S7',np.min(sub_matriz1))

#Sc2
#periodos de seca em cada ano
sub_matriz = sub_matriz2
seca_18 = sub_matriz[i_18:f_18,:]
seca_19 = sub_matriz[i_19:f_19,:]
seca_20 = sub_matriz[i_20:f_20,:]
seca_21 = sub_matriz[i_21:f_21,:]

# seca mensal
secas_5 = np.concatenate((sub_matriz[i_5_19:f_5_19],sub_matriz[i_5_20:f_5_20],sub_matriz[i_5_21:f_5_21]))
secas_5_2 = secas_5.flatten()
secas_6 = np.concatenate((sub_matriz[i_6_19:f_6_19],sub_matriz[i_6_20:f_6_20],sub_matriz[i_6_21:f_6_21]))
secas_6_2 = secas_6.flatten()
secas_7 = np.concatenate((sub_matriz[i_7_18:f_7_18],sub_matriz[i_7_19:f_7_19],sub_matriz[i_7_20:f_7_20]))
secas_7_2 = secas_7.flatten()
secas_8 = np.concatenate((sub_matriz[i_8_18:f_8_18],sub_matriz[i_8_19:f_8_19],sub_matriz[i_8_20:f_8_20]))
secas_8_2 = secas_8.flatten()

# concatenado total seca
secas = np.zeros((len(secas_datas),n_sim2))
secas = np.concatenate((seca_18,seca_19,seca_20,seca_21))
#color = mycolors[1]
for j in range(n_sim2):
    plt.plot(datas18, seca_18[:, j], linestyle=ls, color=color,linewidth=lw,marker=ms,label=myscenarios[1])
    plt.plot(datas19, seca_19[:, j], linestyle=ls, color=color, linewidth=lw, marker=ms)
    plt.plot(datas20, seca_20[:, j], linestyle=ls, color=color, linewidth=lw, marker=ms)
    plt.plot(datas21, seca_21[:, j], linestyle=ls, color=color, linewidth=lw, marker=ms)
plt.xticks(["01/07/2018","01/05/2019", "01/07/2019","01/05/2020","01/07/2020","01/05/2021","30/06/2021"])
plt.ylabel(my_ylabel)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.gcf().autofmt_xdate()
plt.axhline(y=q90, color='darkblue', linestyle=l90, linewidth=0.5, label=r'$Q_{90}$')
plt.axhline(y=rem, color='darkred', linestyle=lrem, linewidth=0.5, label='25% ' + r'$Q_{90}$')
plt.ylim(min_y+0.1,max_y)
plt.yscale('log')
plt.savefig('integração seca'+myscenarios[1]+'log .jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

for j in range(n_sim2):
    plt.plot(datas, sub_matriz2[:, j], linestyle=ls, color=color,linewidth=lw,marker=ms,label=myscenarios[1])
plt.xticks(["01/07/2018","31/08/2018","01/05/2019", "31/08/2019","01/05/2020","31/08/2020","01/05/2021","30/06/2021"])
plt.ylabel(my_ylabel)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.gcf().autofmt_xdate()
plt.axhline(y=q90, color='darkblue', linestyle=l90, linewidth=0.5, label=r'$Q_{90}$')
plt.axhline(y=rem, color='darkred', linestyle=lrem, linewidth=0.5, label='25% ' + r'$Q_{90}$')
plt.ylim(min_y+0.1,max_y)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.yscale('log')
plt.savefig('integração total'+myscenarios[1]+'log.jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

for j in range(n_sim2):
    plt.plot(datas, sub_matriz2[:, j], linestyle=ls, color=color,linewidth=lw,marker=ms,label=myscenarios[1])
plt.xticks(["01/07/2018","31/08/2018","01/05/2019", "31/08/2019","01/05/2020","31/08/2020","01/05/2021","30/06/2021"])
plt.ylabel(my_ylabel)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.gcf().autofmt_xdate()
plt.axhline(y=q90, color='darkblue', linestyle=l90, linewidth=0.5, label=r'$Q_{90}$')
plt.axhline(y=rem, color='darkred', linestyle=lrem, linewidth=0.5, label='25% ' + r'$Q_{90}$')
plt.ylim((0,1.05*max_y))
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.savefig('integração total'+myscenarios[1]+'linear.jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

#Sc3
#periodos de seca em cada ano
sub_matriz = sub_matriz3
seca_18 = sub_matriz[i_18:f_18,:]
seca_19 = sub_matriz[i_19:f_19,:]
seca_20 = sub_matriz[i_20:f_20,:]
seca_21 = sub_matriz[i_21:f_21,:]

# seca mensal
secas_5 = np.concatenate((sub_matriz[i_5_19:f_5_19],sub_matriz[i_5_20:f_5_20],sub_matriz[i_5_21:f_5_21]))
secas_5_3 = secas_5.flatten()
secas_6 = np.concatenate((sub_matriz[i_6_19:f_6_19],sub_matriz[i_6_20:f_6_20],sub_matriz[i_6_21:f_6_21]))
secas_6_3 = secas_6.flatten()
secas_7 = np.concatenate((sub_matriz[i_7_18:f_7_18],sub_matriz[i_7_19:f_7_19],sub_matriz[i_7_20:f_7_20]))
secas_7_3 = secas_7.flatten()
secas_8 = np.concatenate((sub_matriz[i_8_18:f_8_18],sub_matriz[i_8_19:f_8_19],sub_matriz[i_8_20:f_8_20]))
secas_8_3 = secas_8.flatten()

secas = np.zeros((len(secas_datas),n_sim3))
secas = np.concatenate((seca_18,seca_19,seca_20,seca_21))
#color = mycolors[2]
for j in range(n_sim3):
    plt.plot(datas18, seca_18[:, j], linestyle=ls, color=color,linewidth=lw,marker=ms,label=myscenarios[2])
    plt.plot(datas19, seca_19[:, j], linestyle=ls, color=color, linewidth=lw, marker=ms)
    plt.plot(datas20, seca_20[:, j], linestyle=ls, color=color, linewidth=lw, marker=ms)
    plt.plot(datas21, seca_21[:, j], linestyle=ls, color=color, linewidth=lw, marker=ms)
plt.xticks(["01/07/2018","01/05/2019", "01/07/2019","01/05/2020","01/07/2020","01/05/2021","30/06/2021"])
plt.ylabel(my_ylabel)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.gcf().autofmt_xdate()
plt.axhline(y=q90, color='darkblue', linestyle=l90, linewidth=0.5, label=r'$Q_{90}$')
plt.axhline(y=rem, color='darkred', linestyle=lrem, linewidth=0.5, label='25% ' + r'$Q_{90}$')
plt.ylim(min_y+0.1,max_y)
plt.yscale('log')
plt.savefig('integração seca'+myscenarios[2]+'log .jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

for j in range(n_sim3):
    plt.plot(datas, sub_matriz3[:, j], linestyle=ls, color=color,linewidth=lw,marker=ms,label=myscenarios[2])
plt.xticks(["01/07/2018","31/08/2018","01/05/2019", "31/08/2019","01/05/2020","31/08/2020","01/05/2021","30/06/2021"])
plt.ylabel(my_ylabel)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.gcf().autofmt_xdate()
plt.axhline(y=q90, color='darkblue', linestyle=l90, linewidth=0.5, label=r'$Q_{90}$')
plt.axhline(y=rem, color='darkred', linestyle=lrem, linewidth=0.5, label='25% ' + r'$Q_{90}$')
plt.ylim(min_y+0.1,max_y)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.yscale('log')
plt.legend(by_label.values(), by_label.keys())
plt.savefig('integração total'+myscenarios[2]+'log.jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

for j in range(n_sim3):
    plt.plot(datas, sub_matriz3[:, j], linestyle=ls, color=color,linewidth=lw,marker=ms,label=myscenarios[2])
plt.xticks(["01/07/2018","31/08/2018","01/05/2019", "31/08/2019","01/05/2020","31/08/2020","01/05/2021","30/06/2021"])
plt.ylabel(my_ylabel)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.gcf().autofmt_xdate()
plt.axhline(y=q90, color='darkblue', linestyle=l90, linewidth=0.5, label=r'$Q_{90}$')
plt.axhline(y=rem, color='darkred', linestyle=lrem, linewidth=0.5, label='25% ' + r'$Q_{90}$')
plt.ylim((0,1.05*max_y))
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.savefig('integração total'+myscenarios[2]+'linear.jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

#Sc3
#periodos de seca em cada ano
sub_matriz = sub_matriz4
seca_18 = sub_matriz[i_18:f_18,:]
seca_19 = sub_matriz[i_19:f_19,:]
seca_20 = sub_matriz[i_20:f_20,:]
seca_21 = sub_matriz[i_21:f_21,:]

# seca mensal
secas_5 = np.concatenate((sub_matriz[i_5_19:f_5_19],sub_matriz[i_5_20:f_5_20],sub_matriz[i_5_21:f_5_21]))
secas_5_4 = secas_5.flatten()
secas_6 = np.concatenate((sub_matriz[i_6_19:f_6_19],sub_matriz[i_6_20:f_6_20],sub_matriz[i_6_21:f_6_21]))
secas_6_4 = secas_6.flatten()
secas_7 = np.concatenate((sub_matriz[i_7_18:f_7_18],sub_matriz[i_7_19:f_7_19],sub_matriz[i_7_20:f_7_20]))
secas_7_4 = secas_7.flatten()
secas_8 = np.concatenate((sub_matriz[i_8_18:f_8_18],sub_matriz[i_8_19:f_8_19],sub_matriz[i_8_20:f_8_20]))
secas_8_4 = secas_8.flatten()

secas = np.zeros((len(secas_datas),n_sim4))
secas = np.concatenate((seca_18,seca_19,seca_20,seca_21))
#color = mycolors[3]
for j in range(n_sim4):
    plt.plot(datas18, seca_18[:, j], linestyle=ls, color=color,linewidth=lw,marker=ms,label=myscenarios[3])
    plt.plot(datas19, seca_19[:, j], linestyle=ls, color=color, linewidth=lw, marker=ms)
    plt.plot(datas20, seca_20[:, j], linestyle=ls, color=color, linewidth=lw, marker=ms)
    plt.plot(datas21, seca_21[:, j], linestyle=ls, color=color, linewidth=lw, marker=ms)
plt.xticks(["01/07/2018","01/05/2019", "01/07/2019","01/05/2020","01/07/2020","01/05/2021","30/06/2021"])
plt.ylabel(my_ylabel)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.gcf().autofmt_xdate()
plt.axhline(y=q90, color='darkblue', linestyle=l90, linewidth=0.5, label=r'$Q_{90}$')
plt.axhline(y=rem, color='darkred', linestyle=lrem, linewidth=0.5, label='25% ' + r'$Q_{90}$')
plt.ylim(min_y+0.1,max_y)
plt.yscale('log')
plt.savefig('integração seca'+myscenarios[3]+'log .jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

for j in range(n_sim4):
    plt.plot(datas, sub_matriz4[:, j], linestyle=ls, color=color,linewidth=lw,marker=ms,label=myscenarios[3])
plt.xticks(["01/07/2018","31/08/2018","01/05/2019", "31/08/2019","01/05/2020","31/08/2020","01/05/2021","30/06/2021"])
plt.ylabel(my_ylabel)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.gcf().autofmt_xdate()
plt.axhline(y=q90, color='darkblue', linestyle=l90, linewidth=0.5, label=r'$Q_{90}$')
plt.axhline(y=rem, color='darkred', linestyle=lrem, linewidth=0.5, label='25% ' + r'$Q_{90}$')
plt.ylim(min_y+0.1,max_y)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.yscale('log')
plt.savefig('integração total'+myscenarios[3]+'log.jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

for j in range(n_sim4):
    plt.plot(datas, sub_matriz4[:, j], linestyle=ls, color=color,linewidth=lw,marker=ms,label=myscenarios[3])
plt.xticks(["01/07/2018","31/08/2018","01/05/2019", "31/08/2019","01/05/2020","31/08/2020","01/05/2021","30/06/2021"])
plt.ylabel(my_ylabel)
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.gcf().autofmt_xdate()
plt.axhline(y=q90, color='darkblue', linestyle=l90, linewidth=0.5, label=r'$Q_{90}$')
plt.axhline(y=rem, color='darkred', linestyle=lrem, linewidth=0.5, label='25% ' + r'$Q_{90}$')
plt.ylim((0,1.05*max_y))
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.savefig('integração total'+myscenarios[3]+'linear.jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

# gráficos boxplot mensal - conjunto
def box_plot(data,fill_color,position):
    bp = ax.boxplot(data, patch_artist=True,positions=[position])
    for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], color='black')
    for patch in bp['boxes']:
        patch.set(facecolor=fill_color)
    return bp

fig, ax = plt.subplots()
bp1 = box_plot(secas_5_1, mycolors[0],0)
bp2 = box_plot(secas_5_2, mycolors[1],1)
bp3 = box_plot(secas_5_3, mycolors[2],2)
bp4 = box_plot(secas_5_4, mycolors[3],3)
bp5 = box_plot(secas_6_1, mycolors[0],4)
bp6 = box_plot(secas_6_2, mycolors[1],5)
bp7 = box_plot(secas_6_3, mycolors[2],6)
bp8 = box_plot(secas_6_4, mycolors[3],7)
bp9 = box_plot(secas_7_1, mycolors[0],8)
bp10 = box_plot(secas_7_2, mycolors[1],9)
bp11 = box_plot(secas_7_3, mycolors[2],10)
bp12 = box_plot(secas_7_4, mycolors[3],11)
bp13 = box_plot(secas_8_1, mycolors[0],12)
bp14 = box_plot(secas_8_2, mycolors[1],13)
bp15 = box_plot(secas_8_3, mycolors[2],14)
bp16 = box_plot(secas_8_4, mycolors[3],15)
ax.legend([bp1["boxes"][0], bp2["boxes"][0],bp3["boxes"][0],bp4["boxes"][0]],myscenarios)
ax.set_xticks([],[])
plt.xticks(ticks=[2.5,6.5,10.5,14.5],labels=mymonths)
# ax.legend([bp1_1["boxes"][0], bp1_2["boxes"][0], bp1_3["boxes"][0], bp1_4["boxes"][0]], mylabels, loc='upper left', fontsize='x-small', ncol=2, bbox_to_anchor=(0, -0.25))
ax.axhline(y=q90, color='darkblue', linestyle=l90, linewidth=0.5, label=r'$Q_{90}$')
ax.axhline(y=rem, color='darkred', linestyle=lrem, linewidth=0.5, label='25% ' + r'$Q_{90}$')
plt.yscale("log")
plt.ylabel('log '+my_ylabel)
fig.legend(loc='upper left')
plt.savefig('integração total - seca mensal log'+'.jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

#Conjunto dos 4 gráficos 2x2
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
lim = [0,1.05*max_y]
for j in range(n_sim4):
    ax1.plot(datas, sub_matriz1[:, j], linestyle=ls, color=mycolors[0],linewidth=lw,marker=ms,label=myscenarios[0])
    ax1.set_ylabel(ylabel='Vazão diária'+ "\n" + 'simulada (m³/s)')
    ax1.set_ylim(lim)
    ax1.set_xticks([], [])
    ax2.plot(datas, sub_matriz2[:, j], linestyle=ls, color=mycolors[1],linewidth=lw,marker=ms,label=myscenarios[1])
    ax2.set_ylim(lim)
    ax2.set_xticks([], [])
    ax2.set_yticks([], [])
    ax3.plot(datas, sub_matriz3[:, j], linestyle=ls, color=mycolors[2],linewidth=lw,marker=ms,label=myscenarios[2])
    ax3.set_ylabel(ylabel='Vazão diária'+ "\n" + 'simulada (m³/s)')
    ax3.set_ylim(lim)
    ax3.set_xticks([], [])
    # ax3.tick_params(axis='x', labelsize=6)
    ax4.plot(datas, sub_matriz4[:, j], linestyle=ls, color=mycolors[3],linewidth=lw,marker=ms,label=myscenarios[3])
    ax4.set_ylim(lim)
    ax4.set_xticklabels(
        ["01/07/2018", "31/08/2018", "01/05/2019", "31/08/2019", "01/05/2020", "31/08/2020", "01/05/2021",
         "30/06/2021"])
    ax4.set_yticks([], [])
# for ax in fig.get_axes():
#     ax.label_outer()
for ax in fig.get_axes():
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())
plt.gcf().autofmt_xdate()
plt.ylim((0,1.05*max_y))
plt.xticks(
    ["01/07/2018", "31/08/2018", "01/05/2019", "31/08/2019", "01/05/2020", "31/08/2020", "01/05/2021", "30/06/2021"],
    fontsize=5)
fig.savefig('conjunto total linear.jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

# fig, ax = plt.subplots()
# ms = 1
# m = 'o'
# mylabels = myscenarios
# bp1_1 = ax.boxplot(secas_5_1, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[0]), positions=[1])
# bp1_2 = ax.boxplot(secas_5_2, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[1]), positions=[2])
# bp1_3 = ax.boxplot(secas_5_3, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[2]), positions=[3])
# bp1_4 = ax.boxplot(secas_5_4, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[3]), positions=[4])
# bp2_1 = ax.boxplot(secas_6_1, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[0]), positions=[5])
# bp2_2 = ax.boxplot(secas_6_2, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[1]), positions=[6])
# bp2_3 = ax.boxplot(secas_6_3, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[2]), positions=[7])
# bp2_4 = ax.boxplot(secas_6_4, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[3]), positions=[8])
# bp3_1 = ax.boxplot(secas_7_1, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[0]), positions=[9])
# bp3_2 = ax.boxplot(secas_7_2, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[1]), positions=[10])
# bp3_3 = ax.boxplot(secas_7_3, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[2]), positions=[11])
# bp3_4 = ax.boxplot(secas_7_4, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[3]), positions=[12])
# bp4_1 = ax.boxplot(secas_8_1, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[0]), positions=[13])
# bp4_2 = ax.boxplot(secas_8_2, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[1]), positions=[14])
# bp4_3 = ax.boxplot(secas_8_3, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[2]), positions=[15])
# bp4_4 = ax.boxplot(secas_8_4, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[3]), positions=[16])
# plt.xticks(ticks=[2.5,6.5,10.5,14.5],labels=mymonths)
# ax.legend([bp1_1["boxes"][0], bp1_2["boxes"][0], bp1_3["boxes"][0], bp1_4["boxes"][0]], mylabels, loc='upper left', fontsize='x-small', ncol=2, bbox_to_anchor=(0, -0.25))
# plt.yscale("log")
# plt.ylabel('log '+my_ylabel)
# plt.axhline(y=q90, color='darkblue', linestyle='--',linewidth=0.5,label=r'$Q_{90}$')
# plt.axhline(y=rem, color='orange', linestyle='--',linewidth=0.5,label='25% '+r'$Q_{90}$')
# fig.legend(loc='upper left')
# plt.show()
# plt.savefig('integração total - seca mensal log'+'.jpg',format='jpg',dpi=600) # salva a figura em jpg
# plt.close()

#boxplot individual por mês conjunto cenários
#Maio
fig, ax = plt.subplots()
bp1 = box_plot(secas_5_1, mycolors[0],0)
bp2 = box_plot(secas_5_2, mycolors[1],1)
bp3 = box_plot(secas_5_3, mycolors[2],2)
bp4 = box_plot(secas_5_4, mycolors[3],3)
ax.legend([bp1["boxes"][0], bp2["boxes"][0],bp3["boxes"][0],bp4["boxes"][0]],myscenarios)
ax.set_xlabel(mymonths[0])
ax.set_xticks([],[])
ax.axhline(y=q90, color='darkblue', linestyle='--',linewidth=0.5,label=r'$Q_{90}$')
ax.axhline(y=rem, color='orange', linestyle='--',linewidth=0.5,label='25% '+r'$Q_{90}$')
plt.ylabel(my_ylabel)
fig.legend(loc='upper left')
plt.savefig('integração total - seca'+mymonths[0]+'.jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

# fig, ax = plt.subplots()
# ms = 1
# m = 'o'
# bp1_1 = ax.boxplot(secas_5_1, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[0]), positions=[1])
# bp1_2 = ax.boxplot(secas_5_2, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[1]), positions=[2])
# bp1_3 = ax.boxplot(secas_5_3, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[2]), positions=[3])
# bp1_4 = ax.boxplot(secas_5_4, flierprops={'marker': m, 'markersize': ms}, patch_artist=True,
#                  boxprops=dict(facecolor=mycolors[3]), positions=[4])
# ax.set_xlabel(mymonths[0])
# ax.set_xticks([],[])
# ax.axhline(y=q90, color='darkblue', linestyle='--',linewidth=0.5,label=r'$Q_{90}$')
# ax.axhline(y=rem, color='orange', linestyle='--',linewidth=0.5,label='25% '+r'$Q_{90}$')
# plt.ylabel(my_ylabel)
# ax.legend(handles=[bp1_1["boxes"][0], bp1_2["boxes"][0], bp1_3["boxes"][0],bp1_4["boxes"][0]], labels=['S7','S11','S12','S13'],loc='upper left', fontsize='x-small', ncol=2)
# # ax.legend([bp1_1["boxes"][0], bp1_2["boxes"][0], bp1_3["boxes"][0]], labels=['S7','S11','S12'], loc='upper left', fontsize='x-small', ncol=2, bbox_to_anchor=(0, -0.25))
# ax.legend()
# plt.savefig('integração total - seca maio'+'.jpg',format='jpg',dpi=600) # salva a figura em jpg
# plt.close()

#Junho
fig, ax = plt.subplots()
bp1 = box_plot(secas_6_1, mycolors[0],0)
bp2 = box_plot(secas_6_2, mycolors[1],1)
bp3 = box_plot(secas_6_3, mycolors[2],2)
bp4 = box_plot(secas_6_4, mycolors[3],3)
ax.legend([bp1["boxes"][0], bp2["boxes"][0],bp3["boxes"][0],bp4["boxes"][0]],myscenarios)
ax.set_xlabel(mymonths[1])
ax.set_xticks([],[])
ax.axhline(y=q90, color='darkblue', linestyle='--',linewidth=0.5,label=r'$Q_{90}$')
ax.axhline(y=rem, color='orange', linestyle='--',linewidth=0.5,label='25% '+r'$Q_{90}$')
plt.ylabel(my_ylabel)
fig.legend(loc='upper left')
plt.savefig('integração total - seca'+mymonths[1]+'.jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

#Julho
fig, ax = plt.subplots()
bp1 = box_plot(secas_7_1, mycolors[0],0)
bp2 = box_plot(secas_7_2, mycolors[1],1)
bp3 = box_plot(secas_7_3, mycolors[2],2)
bp4 = box_plot(secas_7_4, mycolors[3],3)
ax.legend([bp1["boxes"][0], bp2["boxes"][0],bp3["boxes"][0],bp4["boxes"][0]],myscenarios)
ax.set_xlabel(mymonths[2])
ax.set_xticks([],[])
ax.axhline(y=q90, color='darkblue', linestyle='--',linewidth=0.5,label=r'$Q_{90}$')
ax.axhline(y=rem, color='orange', linestyle='--',linewidth=0.5,label='25% '+r'$Q_{90}$')
plt.ylabel(my_ylabel)
fig.legend(loc='upper left')
plt.savefig('integração total - seca'+mymonths[2]+'.jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

#Agosto
fig, ax = plt.subplots()
bp1 = box_plot(secas_8_1, mycolors[0],0)
bp2 = box_plot(secas_8_2, mycolors[1],1)
bp3 = box_plot(secas_8_3, mycolors[2],2)
bp4 = box_plot(secas_8_4, mycolors[3],3)
ax.legend([bp1["boxes"][0], bp2["boxes"][0],bp3["boxes"][0],bp4["boxes"][0]],myscenarios)
ax.set_xlabel(mymonths[3])
ax.set_xticks([],[])
ax.axhline(y=q90, color='darkblue', linestyle='--',linewidth=0.5,label=r'$Q_{90}$')
ax.axhline(y=rem, color='orange', linestyle='--',linewidth=0.5,label='25% '+r'$Q_{90}$')
plt.ylabel(my_ylabel)
fig.legend(loc='upper left')
plt.savefig('integração total - seca'+mymonths[3]+'.jpg',format='jpg',dpi=600) # salva a figura em jpg
plt.close()

# estatísticas
# porcentagens de valores em Agosto menores que a q 90 para cada cenário
# v_8_2 = np.array(secas_8_2)
# perc_menor = (np.count_nonzero(v_8_2 <= rem))#/(len(secas_8_2)*n_sim2)
# print('cenario 2',perc_menor)
# perc_menor = (np.count_nonzero(v_8_2 <= q90))#/(len(secas_8_2)*n_sim2)
# print('cenario 2 90',perc_menor)
# v_8_3 = np.array(secas_8_3)
# perc_menor = (np.count_nonzero(v_8_3 <= rem))#/(len(secas_8_3)*n_sim3)
# print('cenario 3',perc_menor)
# perc_menor = (np.count_nonzero(v_8_3 <= q90))#/(len(secas_8_3)*n_sim3)
# print('cenario 3 90',perc_menor)
# v_8_4 = np.array(secas_8_4)
# perc_menor = (np.count_nonzero(v_8_4 <= rem))#/(len(secas_8_3)*n_sim3)
# print('cenario 4',perc_menor)
# perc_menor = (np.count_nonzero(v_8_4 <= q90))#/(len(secas_8_3)*n_sim3)
# print('cenario 4 90',perc_menor)

# for j in range(n_sim1):
#     plt.plot(datas18, seca_18[:, j], linestyle='-', color='lightgrey',linewidth=lw,marker=None,label='S7-2018')
#     plt.plot(datas19, seca_19[:, j], linestyle='-', color='grey', linewidth=lw, marker=None, label='S7-2019')
#     plt.plot(datas20, seca_20[:, j], linestyle='-', color='darkgrey', linewidth=lw, marker=None, label='S7-2020')
#     plt.plot(datas21, seca_21[:, j], linestyle='-', color='black', linewidth=lw, marker=None, label='S7-2021')
# for i in range(len(datas18)):
#     plt.plot(datas18,k18,linestyle='-',color='red',linewidth=0.4,marker=None,label='Média de 100 simulações')
# for i in range(len(datas19)):
#     plt.plot(datas19,k19,linestyle='-',color='red',linewidth=0.4,marker=None,label='Média de 100 simulações')
# for i in range(len(datas20)):
#     plt.plot(datas20,k20,linestyle='-',color='red',linewidth=0.4,marker=None,label='Média de 100 simulações')
# for i in range(len(datas21)):
#     plt.plot(datas21,k21,linestyle='-',color='red',linewidth=0.4,marker=None,label='Média de 100 simulações')
# plt.xticks(["01/07/2018","01/07/2019","01/07/2020","30/06/2021"])
# plt.ylabel('Vazão diária simulada (m³/s)')
# handles, labels = plt.gca().get_legend_handles_labels()
# by_label = dict(zip(labels, handles))
# plt.legend(by_label.values(), by_label.keys())
# plt.gcf().autofmt_xdate()
# plt.axhline(y=1.245, color='blue', linestyle='-')
# plt.show()
# #plt.savefig('integração S7 - seca '+'.jpg',format='jpg',dpi=600) # salva a figura em jpg
# plt.close()
#
# # lw = 0.15
# # lw_m = 0.3
# # for j in range(n_sim):
# #     plt.plot(datas18,seca_18[:,j],linestyle='-',color='lightgrey',linewidth=lw,marker=None,label='Sc1-2018')
# #     plt.plot(datas19, seca_19[:, j], linestyle='-', color='grey', linewidth=lw, marker=None, label='Sc1-2019')
# #     plt.plot(datas20, seca_20[:, j], linestyle='-', color='darkgrey', linewidth=lw, marker=None, label='Sc1-2020')
# #     plt.plot(datas21, seca_21[:, j], linestyle='-', color='black', linewidth=lw, marker=None, label='Sc1-2021')
# # for i in range(len(datas18)):
# #     plt.plot(datas18,k18,linestyle='-',color='red',linewidth=lw_m,marker=None,label='Average 100 simulations')
# # for i in range(len(datas19)):
# #     plt.plot(datas19,k19,linestyle='-',color='red',linewidth=lw_m,marker=None)
# # for i in range(len(datas20)):
# #     plt.plot(datas20,k20,linestyle='-',color='red',linewidth=lw_m,marker=None)
# # for i in range(len(datas21)):
# #     plt.plot(datas21,k21,linestyle='-',color='red',linewidth=lw_m,marker=None)
# # plt.xticks(["01/07/2018","01/07/2019","01/07/2020","30/06/2021"])
# # plt.ylabel('Simulated daily streamflow (m³/s)')
# # handles, labels = plt.gca().get_legend_handles_labels()
# # by_label = dict(zip(labels, handles))
# # plt.legend(by_label.values(), by_label.keys())
# # plt.gcf().autofmt_xdate()
# # plt.savefig('integration Sc1 - dry '+'.jpg',format='jpg',dpi=600) # salva a figura em jpg
# # plt.close()
# #
# # # boxplot seca
# # ms = 1
# # m = 'o'
# # # plt.boxplot(np.transpose(seca_18),flierprops={'marker': m, 'markersize': ms})
# # # plt.boxplot(np.transpose(seca_19),flierprops={'marker': m, 'markersize': ms})
# # # plt.boxplot(np.transpose(seca_20),flierprops={'marker': m, 'markersize': ms})
# # plt.boxplot(np.transpose(seca_21),flierprops={'marker': m, 'markersize': ms})
# # plt.ylim(0, 140)
# # plt.ylabel('Simulated daily streamflow (m³/s)')
# # plt.gcf().autofmt_xdate()
# # plt.xticks([0,365,731,1095],["01/07/2018","01/07/2019","01/07/2020","30/06/2021",])
# # #plt.savefig(titulo + '.jpg', format='jpg', dpi=600)
# # plt.show()
# # plt.close()
# #
# # # periodos de seca em cada ano Sc2
# # seca_18 = sub_matriz2[i_18[0]:f_18[0],:]
# # seca_19 = sub_matriz2[i_19[0]:f_19[0],:]
# # seca_20 = sub_matriz2[i_20[0]:f_20[0],:]
# # seca_21 = sub_matriz2[i_21[0]:f_21[0],:]
# #
# # k18 = []
# # for i in range(len(datas18)):
# #     k18.append(sts.mean(seca_18[i, :]))
# # k19 = []
# # for i in range(len(datas19)):
# #     k19.append(sts.mean(seca_19[i, :]))
# # k20 = []
# # for i in range(len(datas20)):
# #     k20.append(sts.mean(seca_20[i, :]))
# # k21 = []
# # for i in range(len(datas21)):
# #     k21.append(sts.mean(seca_21[i, :]))
# #
# # for j in range(n_sim2):
# #     plt.plot(datas18,seca_18[:,j],linestyle='-',color='grey',linewidth=lw,marker=None)
# #     plt.plot(datas19, seca_19[:, j], linestyle='-', color='grey', linewidth=lw, marker=None)
# #     plt.plot(datas20, seca_20[:, j], linestyle='-', color='grey', linewidth=lw, marker=None)
# #     plt.plot(datas21, seca_21[:, j], linestyle='-', color='grey', linewidth=lw, marker=None)
# #     # plt.plot(datas18,seca_18[:,j],linestyle='-',color='lightgrey',linewidth=lw,marker=None,label='Sc2-2018')
# #     # plt.plot(datas19, seca_19[:, j], linestyle='-', color='grey', linewidth=lw, marker=None, label='Sc2-2019')
# #     # plt.plot(datas20, seca_20[:, j], linestyle='-', color='darkgrey', linewidth=lw, marker=None, label='Sc2-2020')
# #     # plt.plot(datas21, seca_21[:, j], linestyle='-', color='black', linewidth=lw, marker=None, label='Sc2-2021')
# # for i in range(len(datas18)):
# #     plt.plot(datas18,k18,linestyle='-',color='red',linewidth=lw_m,marker=None,label='Average 100 simulations')
# # for i in range(len(datas19)):
# #     plt.plot(datas19,k19,linestyle='-',color='red',linewidth=lw_m,marker=None)
# # for i in range(len(datas20)):
# #     plt.plot(datas20,k20,linestyle='-',color='red',linewidth=lw_m,marker=None)
# # for i in range(len(datas21)):
# #     plt.plot(datas21,k21,linestyle='-',color='red',linewidth=lw_m,marker=None)
# # plt.xticks(["01/07/2018","01/07/2019","01/07/2020","30/06/2021"])
# # plt.ylabel('Simulated daily streamflow (m³/s)')
# # handles, labels = plt.gca().get_legend_handles_labels()
# # by_label = dict(zip(labels, handles))
# # plt.legend(by_label.values(), by_label.keys())
# # plt.gcf().autofmt_xdate()
# # plt.savefig('integration Sc2 - dry - same color'+'.jpg',format='jpg',dpi=600) # salva a figura em jpg
# # plt.close()
#
# # Os dois juntos
# #Sc2
# # periodos de seca em cada ano Sc2
# lw = 0.15
# lw_m = 0.3
#
# seca_18 = sub_matriz2[i_18[0]:f_18[0],:]
# seca_19 = sub_matriz2[i_19[0]:f_19[0],:]
# seca_20 = sub_matriz2[i_20[0]:f_20[0],:]
# seca_21 = sub_matriz2[i_21[0]:f_21[0],:]
#
# l18 = []
# for i in range(len(datas18)):
#     l18.append(sts.mean(seca_18[i, :]))
# l19 = []
# for i in range(len(datas19)):
#     l19.append(sts.mean(seca_19[i, :]))
# l20 = []
# for i in range(len(datas20)):
#     l20.append(sts.mean(seca_20[i, :]))
# l21 = []
# for i in range(len(datas21)):
#     l21.append(sts.mean(seca_21[i, :]))
#
# color = 'grey'
# for j in range(n_sim2):
#     plt.plot(datas18,seca_18[:,j],linestyle='-',color=color,linewidth=lw,marker=None,label='Sc2')
#     plt.plot(datas19, seca_19[:, j], linestyle='-', color=color, linewidth=lw, marker=None)
#     plt.plot(datas20, seca_20[:, j], linestyle='-', color=color, linewidth=lw, marker=None)
#     plt.plot(datas21, seca_21[:, j], linestyle='-', color=color, linewidth=lw, marker=None)
# #Sc1
# #periodos de seca em cada ano
# seca_18 = sub_matriz[i_18[0]:f_18[0],:]
# seca_19 = sub_matriz[i_19[0]:f_19[0],:]
# seca_20 = sub_matriz[i_20[0]:f_20[0],:]
# seca_21 = sub_matriz[i_21[0]:f_21[0],:]
#
# k18 = []
# for i in range(len(datas18)):
#     k18.append(sts.mean(seca_18[i, :]))
# k19 = []
# for i in range(len(datas19)):
#     k19.append(sts.mean(seca_19[i, :]))
# k20 = []
# for i in range(len(datas20)):
#     k20.append(sts.mean(seca_20[i, :]))
# k21 = []
# for i in range(len(datas21)):
#     k21.append(sts.mean(seca_21[i, :]))
#
#
# c = 'black'
# for j in range(n_sim):
#     plt.plot(datas18, seca_18[:, j], linestyle='-', color=c, linewidth=lw, marker=None,label='Sc1')
#     plt.plot(datas19, seca_19[:, j], linestyle='-', color=c, linewidth=lw, marker=None)
#     plt.plot(datas20, seca_20[:, j], linestyle='-', color=c, linewidth=lw, marker=None)
#     plt.plot(datas21, seca_21[:, j], linestyle='-', color=c, linewidth=lw, marker=None)
# # for i in range(len(datas18)):
# #     plt.plot(datas18,k18,linestyle='-',color='darkred',linewidth=lw_m,marker=None,label='Average 100 simulations Sc1')
# # for i in range(len(datas19)):
# #     plt.plot(datas19,k19,linestyle='-',color='darkred',linewidth=lw_m,marker=None)
# # for i in range(len(datas20)):
# #     plt.plot(datas20,k20,linestyle='-',color='darkred',linewidth=lw_m,marker=None)
# # for i in range(len(datas21)):
# #     plt.plot(datas21,k21,linestyle='-',color='darkred',linewidth=lw_m,marker=None)
#
#
# # for i in range(len(datas18)):
# #     plt.plot(datas18,l18,linestyle='-',color='red',linewidth=lw_m,marker=None,label='Average 100 simulations Sc2')
# # for i in range(len(datas19)):
# #     plt.plot(datas19,l19,linestyle='-',color='red',linewidth=lw_m,marker=None)
# # for i in range(len(datas20)):
# #     plt.plot(datas20,l20,linestyle='-',color='red',linewidth=lw_m,marker=None)
# # for i in range(len(datas21)):
# #     plt.plot(datas21,l21,linestyle='-',color='red',linewidth=lw_m,marker=None)
# plt.xticks(["01/07/2018","01/07/2019","01/07/2020","30/06/2021"])
# plt.ylabel('logarithm Simulated daily streamflow (m³/s)')
# plt.yscale('log')
# handles, labels = plt.gca().get_legend_handles_labels()
# by_label = dict(zip(labels, handles))
# plt.legend(by_label.values(), by_label.keys())
# plt.gcf().autofmt_xdate()
# plt.show()
# # plt.savefig('integration Sc2 - dry - same color'+'.jpg',format='jpg',dpi=600) # salva a figura em jpg
# # plt.close()