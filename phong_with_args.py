import numpy as np

from entidades import Esfera
from fonte_de_luz import Luz
from vectors import Ponto


# od é a cor do objeto
def phong(entidade, luzes, ponto_intersec, camera_position):
    # Cores
    Ia = np.array([255, 255, 255])  # Intensisade da luz ambiente

    # Vetores
    # L Vetor que vai do ponto de intersecção até a fonte de luz
    # N é o vetor Normal do objeto

    if isinstance(entidade, Esfera):
        N = np.array(
            entidade.__get_normal_vector_to_intersection_point__(ponto_intersec)
        )

        V = np.array(
            [
                camera_position.x - ponto_intersec.x,
                camera_position.y - ponto_intersec.y,
                camera_position.z - ponto_intersec.z,
            ]
        )

    # ka * Ia é o ambiente (luz ambiente)
    # Para cada ponto de luz nós iremos rodar a parte da direita da equação
    # Il * od * kd * (N.dot(L)) componente difusa
    # Il * ks * (R.dot(V)) ** n componente especular

    entidade.color = np.array(entidade.color)

    for luz in luzes:
        luz.I = np.array(luz.I)
        if isinstance(entidade, Esfera):
            L = np.array(
                [
                    luz.x - ponto_intersec.x,
                    luz.y - ponto_intersec.y,
                    luz.z - ponto_intersec.z,
                ]
            )

            R = 2 * (N.dot(L)) * N - L

            I = luz.I * entidade.color * entidade.k_difuso * (
                N.dot(L)
            ) + luz.I * entidade.k_especular * ((R.dot(V)) ** entidade.n_rugosidade)

    cor = (entidade.k_ambiental * Ia) + I

    return [min(255, i) for i in cor]


esfera = Esfera(
    center=Ponto(0, 0, 0),
    radius=50,
    color=(255, 0, 0),
    k_ambiental=0.7,
    k_difuso=0.7,
    k_especular=0.7,
    n_rugosidade=10,
)

phong(esfera, [Luz(0, 0, 0, [255, 255, 255])], Ponto(0, 0, 0), Ponto(100, 200, 100))
