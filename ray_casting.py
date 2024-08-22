"""This module is responsible for the ray casting algorithm"""

import cv2 as cv
import numpy as np
from bsp import render_bsp_tree
from camera import Camera, Ray


class RayCasting:
    """
    Class Representing the Ray Casting Algorithm
    """

    def __init__(self, hres, vres):
        self.hres = hres
        self.vres = vres
        self.image = np.zeros((self.vres, self.hres, 3), dtype=np.uint8)
        self.total_pixels = self.vres * self.hres
        self.processed_pixels = 0

    def __generate_image__(self, targets, distancia, camera: Camera):
        for i in range(self.vres):
            for j in range(self.hres):
                ray = Ray(
                    origin=camera.position,
                    direction=(
                        camera.w.__mul_escalar__(distancia)
                        + camera.v.__mul_escalar__(2 * 0.5 * (j / self.hres - 0.5))
                        + camera.u.__mul_escalar__(2 * 0.5 * (i / self.vres - 0.5))
                    ),
                )
                color = camera.__intersect__(ray, targets)

                self.image[i, j] = color[::-1]
                self.processed_pixels += 1
            print(f"Progress: {self.processed_pixels / self.total_pixels * 100:.2f}%")

        # pylint: disable=no-member
        cv.imshow("image", self.image)
        cv.waitKey(0)
        cv.destroyAllWindows("i")

    def __generate_image__with_bsp(self, root, camera: Camera):
        for i in range(self.vres):
            for j in range(self.hres):
                ray_direction = (
                    camera.w.__mul_escalar__(camera.target_distance)
                    + camera.v.__mul_escalar__(2 * 0.5 * (j / self.hres - 0.5))
                    + camera.u.__mul_escalar__(2 * 0.5 * (i / self.vres - 0.5))
                ).__normalize__()

                ray = Ray(origin=camera.position, direction=ray_direction)

                # Renderize a cena utilizando a árvore BSP
                color = render_bsp_tree(root, camera, ray)
                if color is not None:
                    self.image[i, j] = color[::-1]
                else:
                    self.image[i, j] = [0, 0, 0]  # Background color

                self.processed_pixels += 1
            print(f"Progress: {self.processed_pixels / self.total_pixels * 100:.2f}%")

        # pylint: disable=no-member
        cv.imshow("image", self.image)
        cv.waitKey(0)
        cv.destroyAllWindows("i")
