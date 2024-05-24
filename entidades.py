"""Module containing the classes that represent the entities in the 3D space"""
from vectors import Vetor
import numpy as np

class Esfera:
    """Class Representing a Sphere in 3D Space"""

    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

    def __intersect_line__(self, line_point, line_vector):
        """Calculate the Intersection Points of a Sphere and a Line"""
        a = sum(i * j for i, j in zip(line_vector, line_vector))
        b = 2 * sum(
            i * j
            for i, j in zip(
                line_vector, (p - c for p, c in zip(line_point, self.center))
            )
        )
        c = sum((p - c) ** 2 for p, c in zip(line_point, self.center)) - self.radius**2
        discriminant = b**2 - 4 * a * c
        if discriminant <= 0:
            return None
        t1 = (-b + discriminant**0.5) / (2 * a)
        t2 = (-b - discriminant**0.5) / (2 * a)

        if 0 < t1 < t2:
            return tuple(p + t1 * v for p, v in zip(line_point, line_vector))
        if 0 < t2 < t1:
            return tuple(p + t2 * v for p, v in zip(line_point, line_vector))

        return None


class Plane:
    """Class Representing a Plane in 3D Space"""

    def __init__(self, point, normal, color):
        self.point = point
        self.normal = normal
        self.color = color

    def __intersect_line__(self, line_point, line_vector):
        """Calculate the Intersection Point of a Plane and a Line"""
        d = tuple(p - lp for p, lp in zip(self.point, line_point))
        denominator = sum(n * lv for n, lv in zip(self.normal, line_vector))
        if denominator == 0:
            return None
        t = sum(n * dp for n, dp in zip(self.normal, d)) / denominator
        return tuple(lp + t * lv for lp, lv in zip(line_point, line_vector))

class TriangleMesh:
    """Class Representing a Triangle Mesh in 3D Space"""

    def __init__(self, num_triangles, num_vertices, vertices, triangles, triangle_normals, vertex_normals, color):
        self.num_triangles = num_triangles
        self.num_vertices = num_vertices
        self.vertices = vertices
        self.triangles = triangles
        self.triangle_normals = triangle_normals
        self.vertex_normals = vertex_normals
        self.color = color

    def __intersect_line__(self, line_origin, line_direction):
        for i, triangle in enumerate(self.triangles):
            v0, v1, v2 = [self.vertices[idx] for idx in triangle]
            triangle_normal = self.triangle_normals[i]

            d = Vetor(v0.x - line_origin.x, v0.y - line_origin.y, v0.z - line_origin.z)
            denominator = triangle_normal * line_direction
            if abs(denominator) < 1e-6:
                continue  # Line is parallel to the triangle
            t = (triangle_normal * d) / denominator
            if t < 0:
                continue  # Intersection point is behind the line origin

            intersection_point = Vetor(line_origin.x + t * line_direction.x,
                                        line_origin.y + t * line_direction.y,
                                        line_origin.z + t * line_direction.z)

            # Check if the intersection point is inside the triangle
            edge0 = Vetor(v1.x - v0.x, v1.y - v0.y, v1.z - v0.z)
            edge1 = Vetor(v2.x - v1.x, v2.y - v1.y, v2.z - v1.z)
            edge2 = Vetor(v0.x - v2.x, v0.y - v2.y, v0.z - v2.z)
            c0 = Vetor.__cross__(edge0, intersection_point - v0)
            c1 = Vetor.__cross__(edge1, intersection_point - v1)
            c2 = Vetor.__cross__(edge2, intersection_point - v2)
            if (c0 * triangle_normal >= 0 and
                    c1 * triangle_normal >= 0 and
                    c2 * triangle_normal >= 0):
                return intersection_point

        return None
    