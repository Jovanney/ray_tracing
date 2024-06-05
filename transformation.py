import numpy as np
from decimal import Decimal
from vectors import Ponto, Vetor

class Transformacao:
    @staticmethod
    def criar_matriz_translacao(dx, dy, dz):
        return np.array([
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ], dtype=float)

    @staticmethod
    def criar_matriz_escala(sx, sy, sz):
        return np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ], dtype=float)

    @staticmethod
    def criar_matriz_rotacao_x(angulo):
        cos_a = np.cos(angulo)
        sin_a = np.sin(angulo)
        return np.array([
            [1, 0, 0, 0],
            [0, cos_a, -sin_a, 0],
            [0, sin_a, cos_a, 0],
            [0, 0, 0, 1]
        ], dtype=float)

    @staticmethod
    def criar_matriz_rotacao_y(angulo):
        cos_a = np.cos(angulo)
        sin_a = np.sin(angulo)
        return np.array([
            [cos_a, 0, sin_a, 0],
            [0, 1, 0, 0],
            [-sin_a, 0, cos_a, 0],
            [0, 0, 0, 1]
        ], dtype=float)

    @staticmethod
    def criar_matriz_rotacao_z(angulo):
        cos_a = np.cos(angulo)
        sin_a = np.sin(angulo)
        return np.array([
            [cos_a, -sin_a, 0, 0],
            [sin_a, cos_a, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=float)

    @staticmethod
    def aplicar_transformacao_ponto(ponto: Ponto, matriz):
        ponto_homogeneo = np.array([ponto.x, ponto.y, ponto.z, 1], dtype=float)
        resultado = matriz @ ponto_homogeneo
        return Ponto(resultado[0], resultado[1], resultado[2])

    @staticmethod
    def aplicar_transformacao_vetor(vetor: Vetor, matriz):
        vetor_homogeneo = np.array([vetor.x, vetor.y, vetor.z, 0], dtype=float)
        resultado = matriz @ vetor_homogeneo
        return Vetor(resultado[0], resultado[1], resultado[2])

    @staticmethod
    def aplicar_transformacao_malha(mesh, matriz):
        for i, vertice in enumerate(mesh.vertices):
            mesh.vertices[i] = Transformacao.aplicar_transformacao_ponto(vertice, matriz)
        return mesh
