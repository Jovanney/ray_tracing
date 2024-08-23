"""Main File"""

import math
import numpy as np
from vectors import Ponto, Vetor
from entidades import Mesh, Esfera, Plane
from camera import Camera
from ray_casting import RayCasting
from toro import Toro
from EsferaTexturizada import EsferaTexturizada


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
        target=Ponto(0, -1, 3),
        position=Ponto(0, -1, -5),
        up=Vetor(0, 1, 0),
    )    

    ray_casting = RayCasting(hres=500, vres=500)

    esfera_texturizada = EsferaTexturizada(
    center=Ponto(0, -1, 0),
    radius=1,
    texture_path="ray_tracing\globo2.png",
    k_difuso=0.8,
    k_especular=0.1,
    k_ambiental=0.1,
    k_reflexao=0.0,
    k_refracao=0.0,
    n_rugosidade=1.0,
    )   

    esfera = Esfera(
        center=Ponto(0, -2, 0),
        radius=1,
        color=[0, 1, 0],
        k_difuso=0.7,
        k_especular=0.0,
        k_ambiental=0.0,
        k_reflexao=0.0,
        k_refracao=0.0,
        n_rugosidade=1.0,
    )

    esfera3 = Esfera(
        center=Ponto(2, 1, 2),
        radius=0.7,
        color=(0, 0, 1),
        k_difuso=0.7,
        k_especular=0.0,
        k_ambiental=0.0,
        k_reflexao=0.0,
        k_refracao=0.0,
        n_rugosidade=1.0,
    )
  

    entidades = [esfera_texturizada]

    ray_casting.__generate_image__(entidades, 1, camera)

main()
