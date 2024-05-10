from vectors import Ponto, Vetor
from objects import Plano, Esfera
import cv2 as cv
import numpy as np

def normalize(vector):
    return vector / np.linalg.norm(vector)

class ObjPointer:
    def __init__(self, ptr_esfera=None, ptr_plano=None, tipo_objeto=None):
        self.ptr_esfera = ptr_esfera
        self.ptr_plano = ptr_plano
        self.tipo = tipo_objeto

class Camera:
    def __init__(self, posicao, target, up_vector):
        self.k = up_vector
        self.posicao = posicao
        self.W = (target - posicao)
        self.W = normalize(self.W)

        self.U = np.cross(self.k, self.W)
        self.U = normalize(self.U)

        self.UP = np.cross(self.W, self.U) * -1
        self.UP = normalize(self.UP)

    def intersect(self, vetor_atual, objects):
        menor_t= 1000000
        cor = [0, 0, 0]
        for obj in objects:
            if isinstance(obj, Esfera):
                inter_esfera = obj.intersecao_com_a_reta(vetor_atual, self.posicao)
                if inter_esfera.intersecoes:
                    if inter_esfera.parametro <= menor_t and inter_esfera.parametro >= 0.01:
                        cor = [255, 0, 0]
                        menor_t = inter_esfera.parametro
            elif isinstance(obj, Plano):
                inter_plano = obj._calcula_intersecao(vetor_atual, self.posicao)
                if inter_plano:
                    if inter_plano.intersecoes:
                        if inter_plano.parametro <= menor_t and inter_plano.parametro >= 0.01:
                            cor = [0, 255, 0]
                            menor_t = inter_plano.parametro
        return cor

    def raycasting(self, distancia, hres, vres, objects):
        deslocamento_vertical = (2*0.5/(hres - 1)*self.U)
        deslocamento_horizontal = (2*0.5/(vres - 1)*self.UP)
        centro_tela = (self.W * distancia)
        pixel_0_0 = centro_tela - (0.5 * self.U) - (0.5 * self.UP)
        imagem = np.zeros((vres, hres, 3), dtype=np.uint8)  # Imagem a ser gerada
        for i in range(vres):
            for j in range(hres):
                vetor_atual = pixel_0_0 + deslocamento_vertical*i + deslocamento_horizontal*j
                imagem[j,i] = self.intersect(vetor_atual, objects)
        cv.imshow("Raycasting", imagem)
        cv.waitKey(0)
        cv.destroyAllWindows('i')
