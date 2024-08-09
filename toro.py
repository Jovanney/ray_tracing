import math
import numpy as np
from entidades import Mesh
from vectors import Ponto

def toRad(espacamento):
    #transforma os valores que serão ultilizamos para a triangularização com base no espaçamento fornecido para radianos
    valores = np.arange(0, 2 * math.pi + espacamento, espacamento)
    if valores[-1] > 2 * math.pi:
        valores = valores[:-1]
    if valores[-1] < 2 * math.pi:
        valores = np.append(valores, 2 * math.pi)
    return valores

class Toro:
    def __init__(self, centro_y, centro_z, R, r, cor):
        self.centro_y = centro_y
        self.centro_z = centro_z
        self.R = R
        self.r = r
        self.cor = cor

    def point_on_surface(self, theta, alpha):#gerar o ponto na superfície do toro correspondente aos angulos fornecidos 
        x = (self.R + self.r * math.cos(theta)) * math.cos(alpha)
        z = (self.R + self.r * math.cos(theta)) * math.sin(alpha)
        y = self.r * math.sin(theta)
        return Ponto(x, y, z)
    
    def triangularizar(self, espacamento):
        """Triangulariza o objeto com base no espaçamento fornecido."""
        pontos_bezier = []
        theta_values = toRad(espacamento)
        alpha_values = toRad(espacamento)

        for theta in theta_values:
            for alpha in alpha_values:
                ponto = self.point_on_surface(theta, alpha)
                pontos_bezier.append(ponto)

        triangulos = []
        n = len(theta_values) - 1

        for i in range(n): #geração dos triangulos
            for j in range(n):
                triangulos.append((i * (n + 1) + j, (i + 1) * (n + 1) + j, i * (n + 1) + j + 1))
                triangulos.append(((i + 1) * (n + 1) + j, (i + 1) * (n + 1) + j + 1, i * (n + 1) + j + 1))

        lista_normais = []
        for triangulo in triangulos: #calcula as normais dos triângulos
            p0 = np.array([pontos_bezier[triangulo[0]].x, pontos_bezier[triangulo[0]].y, pontos_bezier[triangulo[0]].z])
            p1 = np.array([pontos_bezier[triangulo[1]].x, pontos_bezier[triangulo[1]].y, pontos_bezier[triangulo[1]].z])
            p2 = np.array([pontos_bezier[triangulo[2]].x, pontos_bezier[triangulo[2]].y, pontos_bezier[triangulo[2]].z])

            normal = np.cross(p1 - p0, p2 - p0)
            norma = np.linalg.norm(normal)
            normal = normal / norma
            
            lista_normais.append(normal.tolist())

        malha = Mesh(
            triangle_quantity=len(triangulos),
            vertices_quantity=len(pontos_bezier),
            vertices=pontos_bezier,
            triangle_tuple_vertices=triangulos,
            triangle_normals=lista_normais,
            vertex_normals=[],
            color=self.cor,
            k_ambiental=0.5,
            k_difuso=0.5,
            k_especular=0.5,
            n_rugosidade=50,
            k_reflexao=0,
            k_refracao=0,
            indice_refracao=0
        )
        
        return malha
    
