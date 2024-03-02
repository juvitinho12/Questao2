import numpy as np
import random
import matplotlib.pyplot as plt

def pot_rec(pot_trans, dist, d_0):
    c = 1e-4
    n = 4
    pot_rec_result = 0  # Inicializa a variável local

    if dist >= d_0:
        pot_rec_result = pot_trans * (c / ((dist) ** n))

    return pot_rec_result

def dAPUE(x_coord, y_coord, K): #K é o número de UEs
  dAPUE = np.array(K)
  for i in range(K):
    dAPUE[i] = np.linalg.norm(np.array([x_coord[i], y_coord[i]]) - np.array([500,500]))
  return dAPUE


def simular_experimento(B_t, p_t, d_0, K_0, M, N, K):
    x_coord = np.zeros(K)
    y_coord = np.zeros(K)
    distanciaAPUE = np.zeros(K)
    potencia_recebida = np.zeros(K)
    p_n = K_0 * (B_t / N)
    SNR = []
    SINR = []

    for i in range(K):
        x_coord[i] = random.random() * 1000
        y_coord[i] = random.random() * 1000
        distanciaAPUE[i] = dAPUE(x_coord[i], y_coord[i], K)
        potencia_recebida[i] = pot_rec(p_t, distanciaAPUE[i], d_0)
    


    B_c = B_t / N
    Capacidade = np.zeros(K)

    #Penso em fazer a condicional de ser cálculo de SNR ou SINR no mesmo laço for, assim com isso eu posso colocar quando o valor for igual a 0 ser nulo, para que assim eu junte os vetores num só para melhor cálculo da SINR
    SNR_SINR = np.concatenate((SNR, SINR))
    for i in range(K):
      Capacidade[i] = B_c * np.log2(1+SNR_SINR)

    return Capacidade
'''Cálculo da SINR em laço for:
            outras_estacoes = np.delete(potencia_recebida, i)
            interferencia = np.sum(outras_estacoes)
            SINR[i] = potencia_recebida[i] / (interferencia + p_n)'''



########################################################################################################################################
B_t, p_t, d_0, K_0 = 100e6, 1e3, 1, 1e-17 # Em MHz, mW, metros, mW/Hz respectivamente
M, K, N = 1, 10, 9 #Número de APs, UEs e Canais respectivamente

# Número de iterações
num_iteracoes = 1000

# Armazenar todas as capacidades
Capacidade_total = []

# Iteração
for i in range(num_iteracoes):
    Capacidade_iteracao = simular_experimento(B_t, p_t, d_0, K_0, M, N, K)
    Capacidade_total = np.concatenate((Capacidade_total, Capacidade_iteracao))

#Deixando em ordem crescente
x = np.sort(Capacidade_total)

# Plotar apenas o eixo x em decibéis
plt.xlabel('Capacidade')
plt.ylabel('Porcentagem')
plt.title('CDF da Capacidade')

plt.plot(x, np.arange(0, len(Capacidade_total)) / len(Capacidade_total))
plt.show()