import numpy as np


# od é a cor do objeto
def phong_model(od):
    # Coeficientes de iluminação
    kd = np.array(
        [0.7, 0.7, 0.7]
    )  # difuso, é o efeito de iluminação que faz com que a luz se espalhe uniformemente
    ks = np.array(
        [0.5, 0.5, 0.5]
    )  # especular é o efeito de iluminação que faz com que a luz se espalhe em um ponto
    ka = np.array([0.1, 0.1, 0.1])  # atenuador da luz ambiente
    kr = np.array([0.5, 0.5, 0.5])  # reflexão, o quão reflexivo ele é
    kt = np.array([0.5, 0.5, 0.5])  # transmissão, o quão transmissivo ele é
    n = 10  # coeficiente de rugosidade, o qual rugoso ele é (afeta a especularidade)

    # Cores
    Ia = np.array([255, 255, 255])  # Intensisade da luz (luz branca)
    Il = np.array([255, 255, 255])  # Intensidade da luz (luz branca)

    # Vetores
    L = np.array([1, 1, 1])
    N = np.array([1, 1, 1])
    V = np.array([1, 1, 1])
    R = np.array([1, 1, 1])

    # ka * Ia é o ambiente (luz ambiente)
    # Para cada ponto de luz nós iremos rodar a parte da direita da equação
    # Il * od * kd * (N.dot(L)) componente difusa
    # Il * ks * (R.dot(V)) ** n componente especular

    I = ka * Ia + (Il * od * kd * (N.dot(L)) + Il * ks * (R.dot(V)) ** n)

    return I
