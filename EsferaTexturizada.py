from PIL import Image
import numpy as np
from entidades import Esfera
from vectors import Ponto
import math

class EsferaTexturizada(Esfera):
    def __init__(
        self,
        center,
        radius,
        texture_path,
        k_difuso=0.0,
        k_especular=0.0,
        k_ambiental=0.0,
        k_reflexao=0.0,
        k_refracao=0.0,
        indice_refracao=0.0,
        n_rugosidade=0.0,
    ):
        super().__init__(
            center,
            radius,
            [0, 0, 0],
            k_difuso,
            k_especular,
            k_ambiental,
            k_reflexao,
            k_refracao,
            indice_refracao,
            n_rugosidade,
        )
        self.texture = np.array(Image.open(texture_path))
        print("Textura carregada com dimensões:", self.texture.shape)

    def get_uv(self, ponto_intersec):
        normal = self.__get_normal_vector_to_intersection_point__(ponto_intersec)
        
        theta = math.atan2(normal[2], normal[0])
        phi = math.acos(normal[1])
        
        u = 0.5 + (theta / (2 * math.pi))
        v = 1 - (phi / math.pi)
        
        u = np.clip(u, 0, 1)
        v = np.clip(v, 0, 1)

        return u, v

    def get_color(self, u, v):
        height, width, _ = self.texture.shape
        
        x = int(u * (width - 1))
        y = int(v * (height - 1)) 

        x = np.clip(x, 0, width - 1)
        y = np.clip(y, 0, height - 1)

        color = self.texture[y, x] / 255.0
        return color
