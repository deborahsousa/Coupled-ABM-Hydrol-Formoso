#Programa que gera uma matriz de probabilidades a partir de arquivos .csv contendo a frequência de dados em determinados
# intervalos
# Autoria: Déborah Santos de Sousa

import numpy as np # package de manipulação de listas e matrizes
import pandas as pd # package de leitura de csv
import matplotlib.pyplot as plt # Plotagem de gráficos
from scipy.stats import skew

#Dados de entrada
### Matriz característica
matriz_carac = np.array(pd.read_csv('matriz_caract.csv',sep=";",header=None))
###Volume
matriz_demanda = np.array(pd.read_csv('volume_demanda_urubu.csv', sep=";", decimal="."))

def PlotHistCategoria(lista_demanda_categ,titulo_grafico):
    list_bins = np.arange(1000, 191001, 10000)
    list_bins = np.insert(list_bins, 0,100)
    list_bins = np.insert(list_bins, 0,1)
    list_bins = np.insert(list_bins, 0,0)
    my_total = len(lista_demanda_categ)
    fig2 = plt.hist(lista_demanda_categ, bins=list_bins, histtype = 'bar',weights=np.ones_like(lista_demanda_categ)*100/len(lista_demanda_categ))
    my_bins = fig2[1]
    my_perc = fig2[0]
    np.savetxt('list_perc_sem9bombas' +str(titulo_grafico)+'.csv',my_perc)
    np.savetxt('list_bins_sem9bombas' + str(titulo_grafico) + '.csv', my_bins)
    plt.close()

