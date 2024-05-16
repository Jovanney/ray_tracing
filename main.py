"""Main File"""

from vectors import Ponto, Vetor
from entidades import Esfera, Plane
from camera import Camera


def main():
    """Main Function"""

    camera = Camera(
        target=Ponto(2, 0, 0),
        position=Ponto(0, 1, 0),
        up=Vetor(0, 1, 0),
    )

    plano = Plane(
        point=Ponto(0, 1, 0),
        normal=Vetor(0, -1, 0),
        color=(255, 0, 0),
    )

    esfera = Esfera(
        center=Ponto(2, 0, 0),
        radius=0.25,
        color=(0, 128, 0),
    )

    entidades = [plano, esfera]

    camera.__ray_casting__(entidades)


main()
