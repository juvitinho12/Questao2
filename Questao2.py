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

def distribuir_APs(M): #M é o número de APs
    if M not in [1, 4, 9, 16, 25, 36, 49, 64]:
        return None

    tamanho_quadrado = 1000
    lado_quadrado = int(np.sqrt(M))

    tamanho_celula = tamanho_quadrado // lado_quadrado

    # Criar coordenadas usando meshgrid
    x, y = np.meshgrid(np.arange(0.5 * tamanho_celula, tamanho_quadrado, tamanho_celula),
                      np.arange(0.5 * tamanho_celula, tamanho_quadrado, tamanho_celula))

    coordenadas_APs = np.column_stack((x.ravel(), y.ravel()))

    return coordenadas_APs

def dAPUE(x_coord, y_coord, K, M): #K é o número de UEs e M é a coordenada da AP
  dAPUE = []
  for i in range(K):
    dAPUE[i] = np.linalg.norm(np.array([x_coord[i], y_coord[i]]) - M)
  return dAPUE


def simular_experimento(B_t, p_t, d_0, K_0, M, N, K):
    x_coord = []
    y_coord = []
    distanciaAPUE = []
    coord_AP = distribuir_APs(M)
    potencia_recebida = []
    p_n = K_0 * (B_t / N)
    SNR = []
    SINR = []
    capacidade = []

    for i in range(K):
        x_coord[i] = random.random() * 1000
        y_coord[i] = random.random() * 1000
        distanciaAPUE[i] = dAPUE(x_coord[i], y_coord[i], K, coord_AP)
        potencia_recebida[i] = pot_rec(p_t, distanciaAPUE[i], d_0)
        if N <= K:
            SNR[i] = potencia_recebida[i]/p_n
        else:
            outras_estacoes = np.delete(potencia_recebida, i)
            interferencia = np.sum(outras_estacoes)
            SINR[i] = potencia_recebida[i] / (interferencia + p_n)
    B_c = B_t / N
    snr_2 = np.sum(SNR)
    Capacidade = []
    if N <= K:
      Capacidade = B_c * np.log2(1+snr_2)
    else:
       for i in range(K):
          Capacidade[i] == B_c * np.log2(1+SINR)
    return Capacidade