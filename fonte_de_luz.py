"""Módulo que contém a classe FonteDeLuz"""


class Luz:
    """Classe que representa uma fonte de luz no espaço tridimensional

    - Cada luz é um ponto, que determina sua localização --->  l(x, y, z) onde,x, y e z e R.
    - Intensidade da luz, uma cor RGB
    """

    def __init__(self, x, y, z, I):
        self.x = x
        self.y = y
        self.z = z
        self.I = I
