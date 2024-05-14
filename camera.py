"""Camera class for 3D rendering"""

import cv2 as cv
import numpy as np
from entidades import Esfera, Plane
from vectors import Ponto, Vetor


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
        vres: int = 200,
        hres: int = 100,
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

        self.targer_distance = self.position.__distance__(self.target)

        self.vres = vres
        self.hres = hres

    # def __intersect_sphere__(self, center: "Vetor", radius: float, ray: "Ray") -> bool:
    #     """Return the intersection of a ray with a sphere"""
    #     oc = ray.origin.__sub__(center)
    #     a = ray.direction.__mul__(ray.direction)
    #     b = 2.0 * oc.__mul__(ray.direction)
    #     c = oc.__mul__(oc) - radius * radius
    #     discriminant = b * b - 4 * a * c
    #     return discriminant > 0

    def __intersect__(self, ray: "Ray", targets: list) -> bool:
        """Return the intersection of a ray with a target"""
        for target in targets:
            if isinstance(target, Esfera):
                if target.__intersect_line__(ray.origin, ray.direction):
                    return True
            elif isinstance(target, Plane):
                if target.__intersec_line__(ray.origin, ray.direction):
                    return True
        return False

    def __ray_casting__(self, targets: list):
        """Return the image generated by the camera"""
        image = np.zeros((self.vres, self.hres, 3), dtype=np.uint8)

        for i in range(self.hres - 1):
            for j in range(self.vres - 1):
                x = -1 + 2 * (j + 0.5) / self.vres
                y = -1 + 2 * (i + 0.5) / self.hres

                direction = (
                    self.w + self.v.__mul_escalar__(x) + self.u.__mul_escalar__(y)
                )
                direction = Vetor(direction.x, direction.y, direction.z)
                direction = direction.__normalize__()

                ray = Ray(self.position, direction)

                image[j, i] = 150 if self.__intersect__(ray, targets) else 0

        # pylint: disable=no-member
        cv.imshow("image", image)
        cv.waitKey(0)
        cv.destroyAllWindows("i")


if __name__ == "__main__":
    camera = Camera(Ponto(0, 0, 0), Ponto(0, 0, -5), Vetor(0, 1, 0))
    # camera.__ray_casting__([Esfera(Ponto(0, 0, -10), 1, (150, 0, 0))])
    camera.__ray_casting__([Plane(Ponto(0, 0, -10), Vetor(0, 0, 1), (150, 0, 0))])