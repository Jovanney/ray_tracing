"""Camera class for 3D rendering"""

from vectors import Ponto, Vetor


class Camera:
    """Class Representing a Camera in 3D Space
        w is the vector that always points to the center of the screen
        v is the vector that's always points to the right and it's ortogonal to w and up
        u is the vector that's always points up and it's ortogonal to w and v
    Args:
        target, position, up
    """

    def __init__(self, target: "Ponto", position: "Ponto", up: "Vetor"):
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


camera_position = Ponto(0, 0, 0)
camera_target = Ponto(0, 0, 1)
vetor_up = Vetor(0, 1, 0)

t = Camera(target=camera_target, position=camera_position, up=vetor_up)

print(f"w:{t.w.__dict__} v:{t.v.__dict__} u:{t.u.__dict__}")
