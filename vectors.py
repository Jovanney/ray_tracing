"""Module for Vector Operations"""
import numpy as np
import math


class Ponto:
    """Class Representing a Point in 3D Space"""

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, p):
        return Ponto(self.x + p.x, self.y + p.y, self.z + p.z)

    def __sub__(self, p):
        # print(
        #     f"inicial: ({self.x}, {self.y}, {self.z})", f"final: ({p.x}, {p.y}, {p.z})"
        # )

        vetor_resultado = Vetor(self.x - p.x, self.y - p.y, self.z - p.z)
        # print("vetor resultante: ", vetor_resultado.__dict__)
        return vetor_resultado

    def __distance__(self, p):
        return ((self.x - p.x) ** 2 + (self.y - p.y) ** 2 + (self.z - p.z) ** 2) ** 0.5

    def __print__(self):
        print(f"({self.x}, {self.y}, {self.z})")


class Vetor(Ponto):
    """Class Representing a Vector in 3D Space"""

    def __mul__(self, p):
        return self.x * p.x + self.y * p.y + self.z * p.z

    def __mul_escalar__(self, escalar):
        if isinstance(escalar, (int, float)):
            return Vetor(self.x * escalar, self.y * escalar, self.z * escalar)
        else:
            raise TypeError("Multiplicação de vetor só é suportada por escalares.")
        
    def as_array(self):
        return np.array([self.x, self.y, self.z])

    def __cross__(self, p):
        return Vetor(
            self.y * p.z - self.z * p.y,
            self.z * p.x - self.x * p.z,
            self.x * p.y - self.y * p.x,
        )

    def __magnitude__(self):
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def __normalize__(self):
        magnitude = self.__magnitude__()
        if magnitude == 0:
            return Vetor(0, 0, 0)
        return Vetor(self.x / magnitude, self.y / magnitude, self.z / magnitude)

    def __angle__(self, p: "Vetor"):
        return math.acos((self * p) / (self.__magnitude__() * p.__magnitude__()))
    
    def __truediv__(self, other):
        return Vetor(self.x / other, self.y / other, self.z / other)

