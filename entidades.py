"""Module containing the classes that represent the entities in the 3D space"""

from vectors import Ponto


class Esfera:
    """Class Representing a Sphere in 3D Space"""

    def __init__(
        self,
        center,
        radius,
        color,
        k_difuso=0.0,
        k_especular=0.0,
        k_ambiental=0.0,
        k_reflexao=0.0,
        k_refracao=0.0,
        indice_refracao=0.0,
        n_rugosidade=0.0,
    ):
        self.center = center
        self.radius = radius
        self.color = color
        self.k_difuso = k_difuso
        self.k_especular = k_especular
        self.k_ambiental = k_ambiental
        self.k_reflexao = k_reflexao
        self.k_refracao = k_refracao
        self.indice_refracao = indice_refracao
        self.n_rugosidade = n_rugosidade

    def __get_normal_vector_to_intersection_point__(self, intersection_point):
        """Calculate the Normal Vector to the Intersection Point of a Sphere"""
        return [
            intersection_point.x - self.center.x,
            intersection_point.y - self.center.y,
            intersection_point.z - self.center.z,
        ]

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

    def __init__(
        self,
        point,
        normal,
        color,
        k_difuso=0.0,
        k_especular=0.0,
        k_ambiental=0.0,
        k_reflexao=0.0,
        k_refracao=0.0,
        indice_refracao=0.0,
        n_rugosidade=0.0,
    ):
        self.point = point
        self.normal = normal
        self.color = color
        self.k_difuso = k_difuso
        self.k_especular = k_especular
        self.k_ambiental = k_ambiental
        self.k_reflexao = k_reflexao
        self.k_refracao = k_refracao
        self.indice_refracao = indice_refracao
        self.n_rugosidade = n_rugosidade

    def __intersect_line__(self, line_point, line_vector):
        """Calculate the Intersection Point of a Plane and a Line"""
        d = tuple(p - lp for p, lp in zip(self.point, line_point))
        denominator = sum(n * lv for n, lv in zip(self.normal, line_vector))
        if denominator == 0:
            return None
        t = sum(n * dp for n, dp in zip(self.normal, d)) / denominator
        return tuple(lp + t * lv for lp, lv in zip(line_point, line_vector))


class Mesh:
    """Class Representing a Mesh in 3D Space"""

    def __init__(
        self,
        triangle_quantity: int,
        vertices_quantity: int,
        vertices: list[Ponto],
        triangle_tuple_vertices: list[tuple[int, int, int]],
        triangle_normals: list,
        vertex_normals: list,
        color,
        k_difuso=0.0,
        k_especular=0.0,
        k_ambiental=0.0,
        k_reflexao=0.0,
        k_refracao=0.0,
        indice_refracao=0.0,
        n_rugosidade=0.0,
    ):
        self.triangle_quantity = triangle_quantity
        self.vertices_quantity = vertices_quantity
        self.vertices = vertices
        self.triangle_tuple_vertices = triangle_tuple_vertices
        self.triangle_normals = triangle_normals
        self.vertex_normals = vertex_normals
        self.normal_to_intersection_point = None
        self.k_difuso = k_difuso
        self.k_especular = k_especular
        self.k_ambiental = k_ambiental
        self.k_reflexao = k_reflexao
        self.k_refracao = k_refracao
        self.indice_refracao = indice_refracao
        self.n_rugosidade = n_rugosidade

        self.color = color

    def __point_in_triangle__(self, point, triangle_vertices):
        """Check if a Point is Inside a Triangle using Barycentric Coordinates"""
        v0 = triangle_vertices[2].__sub__(triangle_vertices[0])
        v1 = triangle_vertices[1].__sub__(triangle_vertices[0])
        v2 = point.__sub__(triangle_vertices[0])

        d00 = v0.__mul__(v0)
        d01 = v0.__mul__(v1)
        d11 = v1.__mul__(v1)
        d20 = v2.__mul__(v0)
        d21 = v2.__mul__(v1)

        denom = d00 * d11 - d01 * d01

        v = (d11 * d20 - d01 * d21) / denom
        w = (d00 * d21 - d01 * d20) / denom
        u = 1.0 - v - w

        return (0 <= v <= 1) and (0 <= w <= 1) and (0 <= u <= 1)

    def __intersect_line__(self, line_point, line_vector):
        """Calculate the Intersection Point of a Mesh and a Line"""
        for index, triangle in enumerate(self.triangle_tuple_vertices):
            triangle_vertices = [self.vertices[i] for i in triangle]
            triangle_normal = self.triangle_normals[index]
            plane = Plane(triangle_vertices[0], triangle_normal, self.color)
            intersection_point = plane.__intersect_line__(line_point, line_vector)
            if intersection_point is not None:
                intersection_point = Ponto(
                    intersection_point[0], intersection_point[1], intersection_point[2]
                )
                if self.__point_in_triangle__(intersection_point, triangle_vertices):
                    self.normal_to_intersection_point = triangle_normal
                    return (
                        intersection_point.x,
                        intersection_point.y,
                        intersection_point.z,
                    )
        return None
