"""Module containing the classes that represent the entities in the 3D space"""


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
        if discriminant < 0:
            return None, None
        t1 = (-b + discriminant**0.5) / (2 * a)
        t2 = (-b - discriminant**0.5) / (2 * a)
        return tuple(p + t1 * v for p, v in zip(line_point, line_vector)), tuple(
            p + t2 * v for p, v in zip(line_point, line_vector)
        )


class Plane:
    """Class Representing a Plane in 3D Space"""

    def __init__(self, point, normal, color):
        self.point = point
        self.normal = normal
        self.color = color

    def __intersect_line__(self, line_point, line_vector):
        """Calculate the Intersection Point of a Plane and a Line"""
        d = tuple(p - lp for p, lp in zip(self.point, line_point))
        t = sum(n * dp for n, dp in zip(self.normal, d)) / sum(
            n * lv for n, lv in zip(self.normal, line_vector)
        )
        return tuple(lp + t * lv for lp, lv in zip(line_point, line_vector))
