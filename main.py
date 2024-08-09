"""Main File"""

import numpy as np
from phong_with_args import refract
from vectors import Ponto, Vetor
from entidades import Mesh, Esfera, Plane
from camera import Camera
from ray_casting import RayCasting


def main():
    """Main Function"""

    p0 = Ponto(10, 0, 0)
    p1 = Ponto(0, 10, 0)
    p2 = Ponto(-10, 0, 0)
    p3 = Ponto(0, -10, 0)
    p4 = Ponto(0, 0, 10)

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

    esfera_vermelha2 = Esfera(
        center=Ponto(3, 0, -5),
        radius=3,
        color=(1, 1, 0),
        k_difuso=0.8,
        k_ambiental=0.1,
        k_especular=0.1,
        n_rugosidade=1.0,
        k_reflexao=0.5,
        k_refracao=1.0,
        indice_refracao=0.0,
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

    esfera_rosa = Esfera(
        center=Ponto(0, 3, 5),
        radius=1,
        color=(255, 0, 255),
        k_difuso=0.8,
        k_ambiental=0.1,
        k_especular=0.6,
        n_rugosidade=1.0,
        k_reflexao=0.0,
        k_refracao=0.0,
        indice_refracao=0.0,
    )

    esfera_azul = Esfera(
        center=Ponto(1, 3, 5),
        radius=1,
        color=(0, 0, 255),
        k_difuso=0.8,
        k_ambiental=0.1,
        k_especular=0.6,
        n_rugosidade=1.0,
        k_reflexao=0.7,
        k_refracao=0.3,
        indice_refracao=1.0,
    )

    esfera_rosa_2 = Esfera(
        center=Ponto(3, -3, -20),
        radius=4,
        color=(1, 1, 0),
        k_difuso=0.8,
        k_ambiental=0.1,
        k_especular=0.6,
        n_rugosidade=1.0,
        k_reflexao=0.7,
        k_refracao=0.9,
        indice_refracao=0.0,
    )

    ray_casting = RayCasting(hres=500, vres=500)

    esfera_vermelha = Esfera(
        center=Ponto(3, 0, 0),
        radius=1,
        color=(1, 0, 0),
        k_difuso=0.8,
        k_ambiental=0.1,
        k_especular=0.1,
        n_rugosidade=1.0,
        k_reflexao=1.0,
        k_refracao=0.9,
        indice_refracao=1.5,
    )

    mesh = Mesh(
        triangle_quantity=1,
        vertices_quantity=3,
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

    camera = Camera(
        target=Ponto(0, 3, 5),
        position=Ponto(0, -1, 10),
        up=Vetor(0, 1, 0),
    )

    plano = Plane(
        point=Ponto(0, -1, 3),
        normal=Vetor(0, 0, -1),
        color=(255, 255, 0),
        k_difuso=0.8,
        k_ambiental=0.1,
        k_especular=0.1,
        n_rugosidade=1.0,
        k_reflexao=1.0,
        indice_refracao=10,
        k_refracao=1.0,
        texture_image_path="minecraft.webp",
    )

    plano_2 = Plane(
        point=Ponto(0, -1, 3),
        normal=Vetor(0, 0, -1),
        color=(255, 255, 0),
        k_difuso=0.8,
        k_ambiental=0.1,
        k_especular=0.1,
        n_rugosidade=1.0,
        k_reflexao=1.0,
        indice_refracao=10,
        k_refracao=1.0,
        texture_image_path="minecraft.webp",
    )

    esfera_metalica = Esfera(
        center=Ponto(0, -1, 3),
        radius=1,
        color=(1, 0, 0),
        k_difuso=0.8,  # Lower diffuse reflection
        k_especular=0.9,  # High specular reflection
        k_ambiental=0.3,  # Ambient reflection usually remains low
        n_rugosidade=50,
        k_reflexao=1.0,
        # Higher roughness for sharper specular highlights
    )
    entidades = [plano, esfera_rosa, esfera_azul]

    ray_casting.__generate_image__(entidades, 1, camera)


main()
