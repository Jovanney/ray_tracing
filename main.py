"""Main File"""

import numpy as np
from vectors import Ponto, Vetor
from entidades import Mesh
from camera import Camera
from ray_casting import RayCasting
from transformation import Transformacao


def main():
    """Main Function"""

    p0 = Ponto(100, 0, 0)
    p1 = Ponto(0, 100, 0)
    p2 = Ponto(-100, 0, 0)
    p3 = Ponto(0, -100, 0)
    p4 = Ponto(0, 0, 100)

    v1 = p1.__sub__(p0)
    v2 = p4.__sub__(p0)
    normal1 = v1.__cross__(v2).__normalize__()

    v3 = p2.__sub__(p1)
    v4 = p4.__sub__(p1)
    normal2 = v3.__cross__(v4).__normalize__()

    v5 = p3.__sub__(p2)
    v6 = p4.__sub__(p2)
    normal3 = v5.__cross__(v6).__normalize__()

    v7 = p0.__sub__(p3)
    v8 = p4.__sub__(p3)
    normal4 = v7.__cross__(v8).__normalize__()

    camera = Camera(
        target=Ponto(0, 0, 0),
        position=Ponto(100, 200, 100),
        up=Vetor(0, 1, 0),
    )

    ray_casting = RayCasting(hres=500, vres=500)

    # plano = Plane(
    #     point=Ponto(2, 0, 0),
    #     normal=Vetor(0, 1, 0),
    #     color=(255, 0, 0),
    # )

    # esfera = Esfera(
    #     center=Ponto(2, 0, 0),
    #     radius=0.25,
    #     color=(0, 128, 0),
    # )

    # esfera2 = Esfera(
    #     center=Ponto(4, 0, 0),
    #     radius=1,
    #     color=(128, 128, 0),
    # )

    mesh = Mesh(
        triangle_quantity=4,
        vertices_quantity=5,
        vertices=[p0, p1, p2, p3, p4],
        triangle_normals=[normal1, normal2, normal3, normal4],
        color=(0, 0, 255),
        triangle_tuple_vertices=[(0, 1, 4), (1, 2, 4), (2, 3, 4), (0, 3, 4)],
        vertex_normals=[],
    )

    angulo_180 = np.pi
    angulo_120 = np.pi / 3
    matriz_rotacao_y = Transformacao.criar_matriz_rotacao_y(angulo_180)
    matriz_rotacao_x = Transformacao.criar_matriz_rotacao_x(angulo_120)
    matriz_rotacao = matriz_rotacao_x @ matriz_rotacao_y

    mesh = Transformacao.aplicar_transformacao_malha(mesh, matriz_rotacao)

    entidades = [mesh]

    ray_casting.__generate_image__(entidades, 1, camera)


main()
