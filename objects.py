import numpy as np


class Plano:
    def __init__(self, v, P):
        self.vetor_normal = v
        self.ponto = P

    def intersecao_com_a_reta(self, vetor_diretor, ponto):
        return self._calcula_intersecao(vetor_diretor, ponto)

    def _calcula_intersecao(self, vetor_diretor, ponto):
        denominador = np.dot(self.vetor_normal, vetor_diretor)
        if np.isclose(denominador, 0):
            return RetornoIntersecao(False, None, None)
        t = (
            np.dot(self.vetor_normal, self.ponto) - np.dot(self.vetor_normal, ponto)
        ) / denominador
        ponto_intersecao = ponto + vetor_diretor * t
        return RetornoIntersecao(True, t, ponto_intersecao)


class RetornoIntersecao:

    def __init__(self, intersecoes, parametro, ponto_intersecao):
        self.intersecoes = intersecoes
        self.parametro = parametro
        self.ponto_intersecao = ponto_intersecao


class Esfera:

    def __init__(self, P, r):

        self.centro = P
        self.r = r

    def intersecao_com_a_reta(self, vetor_diretor, ponto):
        cp = ponto - self.centro
        a = np.dot(vetor_diretor, vetor_diretor)
        b = 2 * np.dot(vetor_diretor, cp)
        c = np.dot(cp, cp) - self.r**2
        delta = (b**2) - (4 * a * c)

        if delta < 0:
            return RetornoIntersecao(False, None, None)

        sqrt_delta = np.sqrt(delta)
        t1 = (-b + sqrt_delta) / (2 * a)
        t2 = (-b - sqrt_delta) / (2 * a)
        t = (
            min(t for t in (t1, t2) if t >= 0)
            if any(t >= 0 for t in (t1, t2))
            else None
        )

        if t is None:
            return RetornoIntersecao(False, None, None)

        intersection_point = ponto + vetor_diretor * t
        return RetornoIntersecao(True, t, intersection_point)