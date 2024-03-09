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
    #Definindo em qual canal da UE está alocada:
    Canal_UE = canal_UE(K, N)
    B_c = B_t / N
    Capacidade = np.zeros(K)

    for i in range(K):
        x_coord[i] = random.random() * 1000
        y_coord[i] = random.random() * 1000
        distanciaAPUE[i] = dAPUE(x_coord, y_coord, K)[i]
        potencia_recebida[i] = pot_rec(p_t, distanciaAPUE[i], d_0)
       
    for i in range(K):
        # Criar lista de índices de outros equipamentos no mesmo canal
        outros_no_mesmo_canal = [n for n in range(K) if Canal_UE[n] == Canal_UE[i] and n != i]

        # Calcular interferência apenas para os equipamentos no mesmo canal
        interferencia = np.sum([potencia_recebida[n] for n in outros_no_mesmo_canal])
        
        # Calcular SINR apenas se houver interferência
        if interferencia > 0:
            outras_estacoes = np.delete(potencia_recebida, i)
            interferencia = np.sum(outras_estacoes)
            SNR_SINR[i] = potencia_recebida[i] / (interferencia + p_n)
        else:
            SNR_SINR[i] = potencia_recebida[i]/p_n

        # Calcular a capacidade
        Capacidade[i] = B_c * np.log2(1 + SNR_SINR[i])
        

    return Capacidade

########################################################################################################################################
B_t, p_t, d_0, K_0 = 100e6, 1e3, 1, 1e-17 # Em MHz, mW, metros, mW/Hz respectivamente
M, K, N = 1, 15, 9 #Número de APs, UEs e Canais respectivamente

# Número de iterações
num_iteracoes = 8000

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