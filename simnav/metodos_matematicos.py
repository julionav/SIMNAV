"""Metodos matematicos a utilizar en las simulaciones"""

import numpy as np


def metodo_tomas(a, b, c, d):
    """Metodo de tomas utilizado para resolver matrices tridiagonales"""
    N = a.size
    x = np.zeros(N)
    # se modifican los coeficientes de la primera fila
    c[0] = c[0] / b[0]
    d[0] = d[0] / b[0]

    for i in range(1, N):
        temp = b[i] - a[i] * c[i - 1]
        c[i] = c[i] / temp
        d[i] = (d[i] - a[i] * d[i - 1]) / temp

    # ahora se sustituye hacia atras.
    x[N - 1] = d[N - 1]

    for i in range(N - 2, -1, -1):
        x[i] = d[i] - c[i] * x[i + 1]
    return x