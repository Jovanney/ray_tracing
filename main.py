"""Main File"""

import numpy as np
from bsp import build_bsp
from vectors import Ponto, Vetor
from entidades import Mesh, Esfera, Plane
from camera import Camera
from ray_casting import RayCasting


def main():
    """Main Function"""

    # Define vertices of the triangle
    p0 = Ponto(0, 0, 0)
    p1 = Ponto(2, 0, 0)
    p2 = Ponto(1, 0, 2)

    # Calculate normal for the triangle
    v1 = p1 - p0
    v2 = p2 - p0
    normal = v1.__cross__(v2).__normalize__()

    # Define vertices of the second triangle (behind the first triangle)
    p3 = Ponto(-1, -2, 0)
    p4 = Ponto(3, -2, 0)
    p5 = Ponto(1, -2, 3)

    # Calculate normal for the second triangle
    v3 = p4 - p3
    v4 = p5 - p3
    normal2 = v3.__cross__(v4).__normalize__()

    # Define spheres
    esfera_metalica = Esfera(
        center=Ponto(0, -1, 3),
        radius=1,
        color=(255, 0, 0),
    )

    esfera_opaca = Esfera(
        center=Ponto(2, -1, 3),
        radius=1,
        color=(0, 0, 255),
    )

    esfera_3 = Esfera(
        center=Ponto(-2, -1, 3),
        radius=1,
        color=(0, 255, 0),
    )

    esfera_exemplo_2 = Esfera(
        center=Ponto(0.2, 1, 3),
        radius=0.7,
        color=(0, 255, 0),
    )

    # Define camera
    camera = Camera(
        target=Ponto(1, -1, 1),
        position=Ponto(1, 5, 1),
        up=Vetor(0, 0, 1),
    )

    # Define planes
    plano = Plane(
        point=Ponto(0, -1, 3),
        normal=Vetor(0, 0, -1),
        color=(255, 255, 0),
    )

    plano_atras = Plane(
        point=Ponto(0, -1, 5),  # Behind the existing plane
        normal=Vetor(0, 0, -1),
        color=(255, 0, 255),
    )

    plano_frente = Plane(
        point=Ponto(0, -1, 1),  # In front of the existing plane
        normal=Vetor(0, 0, -1),
        color=(0, 255, 255),
    )

    plano_meio = Plane(
        point=Ponto(0, -1, 3),  # Intersecting the existing plane
        normal=Vetor(1, 0, 0),  # Different normal to ensure intersection
        color=(255, 255, 255),
    )

    # Build BSP tree
    # bsp_tree = build_bsp([plano, plano_atras, plano_frente, plano_meio])

    # print(bsp_tree)

    # Define ray casting
    ray_casting = RayCasting(hres=500, vres=500)

    # Define triangle mesh
    triangle = Mesh(
        triangle_quantity=1,
        vertices_quantity=3,
        vertices=[p0, p1, p2],
        triangle_normals=[normal],
        color=(0, 0, 255),
        triangle_tuple_vertices=[(0, 1, 2)],
        vertex_normals=[],
    )

    triangle2 = Mesh(
        triangle_quantity=1,
        vertices_quantity=3,
        vertices=[p3, p4, p5],
        triangle_normals=[normal2],
        color=(255, 0, 0),
        triangle_tuple_vertices=[(0, 1, 2)],
        vertex_normals=[],
    )

    # bsp_tree = build_bsp([triangle])
    # Add entities
    entidades = [triangle, triangle2]

    # Generate image
    ray_casting.__generate_image__(entidades, 1, camera)


main()
