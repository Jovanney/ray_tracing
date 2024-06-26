import numpy as np

from entidades import Esfera, Plane, Mesh
from vectors import Ponto


def phong(entidade, luzes, ponto_intersec, camera_position):
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

    V = V / np.linalg.norm(V)  # Normaliza o vetor V

    if isinstance(entidade, Esfera):
        N = np.array(
            entidade.__get_normal_vector_to_intersection_point__(ponto_intersec)
        )

        N = N / np.linalg.norm(N)  # Normaliza a normal N

    elif isinstance(entidade, Plane):
        N = np.array(
            [
                entidade.normal.x,
                entidade.normal.y,
                entidade.normal.z,
            ]
        )

        N = N / np.linalg.norm(N)  # Normaliza a normal N

    elif isinstance(entidade, Mesh):
        intersection_point = None
        for index, triangle in enumerate(entidade.triangle_tuple_vertices):
            triangle_vertices = [entidade.vertices[i] for i in triangle]
            triangle_normal = entidade.triangle_normals[index]
            plane = Plane(triangle_vertices[0], triangle_normal, entidade.color)
            intersection_point = plane.__intersect_line__(ponto_intersec, V)
            if intersection_point is not None:
                intersection_point = Ponto(
                    intersection_point[0], intersection_point[1], intersection_point[2]
                )
                if entidade.__point_in_triangle__(
                    intersection_point, triangle_vertices
                ):
                    N = np.array(
                        [triangle_normal.x, triangle_normal.y, triangle_normal.z]
                    )
                    break

        if intersection_point is not None:
            N = N / np.linalg.norm(N)  # Normaliza a normal N

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
        R = R / np.linalg.norm(R)  # Normaliza o vetor R

        N_dot_L = max(N.dot(L), 0)  # Garante que o produto escalar é não-negativo
        R_dot_V = max(R.dot(V), 0)  # Garante que o produto escalar é não-negativo

        I_difusa = luz.I * entidade.color * entidade.k_difuso * N_dot_L
        I_especular = luz.I * entidade.k_especular * (R_dot_V**entidade.n_rugosidade)

        I = I_difusa + I_especular
        i_sum += I

    cor = (entidade.k_ambiental * Ia) + i_sum

    cor_final = [min(255, max(0, int(i))) for i in cor]

    return cor_final
