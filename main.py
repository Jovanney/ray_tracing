"""Main File"""

from vectors import Ponto, Vetor
from entidades import Esfera, Plane
from camera import Camera


def main():
    """Main Function"""

    camera = Camera(
        target=Ponto(0, 0, 0),
        position=Ponto(0, 0, 10),
        up=Vetor(0, 1, 0),
    )

    plano = Plane(
        point=Ponto(0, 0, 0),
        normal=Vetor(0, 0, 1),
        color=(255, 0, 0),
    )

    esfera = Esfera(
        center=Ponto(0, 0, 0),
        radius=1,
        color=(255, 0, 0),
    )

    entidades = [plano, esfera]

    camera.__ray_casting__(entidades)


main()
