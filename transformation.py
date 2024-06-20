"""
This module provides classes and methods for performing transformations in 3D space.

Classes:

Note: This module depends on the 'numpy' library and the 'vectors' module.
"""

import math
import numpy as np
from vectors import Ponto, Vetor


class Transformacao:
    """
    This class provides static methods for creating transformation matrices and applying transformations to points, vectors, and meshes in 3D space.

    Methods:
    - criar_matriz_translacao(dx, dy, dz): Creates a translation matrix for translating points in 3D space.
    - criar_matriz_escala(sx, sy, sz): Creates a scaling matrix for scaling points in 3D space.
    - criar_matriz_rotacao_x(angulo): Creates a rotation matrix for rotating points around the x-axis.
    - criar_matriz_rotacao_y(angulo): Creates a rotation matrix for rotating points around the y-axis.
    - criar_matriz_rotacao_z(angulo): Creates a rotation matrix for rotating points around the z-axis.
    - aplicar_transformacao_ponto(ponto, matriz): Applies a transformation matrix to a point.
    - aplicar_transformacao_vetor(vetor, matriz): Applies a transformation matrix to a vector.
    - aplicar_transformacao_malha(mesh, matriz): Applies a transformation matrix to a mesh.

    """

    @staticmethod
    def criar_matriz_translacao(dx, dy, dz):
        """
        Creates a translation matrix for translating points in 3D space.

        Args:
        - dx: The translation amount along the x-axis.
        - dy: The translation amount along the y-axis.
        - dz: The translation amount along the z-axis.

        Returns:
        - A 4x4 numpy array representing the translation matrix.
        """
        return np.array(
            [[1, 0, 0, dx], [0, 1, 0, dy], [0, 0, 1, dz], [0, 0, 0, 1]], dtype=float
        )

    @staticmethod
    def criar_matriz_escala(sx, sy, sz):
        """
        Creates a scaling matrix for scaling points in 3D space.

        Args:
        - sx: The scaling factor along the x-axis.
        - sy: The scaling factor along the y-axis.
        - sz: The scaling factor along the z-axis.

        Returns:
        - A 4x4 numpy array representing the scaling matrix.
        """
        return np.array(
            [[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]], dtype=float
        )

    @staticmethod
    def criar_matriz_rotacao_x(angulo):
        """
        Creates a rotation matrix for rotating points around the x-axis.

        Args:
        - angulo: The rotation angle in radians.

        Returns:
        - A 4x4 numpy array representing the rotation matrix.
        """
        cos_a = math.cos(angulo)
        sin_a = math.sin(angulo)
        return np.array(
            [[1, 0, 0, 0], [0, cos_a, -sin_a, 0], [0, sin_a, cos_a, 0], [0, 0, 0, 1]],
            dtype=float,
        )

    @staticmethod
    def criar_matriz_rotacao_y(angulo):
        cos_a = math.cos(angulo)
        sin_a = math.sin(angulo)
        return np.array(
            [[cos_a, 0, sin_a, 0], [0, 1, 0, 0], [-sin_a, 0, cos_a, 0], [0, 0, 0, 1]],
            dtype=float,
        )

    @staticmethod
    def criar_matriz_rotacao_z(angulo):
        cos_a = math.cos(angulo)
        sin_a = math.sin(angulo)
        return np.array(
            [[cos_a, -sin_a, 0, 0], [sin_a, cos_a, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
            dtype=float,
        )

    @staticmethod
    def aplicar_transformacao_ponto(ponto: Ponto, matriz):
        ponto_homogeneo = np.array([ponto.x, ponto.y, ponto.z, 1], dtype=float)
        resultado = matriz @ ponto_homogeneo
        # print('aaa',ponto)
        return Ponto(resultado[0], resultado[1], resultado[2])

    @staticmethod
    def aplicar_transformacao_vetor(vetor: Vetor, matriz):
        vetor_homogeneo = np.array([vetor.x, vetor.y, vetor.z, 0], dtype=float)
        resultado = matriz @ vetor_homogeneo
        return Vetor(resultado[0], resultado[1], resultado[2])

    @staticmethod
    def aplicar_transformacao_malha(mesh, matriz):
        for i, vertice in enumerate(mesh.vertices):
            transformado = Transformacao.aplicar_transformacao_ponto(vertice, matriz)
            print(
                f"Vértice original: {vertice.x}, {vertice.y}, {vertice.z} -> Vértice transformado: {transformado.x}, {transformado.y}, {transformado.z}"
            )
            mesh.vertices[i] = transformado

        for i, normal in enumerate(mesh.triangle_normals):
            normal_transformada = Transformacao.aplicar_transformacao_vetor(
                normal, matriz
            )
            mesh.triangle_normals[i] = normal_transformada.__normalize__()

        return mesh

    @staticmethod
    def translate_sphere(esfera, dx, dy, dz):
        matriz_translacao = Transformacao.criar_matriz_translacao(dx, dy, dz)
        esfera.center = Transformacao.aplicar_transformacao_ponto(
            esfera.center, matriz_translacao
        )
        return esfera

    @staticmethod
    def change_scale_mesh(mesh, sx, sy, sz):
        matriz_escala = Transformacao.criar_matriz_escala(sx, sy, sz)
        mesh = Transformacao.aplicar_transformacao_malha(mesh, matriz_escala)
        return mesh
