"""Camera class for 3D rendering"""

# import cv2 as cv
# import numpy as np
from vectors import Ponto, Vetor
from entidades import TriangleMesh, Plane, Esfera


def scale_rgb(color: tuple) -> tuple:
    """Return the color scaled to 255"""
    return tuple(rgb / 255 for rgb in color)


class Ray:
    """Class Representing a Ray in 3D Space
    Args:
        origin, direction
    """

    def __init__(self, origin: "Ponto", direction: "Vetor"):
        """Initialize the Ray"""
        self.origin = origin
        self.direction = direction

    def __str__(self):
        """Return the string representation of the Ray"""
        return f"Ray({self.origin}, {self.direction})"

    def __repr__(self):
        """Return the string representation of the Ray"""
        return self.__str__()

    def get_point(self, t: float) -> "Ponto":
        """Return the point at t distance from the origin"""
        return self.origin + (self.direction.__mul_escalar__(t))

    def __add__(self, other: "Ray") -> "Ray":
        """Return the sum of two rays"""
        return Ray(
            self.origin.__add__(other.origin), self.direction.__add__(other.direction)
        )

    def __sub__(self, other: "Ray") -> "Ray":
        """Return the subtraction of two rays"""
        return Ray(
            self.origin.__sub__(other.origin), self.direction.__sub__(other.direction)
        )

    def __mul__(self, other: float) -> "Ray":
        """Return the multiplication of a ray by a scalar"""
        return Ray(self.origin.__mul__(other), self.direction.__mul__(other))

    def __truediv__(self, other: float) -> "Ray":
        """Return the division of a ray by a scalar"""
        return Ray(self.origin.__truediv__(other), self.direction.__truediv__(other))


class Camera:
    """Class Representing a Camera in 3D Space
        w is the vector that always points to the center of the screen
        v is the vector that's always points to the right and it's ortogonal to w and up
        u is the vector that's always points up and it's ortogonal to w and v
    Args:
        target, position, up
    """

    def __init__(
        self,
        target: "Ponto",
        position: "Ponto",
        up: "Vetor",
        vres: int = 300,
        hres: int = 300,
    ):
        """Initialize the Camera"""
        self.position = position
        self.target = target
        self.up = up

        self.w: "Vetor" = self.target.__sub__(self.position)
        self.v: "Vetor" = self.up.__cross__(self.w)

        self.w = self.w.__normalize__()
        self.v = self.v.__normalize__()

        self.u: "Vetor" = self.w.__cross__(self.v)
        self.u = self.u.__normalize__()

        self.target_distance = self.position.__distance__(self.target)

        self.vres = vres
        self.hres = hres

    def __intersect__(
        self, ray: "Ray", targets: list
    ) -> list[int, int, int]:
        """Return the intersection of a ray with a target"""

        smallest_distance = float("inf")
        color = tuple([0, 0, 0])

        for target in targets:
            if isinstance(target, TriangleMesh):  # Verifica se o alvo é uma instância de Mesh
                intersection = target.__intersect_line__(ray.origin, ray.direction)
                if intersection:
                    distance = ray.origin.__distance__(intersection)
                    if distance < smallest_distance:
                        smallest_distance = distance
                        color = target.color
                    

            elif isinstance(target, Plane):  # Verifica se o alvo é uma instância de Plane
                intersection = target.__intersect_line__(ray.origin, ray.direction)
                if intersection:
                    # Defina a cor do plano aqui, se desejar
                    color = target.color

            elif isinstance(target, Esfera):  # Verifica se o alvo é uma instância de Sphere
                intersection = target.__intersect__(ray)
                if intersection:
                    # Defina a cor da esfera aqui, se desejar
                    color = target.color

        return color