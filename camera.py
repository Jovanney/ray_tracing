"""Camera class for 3D rendering"""

# import cv2 as cv
# import numpy as np
from entidades import Plane
from vectors import Ponto, Vetor
from phong_with_args import phong
from fonte_de_luz import Luz
from ray import Ray


def scale_rgb(color: tuple) -> tuple:
    """Return the color scaled to 255"""
    return tuple(rgb / 255 for rgb in color)


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

        self.u: "Vetor" = self.w.__cross__(self.v).__mul_escalar__(-1)
        self.u = self.u.__normalize__()

        self.target_distance = self.position.__distance__(self.target)

        self.vres = vres
        self.hres = hres

    def __intersect__(
        self, ray: "Ray", targets: list
    ) -> list[bool, list[int, int, int]]:
        """Return the intersection of a ray with a target"""

        smallest_distance = float("inf")
        color = [0, 0, 0]

        for target in targets:
            if isinstance(target, Plane):
                [intersection, intersection_color] = target.__intersect_line__(
                    ray.origin, ray.direction
                )
            else:
                intersection = target.__intersect_line__(ray.origin, ray.direction)
                intersection_color = target.color

            if intersection:
                distance_vetor = Vetor(
                    intersection[0], intersection[1], intersection[2]
                )

                distance = ray.origin.__distance__(distance_vetor)
                if distance < smallest_distance:
                    smallest_distance = distance
                    color = intersection_color
                    # phong(
                    #     target,
                    #     [
                    #         Luz(2, 1, 0, [153, 153, 153]),
                    #         Luz(-2, 1, 0, [153, 153, 153]),
                    #     ],
                    #     Ponto(intersection[0], intersection[1], intersection[2]),
                    #     self.position,
                    #     targets,
                    # )

        return color
