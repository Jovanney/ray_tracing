"""Módulo para cálculo de iluminação usando o modelo de Phong."""

import numpy as np

from entidades import Esfera, Plane, Mesh
from vectors import Ponto


def phong(entidade, luzes, ponto_intersec, camera_position):
    """
    Calcula a cor resultante em um ponto de interseção usando o modelo de Phong.

    Args:
        entity: A entidade (Esfera, Plano ou Malha) na qual a luz incide.
        lights: Lista de fontes de luz que incidem sobre a entidade.
        intersection_point: Ponto de interseção da luz com a entidade.
        camera_position: Posição da câmera.

    Returns:
        Uma lista representando a cor RGB resultante no ponto de interseção.
    """

    Ia = np.array([255, 255, 255])  # Intensisade da luz ambiente

    # Vetores
    # V é o vetor que vai do ponto de intersecção até a câmera
    # N é o vetor Normal do objeto
    # R é o vetor de reflexão
    # L Vetor que vai do ponto de intersecção até a fonte de luz

    V = np.array(
        [
            camera_position.x - ponto_intersec.x,
            camera_position.y - ponto_intersec.y,
            camera_position.z - ponto_intersec.z,
        ]
    )

    V /= np.linalg.norm(V)  # Normaliza o vetor V

    N = None

    if isinstance(entidade, Esfera):
        N = np.array(
            entidade.__get_normal_vector_to_intersection_point__(ponto_intersec)
        )

    elif isinstance(entidade, Plane):
        N = np.array(
            [
                entidade.normal.x,
                entidade.normal.y,
                entidade.normal.z,
            ]
        )

    elif isinstance(entidade, Mesh):
        N = np.array(
            [
                entidade.normal_to_intersection_point.x,
                entidade.normal_to_intersection_point.y,
                entidade.normal_to_intersection_point.z,
            ]
        )
    if N is not None:
        N /= np.linalg.norm(N)  # Normaliza a normal N

    # ka * Ia é o ambiente (luz ambiente)
    # Para cada ponto de luz nós iremos rodar a parte da direita da equação
    # Il * od * kd * (N.dot(L)) componente difusa
    # Il * ks * (R.dot(V)) ** n componente especular

    entidade.color = np.array(entidade.color)
    i_sum = np.array([0.0, 0.0, 0.0])

    for luz in luzes:
        luz.I = np.array(luz.I)
        L = np.array(
            [
                luz.x - ponto_intersec.x,
                luz.y - ponto_intersec.y,
                luz.z - ponto_intersec.z,
            ]
        )
        L /= np.linalg.norm(L)  # Normaliza o vetor L

        R = 2 * N * (N.dot(L)) - L
        R /= np.linalg.norm(R)  # Normaliza o vetor R

        N_dot_L = max(N.dot(L), 0)  # Garante que o produto escalar é não-negativo
        R_dot_V = max(R.dot(V), 0)  # Garante que o produto escalar é não-negativo

        if N_dot_L > 0:
            I_difusa = luz.I * entidade.color * entidade.k_difuso * N_dot_L
            I_especular = (
                luz.I * entidade.k_especular * (R_dot_V**entidade.n_rugosidade)
            )

            i_sum += I_difusa + I_especular

    cor = (entidade.k_ambiental * Ia) + i_sum
    cor_final = [min(255, max(0, int(i))) for i in cor]

    return cor_final
