"""Módulo para cálculo de iluminação usando o modelo de Phong."""

import numpy as np
from ray import Ray
from entidades import Esfera, Plane, Mesh
from vectors import Ponto, Vetor


def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

def find_closest_intersection(ray, entidades):
    """
    Encontra a entidade mais próxima e o ponto de interseção com base no raio fornecido.

    Args:
        ray: O raio a ser testado para interseção.
        entidades: Lista de entidades na cena.

    Returns:
        A entidade mais próxima e o ponto de interseção.
    """
    closest_entity = None
    closest_point = None
    min_distance = float('inf')

    for entidade in entidades:
        intersection = entidade.__intersect_line__(
            (ray.origin.x, ray.origin.y, ray.origin.z),
            (ray.direction.x, ray.direction.y, ray.direction.z)
        )
        if intersection:
            distance = np.linalg.norm(np.array([
                intersection[0] - ray.origin.x,
                intersection[1] - ray.origin.y,
                intersection[2] - ray.origin.z
            ]))
            if distance < min_distance:
                min_distance = distance
                closest_entity = entidade
                closest_point = Ponto(intersection[0], intersection[1], intersection[2])

    return closest_entity, closest_point

def phong(entidade, luzes, ponto_intersec, camera_position, entidades, profundidade = 0):
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

    Ia = np.array([51, 51, 51])  # Intensisade da luz ambiente

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

    V = V / np.linalg.norm(V)  # Normaliza o vetor V

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

    if N is not None or np.linalg.norm(N) != 0:
        # N /= np.linalg.norm(N)  # Normaliza a normal N
        N = N / np.linalg.norm(N)
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
        L = L / np.linalg.norm(L)  # Normaliza o vetor L

        R = 2 * N * (N.dot(L)) - L

        N_dot_L = clamp(0, N.dot(L), 1)
        R_dot_V = clamp(0, R.dot(V), 1)

        I_difusa = luz.I * entidade.color * entidade.k_difuso * N_dot_L
        I_especular = luz.I * entidade.k_especular * (R_dot_V**entidade.n_rugosidade)

        i_sum += I_difusa + I_especular

    cor = (entidade.k_ambiental * Ia) + i_sum

    # Adicionar reflexão recursiva
    if profundidade < 3:
        refletido_direcao = 2 * N * (N.dot(V)) - V
        refletido_direcao = refletido_direcao / np.linalg.norm(refletido_direcao)  # Normaliza o vetor refletido
        refletido_origem = ponto_intersec
        raio_refletido = Ray(
            Ponto(refletido_origem.x, refletido_origem.y, refletido_origem.z),
            Vetor(refletido_direcao[0], refletido_direcao[1], refletido_direcao[2])
        )
        
        
        entidade_refletida, ponto_intersecao_refletida = find_closest_intersection(raio_refletido, entidades)
        if entidade_refletida and ponto_intersecao_refletida:
            cor_refletida = phong(entidade_refletida, luzes, ponto_intersecao_refletida, camera_position, entidades, profundidade + 1)
            cor = cor + entidade.k_reflexao * np.array(cor_refletida) 

    cor_final = [min(255, max(0, int(i))) for i in cor]

    return cor_final

    
