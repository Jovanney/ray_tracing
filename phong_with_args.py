"""Módulo para cálculo de iluminação usando o modelo de Phong."""

import numpy as np
from fonte_de_luz import Luz
from ray import Ray
from entidades import Esfera, Plane, Mesh
from vectors import Ponto, Vetor


def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))


def find_closest_intersection(
    ray, entidades, profundidade_reflexao, profundidade_refracao
):
    """
    Encontra a entidade mais próxima e o ponto de interseção com base no raio fornecido.

    Args:
        ray: O raio a ser testado para interseção.
        entidades: Lista de entidades na cena.

    Returns:
        A entidade mais próxima e o ponto de interseção.
    """

    color = [0, 0, 0]
    min_distance = float("inf")

    for entidade in entidades:
        intersection = entidade.__intersect_line__(
            (ray.origin),
            (ray.direction),
        )
        if intersection:
            distance_vetor = Vetor(intersection[0], intersection[1], intersection[2])
            distance = ray.origin.__distance__(distance_vetor)

            if distance < min_distance:
                min_distance = distance
                color = phong(
                    entidade,
                    [
                        Luz(0, 5, 5, [255, 255, 255]),
                    ],
                    Ponto(intersection[0], intersection[1], intersection[2]),
                    ray.origin,
                    entidades,
                    profundidade_reflexao,
                    profundidade_refracao,
                )

    return color


def refract(V, N, n1, n2):
    """
    Calcula o vetor de refração usando a Lei de Snell.

    Args:
        V: Vetor incidente (direção do raio).
        N: Vetor normal no ponto de interseção.
        n1: Índice de refração do meio original.
        n2: Índice de refração do meio transmitido.

    Returns:
        O vetor refratado ou None se a refração total interna ocorrer.
    """
    if n2 == 0:
        return None

    n = n1 / n2
    cos_i = -np.dot(N, V)
    sin_t2 = n**2 * (1 - cos_i**2)

    if sin_t2 > 1:
        # Refração total interna
        return None

    cos_t = np.sqrt(1 - sin_t2)
    T = n * V + (n * cos_i - cos_t) * N
    return T / np.linalg.norm(T)


def phong(
    entidade,
    luzes,
    ponto_intersec,
    camera_position,
    entidades,
    profundidade_reflexao=0,
    profundidade_refracao=0,
):
    """
    Calcula a cor resultante em um ponto de interseção usando o modelo de Phong.

    Args:
        entidade: A entidade (Esfera, Plano ou Malha) na qual a luz incide.
        luzes: Lista de fontes de luz que incidem sobre a entidade.
        ponto_intersec: Ponto de interseção da luz com a entidade.
        camera_position: Posição da câmera.
        entidades: Lista de entidades na cena.
        profundidade_reflexao: Profundidade da recursão para reflexão.
        profundidade_refracao: Profundidade da recursão para refração.
        indice_ref_ambiente: Índice de refração do ambiente.

    Returns:
        Uma lista representando a cor RGB resultante no ponto de interseção.
    """

    if profundidade_reflexao >= 3 and profundidade_refracao >= 3:
        return [0, 0, 0]

    Ia = np.array([51, 51, 51])  # Intensidade da luz ambiente

    # Vetores
    V = np.array(
        [
            camera_position.x - ponto_intersec.x,
            camera_position.y - ponto_intersec.y,
            camera_position.z - ponto_intersec.z,
        ]
    )
    V = V / np.linalg.norm(V)  # Normaliza o vetor V

    N = None
    if isinstance(entidade, Esfera):
        N = np.array(
            entidade.__get_normal_vector_to_intersection_point__(ponto_intersec)
        )
    elif isinstance(entidade, Plane):
        N = np.array([entidade.normal.x, entidade.normal.y, entidade.normal.z])
    elif isinstance(entidade, Mesh):
        N = np.array(
            [
                entidade.normal_to_intersection_point.x,
                entidade.normal_to_intersection_point.y,
                entidade.normal_to_intersection_point.z,
            ]
        )
    if N is not None and np.linalg.norm(N) != 0:
        N = N / np.linalg.norm(N)  # Normaliza a normal N

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
        L = L / np.linalg.norm(L)  # Normaliza o vetor L

        R = 2 * N * (N.dot(L)) - L

        N_dot_L = clamp(0, N.dot(L), 1)
        R_dot_V = clamp(0, R.dot(V), 1)

        I_difusa = luz.I * entidade.color * entidade.k_difuso * N_dot_L
        I_especular = luz.I * entidade.k_especular * (R_dot_V**entidade.n_rugosidade)

        i_sum += I_difusa + I_especular

    cor = (entidade.k_ambiental * Ia) + i_sum

    # Adicionar reflexão recursiva
    if profundidade_reflexao < 3:
        refletido_direcao = 2 * N * (N.dot(V)) - V
        refletido_direcao = refletido_direcao / np.linalg.norm(
            refletido_direcao
        )  # Normaliza o vetor refletido
        refletido_origem = ponto_intersec
        raio_refletido = Ray(
            Ponto(refletido_origem.x, refletido_origem.y, refletido_origem.z),
            Vetor(refletido_direcao[0], refletido_direcao[1], refletido_direcao[2]),
        )

        cor_refletida = find_closest_intersection(
            raio_refletido,
            entidades,
            profundidade_reflexao=profundidade_reflexao + 1,
            profundidade_refracao=profundidade_refracao,
        )

        Ir = np.array(cor_refletida)
        cor = cor + entidade.k_reflexao * Ir

    # # Adicionar refração recursiva
    if profundidade_refracao < 3:
        if entidade.indice_refracao != 0:
            refracao_direcao = refract(V, N, n1=0, n2=entidade.indice_refracao)
            if refracao_direcao is not None:
                refracao_direcao = refracao_direcao / np.linalg.norm(
                    refracao_direcao
                )  # Normaliza o vetor refratado
                refracao_origem = ponto_intersec
                raio_refratado = Ray(
                    Ponto(refracao_origem.x, refracao_origem.y, refracao_origem.z),
                    Vetor(
                        refracao_direcao[0], refracao_direcao[1], refracao_direcao[2]
                    ),
                )

                cor_refratada = find_closest_intersection(
                    raio_refratado,
                    entidades,
                    profundidade_refracao=profundidade_refracao + 1,
                    profundidade_reflexao=profundidade_reflexao,
                )

                cor = cor + entidade.k_refracao * np.array(cor_refratada)

    cor_final = [min(255, max(0, int(i))) for i in cor]

    return cor_final
