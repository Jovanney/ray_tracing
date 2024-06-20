import numpy as np


def phong_model():
    # Coeficientes de iluminação
    kd = np.array(
        [0.7, 0.7, 0.7]
    )  # difuso, é o efeito de iluminação que faz com que a luz se espalhe uniformemente
    ks = np.array(
        [0.5, 0.5, 0.5]
    )  # especular é o efeito de iluminação que faz com que a luz se espalhe em um ponto
    ka = np.array([0.1, 0.1, 0.1])  # ambiental
    kr = np.array([0.5, 0.5, 0.5])  # reflexão
    kt = np.array([0.5, 0.5, 0.5])  # transmissão
    n = 10  # coeficiente de rugosidade

    # Cores
    Ia = np.array([255, 255, 255])
    Il = np.array([255, 255, 255])

    # Vetores
    L = np.array([1, 1, 1])
    N = np.array([1, 1, 1])
    V = np.array([1, 1, 1])
    R = np.array([1, 1, 1])

    # Cálculo da intensidade
    Id = kd * Il * max(0, np.dot(L, N))
    Is = ks * Il * max(0, np.dot(V, R)) ** n
    Ia = ka * Ia
    I = Id + Is + Ia
    return I
