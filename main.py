"""Main File"""

import numpy as np
from bsp import build_bsp, print_bsp_tree
from vectors import Ponto, Vetor
from entidades import Mesh, Plane
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

    p6 = Ponto(0.5, -1, 1)
    p7 = Ponto(1.5, -1, 1)
    p8 = Ponto(1, 1, 1)

    # Calculate normal for the third triangle
    v5 = p7 - p6
    v6 = p8 - p6
    normal3 = v5.__cross__(v6).__normalize__()

    # Define camera
    camera = Camera(
        target=Ponto(1, -1, 1),
        position=Ponto(1, 5, 1),
        up=Vetor(0, 0, 1),
    )

    # Build BSP tree

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

    triangle3 = Mesh(
        triangle_quantity=1,
        vertices_quantity=3,
        vertices=[p6, p7, p8],
        triangle_normals=[normal3],
        color=(0, 255, 0),
        triangle_tuple_vertices=[(0, 1, 2)],
        vertex_normals=[],
    )

    entidades = [triangle, triangle2, triangle3]

    root = build_bsp(entidades)

    print_bsp_tree(root)
    # Generate image
    # ray_casting.__generate_image__(entidades, 1, camera)


main()
