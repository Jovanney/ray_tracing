"""Main File"""

from vectors import Ponto, Vetor
from entidades import Esfera, Plane
from camera import Camera
from ray_casting import RayCasting


def main():
    """Main Function"""

    camera = Camera(
        target=Ponto(5, 0, 0),
        position=Ponto(4, 100, 0),
        up=Vetor(0, 1, 0),
    )

    ray_casting = RayCasting(hres=300, vres=300)

    plano = Plane(
        point=Ponto(2, 0, 0),
        normal=Vetor(0, 1, 0),
        color=(255, 0, 0),
    )

    esfera = Esfera(
        center=Ponto(2, 0, 0),
        radius=0.25,
        color=(0, 128, 0),
    )

    esfera2 = Esfera(
        center=Ponto(4, 0, 0),
        radius=1,
        color=(128, 128, 0),
    )

    entidades = [esfera, esfera2, plano]

    ray_casting.__generate_image__(entidades, camera.target_distance, camera)


main()