def ListaCategoriasSecaAnual15d(matriz_carac,matriz_demanda,categoria):
    # retirando os caracteres de 'ano' da coluna 'data'
    lista_demanda_sem_ano = matriz_demanda[:,0]
    for i in range(len(lista_demanda_sem_ano)):
        elemento_sem_ano = lista_demanda_sem_ano[i].split('/')
        elemento_todo = elemento_sem_ano[0] + "/" + elemento_sem_ano[1]
        lista_demanda_sem_ano[i] = elemento_todo
    matriz_demanda[:,0] = lista_demanda_sem_ano

    #retirando as colunas das bombas com mais de 70% de dados igual a zero na seca
    matriz_demanda[:,[6,7,25,26,27,28,29,33,34]] = np.nan

    ix_sem1a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '1/MAY'] #índice da linha da data inicial da semana 1
    ix_sem1b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '15/MAY'] #índice da linha da data final da semana 1
    ix_sem2a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '16/MAY'] #índice da linha da data inicial da semana 2
    ix_sem2b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '30/MAY'] #índice da linha da data final da semana 2
    ix_sem3a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/MAY'] #índice da linha da data inicial da semana 3
    ix_sem3b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '14/JUNE'] #índice da linha da data final da semana 3
    ix_sem4a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '15/JUNE'] #índice da linha da data inicial da semana 4
    ix_sem4b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '29/JUNE'] #índice da linha da data final da semana 4
    ix_sem5a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '30/JUNE'] #índice da linha da data inicial da semana 5
    ix_sem5b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '14/JULY'] #índice da linha da data final da semana 5
    ix_sem6a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '15/JULY'] #índice da linha da data inicial da semana 6
    ix_sem6b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '29/JULY'] #índice da linha da data final da semana 6
    ix_sem7a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '30/JULY'] #índice da linha da data inicial da semana 7
    ix_sem7b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '13/AUGUST'] #índice da linha da data final da semana 7
    ix_sem8a = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '14/AUGUST'] #índice da linha da data inicial da semana 8
    ix_sem8b = [i for i, v in enumerate(matriz_demanda[:, 0]) if v == '31/AUGUST'] #índice da linha da data final da semana 8

    #definindo em variáveis os índices onde se encontram as datas definidas
    a = ix_sem1a
    b = ix_sem1b
    c = ix_sem2a
    d = ix_sem2b
    e = ix_sem3a
    f = ix_sem3b
    g = ix_sem4a
    h = ix_sem4b
    q = ix_sem5a
    j = ix_sem5b
    k = ix_sem6a
    l = ix_sem6b
    m = ix_sem7a
    n = ix_sem7b
    o = ix_sem8a
    p = ix_sem8b

    matriz_demanda1 = np.concatenate((matriz_demanda[a[0]:b[0]],matriz_demanda[a[1]:b[1]],matriz_demanda[a[2]:b[2]],matriz_demanda[a[3]:b[3]],matriz_demanda[a[4]:b[4]],matriz_demanda[a[5]:b[5]],matriz_demanda[a[6]:b[6]]))
    matriz_demanda1 = matriz_demanda1[:, 1:]
    matriz_demanda2 = np.concatenate((matriz_demanda[c[0]:d[0]],matriz_demanda[c[1]:d[1]],matriz_demanda[c[2]:d[2]],matriz_demanda[c[3]:d[3]],matriz_demanda[c[4]:d[4]],matriz_demanda[c[5]:d[5]],matriz_demanda[c[6]:d[6]]))
    matriz_demanda2 = matriz_demanda2[:, 1:]
    matriz_demanda3 = np.concatenate((matriz_demanda[e[0]:f[0]],matriz_demanda[e[1]:f[1]],matriz_demanda[e[2]:f[2]],matriz_demanda[e[3]:f[3]],matriz_demanda[e[4]:f[4]],matriz_demanda[e[5]:f[5]],matriz_demanda[e[6]:f[6]]))
    matriz_demanda3 = matriz_demanda3[:, 1:]
    matriz_demanda4 = np.concatenate((matriz_demanda[g[0]:h[0]],matriz_demanda[g[1]:h[1]],matriz_demanda[g[2]:h[2]],matriz_demanda[g[3]:h[3]],matriz_demanda[g[4]:h[4]],matriz_demanda[g[5]:h[5]],matriz_demanda[g[6]:h[6]]))
    matriz_demanda4 = matriz_demanda4[:, 1:]
    matriz_demanda5 = np.concatenate((matriz_demanda[q[0]:j[0]],matriz_demanda[q[1]:j[1]],matriz_demanda[q[2]:j[2]],matriz_demanda[q[3]:j[3]],matriz_demanda[q[4]:j[4]],matriz_demanda[q[5]:j[5]],matriz_demanda[q[6]:j[6]]))
    matriz_demanda5 = matriz_demanda5[:, 1:]
    matriz_demanda6 = np.concatenate((matriz_demanda[k[0]:l[0]],matriz_demanda[k[1]:l[1]],matriz_demanda[k[2]:l[2]],matriz_demanda[k[3]:l[3]],matriz_demanda[k[4]:l[4]],matriz_demanda[k[5]:l[5]],matriz_demanda[k[6]:l[6]]))
    matriz_demanda6 = matriz_demanda6[:, 1:]
    matriz_demanda7 = np.concatenate((matriz_demanda[m[0]:n[0]],matriz_demanda[m[1]:n[1]],matriz_demanda[m[2]:n[2]],matriz_demanda[m[3]:n[3]],matriz_demanda[m[4]:n[4]],matriz_demanda[m[5]:n[5]],matriz_demanda[m[6]:n[6]]))
    matriz_demanda7 = matriz_demanda7[:, 1:]
    matriz_demanda8 = np.concatenate((matriz_demanda[o[0]:p[0]],matriz_demanda[o[1]:p[1]],matriz_demanda[o[2]:p[2]],matriz_demanda[o[3]:p[3]],matriz_demanda[o[4]:p[4]],matriz_demanda[o[5]:p[5]],matriz_demanda[o[6]:p[6]]))
    matriz_demanda8 = matriz_demanda8[:, 1:]

    for i in range(0, len(matriz_demanda1)):
        for j in range(len(matriz_demanda1[0])):
            if matriz_demanda1[i, j] == 'None':
                matriz_demanda1[i, j] = np.nan
    matriz_demanda1 = matriz_demanda1.astype(np.float)
    for i in range(0, len(matriz_demanda1)):
        for j in range(len(matriz_demanda1[0])):
            if matriz_demanda1[i, j] >= 2.5e5:
                matriz_demanda1[i, j] = np.nan

    for i in range(0, len(matriz_demanda2)):
        for j in range(len(matriz_demanda2[0])):
            if matriz_demanda2[i, j] == 'None':
                matriz_demanda2[i, j] = np.nan
    matriz_demanda2 = matriz_demanda2.astype(np.float)
    for i in range(0, len(matriz_demanda2)):
        for j in range(len(matriz_demanda2[0])):
            if matriz_demanda2[i, j] >= 2.5e5:
                matriz_demanda2[i, j] = np.nan

    for i in range(0, len(matriz_demanda3)):
        for j in range(len(matriz_demanda3[0])):
            if matriz_demanda3[i, j] == 'None':
                matriz_demanda3[i, j] = np.nan
    matriz_demanda3 = matriz_demanda3.astype(np.float)
    for i in range(0, len(matriz_demanda3)):
        for j in range(len(matriz_demanda3[0])):
            if matriz_demanda3[i, j] >= 2.5e5:
                matriz_demanda3[i, j] = np.nan

    for i in range(0, len(matriz_demanda4)):
        for j in range(len(matriz_demanda4[0])):
            if matriz_demanda4[i, j] == 'None':
                matriz_demanda4[i, j] = np.nan
    matriz_demanda4 = matriz_demanda4.astype(np.float)
    for i in range(0, len(matriz_demanda4)):
        for j in range(len(matriz_demanda4[0])):
            if matriz_demanda4[i, j] >= 2.5e5:
                matriz_demanda4[i, j] = np.nan

    for i in range(0, len(matriz_demanda5)):
        for j in range(len(matriz_demanda5[0])):  # 37 columns, from 0 to 36
            if matriz_demanda5[i, j] == 'None':
                matriz_demanda5[i, j] = np.nan
    matriz_demanda5 = matriz_demanda5.astype(np.float)
    for i in range(0, len(matriz_demanda5)):
        for j in range(len(matriz_demanda5[0])):  # 37 columns, from 0 to 36
            if matriz_demanda5[i, j] >= 2.5e5:
                matriz_demanda5[i, j] = np.nan

    for i in range(0, len(matriz_demanda6)):
        for j in range(len(matriz_demanda6[0])):  # 37 columns, from 0 to 36
            if matriz_demanda6[i, j] == 'None':
                matriz_demanda6[i, j] = np.nan
    matriz_demanda6 = matriz_demanda6.astype(np.float)
    for i in range(0, len(matriz_demanda6)):
        for j in range(len(matriz_demanda6[0])):  # 37 columns, from 0 to 36
            if matriz_demanda6[i, j] >= 2.5e5:
                matriz_demanda6[i, j] = np.nan

    for i in range(0, len(matriz_demanda7)):
        for j in range(len(matriz_demanda7[0])):
            if matriz_demanda7[i, j] == 'None':
                matriz_demanda7[i, j] = np.nan
    matriz_demanda7 = matriz_demanda7.astype(np.float)
    for i in range(0, len(matriz_demanda7)):
        for j in range(len(matriz_demanda7[0])):
            if matriz_demanda7[i, j] >= 2.5e5:
                matriz_demanda7[i, j] = np.nan

    for i in range(0, len(matriz_demanda8)):
        for j in range(len(matriz_demanda8[0])):
            if matriz_demanda8[i, j] == 'None':
                matriz_demanda8[i, j] = np.nan
    matriz_demanda8 = matriz_demanda8.astype(np.float)
    for i in range(0, len(matriz_demanda8)):
        for j in range(len(matriz_demanda8[0])):
            if matriz_demanda8[i, j] >= 2.5e5:
                matriz_demanda8[i, j] = np.nan

    ix_NC = [i for i, v in enumerate(matriz_carac[1, :]) if v == 'NC'] #índices da matriz original e ordenada com perfil NC
    ix_CP = [i for i, v in enumerate(matriz_carac[1, :]) if v == 'CP'] #índices da matriz original e ordenada com perfil CP
    ix_CI = [i for i, v in enumerate(matriz_carac[1, :]) if v == 'CI'] #índices da matriz original e ordenada com perfil CI

    sorted_l_sem1 = []
    sorted_l_sem2 = []
    sorted_l_sem3 = []
    sorted_l_sem4 = []
    sorted_l_sem5 = []
    sorted_l_sem6 = []
    sorted_l_sem7 = []
    sorted_l_sem8 = []

    if categoria == 'NC':
        m_NC = matriz_demanda1[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem1 = sorted(l_NC_nonan)

        m_NC = matriz_demanda2[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem2 = sorted(l_NC_nonan)

        m_NC = matriz_demanda3[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem3 = sorted(l_NC_nonan)

        m_NC = matriz_demanda4[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem4 = sorted(l_NC_nonan)

        m_NC = matriz_demanda5[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem5 = sorted(l_NC_nonan)

        m_NC = matriz_demanda6[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem6 = sorted(l_NC_nonan)

        m_NC = matriz_demanda7[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem7 = sorted(l_NC_nonan)

        m_NC = matriz_demanda8[:,ix_NC] #matriz recortada nas colunas correspondentes ao perfil NC
        l_NC = m_NC.flatten()
        l_NC_nonan = [i for i in l_NC if str(i) != 'nan']
        sorted_l_sem8 = sorted(l_NC_nonan)
    elif categoria == 'CP':
        m_CP = matriz_demanda1[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem1 = sorted(l_CP_nonan)
        m_CP = matriz_demanda2[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem2 = sorted(l_CP_nonan)
        m_CP = matriz_demanda3[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem3 = sorted(l_CP_nonan)
        m_CP = matriz_demanda4[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem4 = sorted(l_CP_nonan)
        m_CP = matriz_demanda5[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem5 = sorted(l_CP_nonan)
        m_CP = matriz_demanda6[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem6 = sorted(l_CP_nonan)
        m_CP = matriz_demanda7[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem7 = sorted(l_CP_nonan)
        m_CP = matriz_demanda8[:,ix_CP] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CP = m_CP.flatten()
        l_CP_nonan = [i for i in l_CP if str(i) != 'nan']
        sorted_l_sem8 = sorted(l_CP_nonan)
    elif categoria == 'CI':
        m_CI = matriz_demanda1[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem1 = sorted(l_CI_nonan)
        m_CI = matriz_demanda2[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem2 = sorted(l_CI_nonan)
        m_CI = matriz_demanda3[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem3 = sorted(l_CI_nonan)
        m_CI = matriz_demanda4[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem4 = sorted(l_CI_nonan)
        m_CI = matriz_demanda5[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem5 = sorted(l_CI_nonan)
        m_CI = matriz_demanda6[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem6 = sorted(l_CI_nonan)
        m_CI = matriz_demanda7[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem7 = sorted(l_CI_nonan)
        m_CI = matriz_demanda8[:,ix_CI] #matriz recortada nas colunas correspondentes ao perfil NC
        l_CI = m_CI.flatten()
        l_CI_nonan = [i for i in l_CI if str(i) != 'nan']
        sorted_l_sem8 = sorted(l_CI_nonan)

    return sorted_l_sem1,sorted_l_sem2,sorted_l_sem3,sorted_l_sem4,sorted_l_sem5,sorted_l_sem6,sorted_l_sem7,sorted_l_sem8

#Saída
# # Lista de porcentagens de dados por intervalo por categoria por quinzena (8*22*3)
# categoria = 'NC'
# for z in range(1,9):
#     titulo = str(categoria) + ' quinzena '+str(z)
#     PlotHistCategoria(ListaCategoriasSecaAnual15d(matriz_carac, matriz_demanda, categoria)[z-1], titulo)
# categoria = 'CP'
# for z in range(1,9):
#     titulo = str(categoria) + ' quinzena '+str(z)
#     PlotHistCategoria(ListaCategoriasSecaAnual15d(matriz_carac, matriz_demanda, categoria)[z-1], titulo)
# categoria = 'CI'
# for z in range(1,9):
#     titulo = str(categoria) + ' quinzena '+str(z)
#     PlotHistCategoria(ListaCategoriasSecaAnual15d(matriz_carac, matriz_demanda, categoria)[z-1], titulo)

my_perc = np.empty((22,8))
categoria = 'NC'
for j in range(8):
    my_perc[:,j] = np.genfromtxt('list_perc_sem9bombas' + str(categoria) + ' quinzena ' + str(j + 1) + '.csv')
np.savetxt(categoria+'-prob.csv',my_perc,fmt='%1.2f')

my_perc = np.empty((22,8))
categoria = 'CI'
for j in range(8):
    my_perc[:,j] = np.genfromtxt('list_perc_sem9bombas' + str(categoria) + ' quinzena ' + str(j + 1) + '.csv')
np.savetxt(categoria+'-prob.csv',my_perc,fmt='%1.2f')

my_perc = np.empty((22,8))
categoria = 'CP'
for j in range(8):
    my_perc[:,j] = np.genfromtxt('list_perc_sem9bombas' + str(categoria) + ' quinzena ' + str(j + 1) + '.csv')
np.savetxt(categoria+'-prob.csv',my_perc,fmt='%1.2f')
