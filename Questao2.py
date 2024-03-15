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

def dAPUE(x_coord, y_coord, K):
    dAPUE = np.zeros(K)
    AP_pos = np.array([500, 500])
    for i in range(K):
        dAPUE[i] = np.linalg.norm(np.array([x_coord[i], y_coord[i]]) - AP_pos)
    return dAPUE



def canal_UE(K, N):
    UE = np.zeros(K)

    if K == N:
        # Quando o número de canal é igual ao número de UE
        for i in range(N):
            UE[i] = i
    elif K < N:
        # Quando eu tenho mais canal do que UE
        for i in range(K):
            UE[i] = i
    else:
        # Quando eu tenho mais UE do que canal
        for i in range(K):
            if i < N:
                UE[i] = i
            else:
                UE[i] = np.random.randint(0, N)
                

    return UE

def simular_experimento(B_t, p_t, d_0, K_0, M, N, K):
    x_coord = np.zeros(K)
    y_coord = np.zeros(K)
    distanciaAPUE = np.zeros(K)
    potencia_recebida = np.zeros(K)
    p_n = K_0 * (B_t / N)
    SNR_SINR = np.zeros(K)
    Canal_UE = np.zeros(K)
    #Definindo em qual canal da UE está alocada:
    for i in range(K):
        Canal_UE[i] = canal_UE(K, N)[i]
    B_c = B_t / N
    Capacidade = np.zeros(K)
    Capacidade_db = np.zeros(K)

    for i in range(K):
        x_coord[i] = random.random() * 1000
        y_coord[i] = random.random() * 1000
        distanciaAPUE[i] = dAPUE(x_coord, y_coord, K)[i]
        potencia_recebida[i] = pot_rec(p_t, distanciaAPUE[i], d_0)
       
    for i in range(K):
        for n in range(K):
            if Canal_UE[n] == Canal_UE[i] and n != i:
                outras_estacoes = np.delete(potencia_recebida, i)
                interferencia_do_canal = np.sum(outras_estacoes)
                SNR_SINR[i] = potencia_recebida[i] / (interferencia_do_canal + p_n)

            else:
                SNR_SINR[i] = potencia_recebida[i]/p_n

        # Calcular a capacidade
        Capacidade[i] = B_c * np.log2(1 + SNR_SINR[i])
        

    return Capacidade

########################################################################################################################################
B_t, p_t, d_0, K_0 = 100e6, 1e3, 1, 1e-17 # Em MHz, mW, metros, mW/Hz respectivamente
M, K1, N1 = 1, 1, 1 #Número de APs, UEs e Canais respectivamente
K2, N2, K3, N3, K4, N4, K5, N5 = 1, 5, 60, 30, 16, 20, 100, 40


# Número de iterações
num_iteracoes1 = 60000
num_iteracoes2 = 60000
num_iteracoes3 = 1000
num_iteracoes4 = 3750
num_iteracoes5 = 600


# Armazenar todas as capacidades
Capacidade_total1 = []
Capacidade_total2 = []
Capacidade_total3 = []
Capacidade_total4 = []
Capacidade_total5 = []

# Iteração
for i in range(num_iteracoes1):
    Capacidade_iteracao1 = simular_experimento(B_t, p_t, d_0, K_0, M, N1, K1)
    Capacidade_total1 = np.concatenate((Capacidade_total1, Capacidade_iteracao1))

for i in range(num_iteracoes2):
    Capacidade_iteracao2 = simular_experimento(B_t, p_t, d_0, K_0, M, N2, K2)
    Capacidade_total2 = np.concatenate((Capacidade_total2, Capacidade_iteracao2))

for i in range(num_iteracoes3):   
    Capacidade_iteracao3 = simular_experimento(B_t, p_t, d_0, K_0, M, N3, K3)
    Capacidade_total3 = np.concatenate((Capacidade_total3, Capacidade_iteracao3))

for i in range(num_iteracoes4):
    Capacidade_iteracao4 = simular_experimento(B_t, p_t, d_0, K_0, M, N4, K4)
    Capacidade_total4 = np.concatenate((Capacidade_total4, Capacidade_iteracao4))

for i in range(num_iteracoes5):
    Capacidade_iteracao5 = simular_experimento(B_t, p_t, d_0, K_0, M, N5, K5)
    Capacidade_total5 = np.concatenate((Capacidade_total5, Capacidade_iteracao5))

#Deixando em ordem crescente
x1 = np.sort(Capacidade_total1)
x2 = np.sort(Capacidade_total2)
x3 = np.sort(Capacidade_total3)
x4 = np.sort(Capacidade_total4)
x5 = np.sort(Capacidade_total5)

plt.plot(x1, np.arange(0, len(Capacidade_total1)) / len(Capacidade_total1), label = '1 UE e 1 Canal')
plt.plot(x2, np.arange(0, len(Capacidade_total1)) / len(Capacidade_total1), label = '1 UE e 5 Canais')
plt.plot(x3, np.arange(0, len(Capacidade_total1)) / len(Capacidade_total1), label = '60 UEs e 30 Canais')
plt.plot(x4, np.arange(0, len(Capacidade_total1)) / len(Capacidade_total1), label = '16 UEs e 20 Canais')
plt.plot(x5, np.arange(0, len(Capacidade_total1)) / len(Capacidade_total1), label = '100 UEs e 40 Canais')
plt.legend()


# Plotar apenas o eixo x em decibéis
plt.xlabel('Capacidade')
plt.ylabel('Porcentagem')
plt.title('CDF da Capacidade')
plt.show()