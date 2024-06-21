"""Main File"""

import numpy as np
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

    # caso com uma esfera
    # target=Ponto(2, 0, 2),
    # position=Ponto(2, -2.5, 2),
    #  [Luz(0, 0, 2, [255, 255, 255]), Luz(4, 0, 2, [255, 255, 255])],

    camera = Camera(
        target=Ponto(2, 0, 2),
        position=Ponto(2, -5, 3),
        up=Vetor(0, 0, 1),
    )

    # Metallic Plane
    plano = Plane(
        point=Ponto(0, 0, 1),
        normal=Vetor(0, 0, 1),
        color=(255, 255, 0),
        k_difuso=0.1,
        k_especular=0.9,
        k_ambiental=0.3,
        n_rugosidade=100,
    )

    # Opaque Sphere
    esfera2 = Esfera(
        center=Ponto(0.2, 1, 1),
        radius=0.7,
        color=(0, 255, 0),
        k_difuso=0.9,
        k_especular=0.1,
        k_ambiental=0.2,
        n_rugosidade=10,
    )

    esfera1 = Esfera(
        center=Ponto(2, 0, 1),
        radius=0.7,
        color=(255, 0, 0),
        k_difuso=0.7,
        k_especular=0.7,
        k_ambiental=0.1,
        k_reflexao=0.0,
        k_transmissao=0.0,
        n_rugosidade=1.0,
    )

    esfera3 = Esfera(
        center=Ponto(4, 1, 1),
        radius=0.7,
        color=(0, 0, 255),
        k_difuso=0.7,
        k_especular=0.7,
        k_ambiental=0.1,
        k_reflexao=0.0,
        k_transmissao=0.0,
        n_rugosidade=1.0,
    )

    ray_casting = RayCasting(hres=500, vres=500)

    mesh = Mesh(
        triangle_quantity=1,
        vertices_quantity=5,
        vertices=[p0, p1, p4],
        triangle_normals=[normal1, normal2, normal3, normal4],
        color=(0, 0, 255),
        triangle_tuple_vertices=[(0, 1, 2)],
        vertex_normals=[],
        k_difuso=0.7,
        k_especular=0.7,
        k_ambiental=0.1,
        k_reflexao=0.0,
        k_transmissao=0.0,
        n_rugosidade=2.0,
    )

    # esfera = Esfera(
    #     center=Ponto(20, 50, 70),
    #     radius=1,
    #     color=(255, 0, 0),
    #     k_ambiental=0.7,
    #     k_difuso=0.7,
    #     k_especular=0.7,
    #     n_rugosidade=10,
    # )

    # plano = Plane(
    #     point=Ponto(0, 0, 0),
    #     normal=Vetor(0, 1, 0),
    #     color=(255, 0, 0),
    # )

    entidades = [esfera2, esfera1, esfera3, plano]

    ray_casting.__generate_image__(entidades, 1, camera)


main()
