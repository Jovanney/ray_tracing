"""Main File"""

import numpy as np
from phong_with_args import refract
from vectors import Ponto, Vetor
from entidades import Mesh, Esfera, Plane
from camera import Camera
from ray_casting import RayCasting


def main():
    """Main Function"""

    p0 = Ponto(100, 0, 0)
    p1 = Ponto(0, 100, 0)
    p2 = Ponto(-100, 0, 0)
    p3 = Ponto(0, -100, 0)
    p4 = Ponto(0, 0, 100)

    v1 = p1 - p0
    v2 = p4 - p0
    normal1 = v1.__cross__(v2).__normalize__()

    v3 = p2 - p1
    v4 = p4 - p1
    normal2 = v3.__cross__(v4).__normalize__()

    v5 = p3 - p2
    v6 = p4 - p2
    normal3 = v5.__cross__(v6).__normalize__()

    v7 = p0 - p3
    v8 = p4 - p3
    normal4 = v7.__cross__(v8).__normalize__()

    camera = Camera(
        target=Ponto(2, 0, 0),
        position=Ponto(3, 1, 8),
        up=Vetor(0, 1, 0),
    )

    esfera_vermelha = Esfera(
        center=Ponto(3, 0, 0),
        radius=1,
        color=(1, 0, 0),
        k_difuso=0.8,
        k_ambiental=0.1,
        k_especular=0.1,
        n_rugosidade=1.0,
        k_reflexao=0.5,
        k_refracao=1.0,
        indice_refracao=1.0,
    )

    esfera_verde = Esfera(
        center=Ponto(0, 0, 0),
        radius=1,
        color=(0, 1, 0),
        k_difuso=0.8,
        k_ambiental=0.1,
        k_especular=0.6,
        n_rugosidade=1.0,
        k_reflexao=0.5,
        k_refracao=1.0,
        indice_refracao=0.3,
    )

    esfera_azul_nao = Esfera(
        center=Ponto(3, 0, -6),
        radius=2,
        color=(1, 1, 0),
        k_difuso=0.8,
        k_ambiental=0.1,
        k_especular=0.6,
        n_rugosidade=1.0,
        k_reflexao=0.5,
        k_refracao=1.0,
        indice_refracao=0.3,
    )

    esfera_azul = Esfera(
        center=Ponto(0, -3, 0),
        radius=1,
        color=(0, 0, 1),
        k_difuso=0.8,
        k_ambiental=0.1,
        k_especular=0.6,
        n_rugosidade=1.0,
        k_reflexao=0.7,
        k_refracao=0.9,
        indice_refracao=0.0,
    )

    ray_casting = RayCasting(hres=500, vres=500)

    mesh = Mesh(
        triangle_quantity=1,
        vertices_quantity=5,
        vertices=[p0, p1, p4],
        triangle_normals=[normal1, normal2, normal3, normal4],
        color=(0, 0, 1),
        triangle_tuple_vertices=[(0, 1, 2)],
        vertex_normals=[],
        k_difuso=0.8,
        k_ambiental=0.1,
        k_especular=0.1,
        n_rugosidade=1.0,
        k_reflexao=0.5,
        k_refracao=1.0,
        indice_refracao=1.0,
    )

    plano = Plane(
        point=Ponto(0, 0, 0),
        normal=Vetor(0, 1, 0),
        color=(1, 1, 0),
        k_difuso=0.7,
        k_especular=0.7,
        k_ambiental=0.1,
        k_reflexao=1.0,
        k_refracao=0.0,
        n_rugosidade=2.0,
        indice_refracao=1.0,
    )

    entidades = [esfera_vermelha, esfera_azul, esfera_verde]

    ray_casting.__generate_image__(entidades, 1, camera)

    # result = refract(np.array([0.707107, -0.707107]), np.array([0, 1]), 9, 10)


main()
