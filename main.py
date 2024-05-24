from vectors import Ponto, Vetor
from entidades import TriangleMesh
from camera import Camera
from ray_casting import RayCasting

def main():
    """Main Function"""

    camera = Camera(
        target=Ponto(5, 0, 0),
        position=Ponto(4, 100, 0),
        up=Vetor(0, 1, 0),
    )

    ray_casting = RayCasting(hres=300, vres=300)

    p0 = Vetor(100, 0, 0)
    p1 = Vetor(0, 100, 0)
    p2 = Vetor(-100, 0, 0)
    p3 = Vetor(0, -100, 0)
    p4 = Vetor(0, 0, 100)

    n1 = Vetor.__cross__(p1 - p0, p4 - p0)
    n1 = n1.__truediv__(n1.__magnitude__())

    n2 = Vetor.__cross__(p2 - p1, p4 - p1)
    n2 = n2.__truediv__(n2.__magnitude__())

    n3 = Vetor.__cross__(p3 - p2, p4 - p2)
    n3 = n3.__truediv__(n3.__magnitude__())

    n4 = Vetor.__cross__(p0 - p3, p4 - p3)
    n4 = n4.__truediv__(n4.__magnitude__())

    malha = TriangleMesh(
            num_triangles=4,
            num_vertices=5,
            vertices=[p0, p1, p2, p3, p4], 
            triangles=[(0, 1, 4), (1, 2, 4), (2, 3, 4), (0, 3, 4)], 
            triangle_normals=[n1, n2, n3, n4], 
            vertex_normals=[], 
            color=[[255, 255, 255], [255, 0, 0], [0, 255, 0], [0, 0, 255]]
        )

    entidades = [malha]

    ray_casting.__generate_image__(entidades, camera.target_distance, camera)


main()

