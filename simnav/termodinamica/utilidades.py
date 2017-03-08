"""Utilidades para el manejo de propiedades y paquetes termodinamicos"""

from functools import wraps

import numpy as np


def soporte_scalar(func):
    """Gives numpy support to a python function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if any(isinstance(arg, (int, float, list, tuple)) for arg in args):
            new_args = []
            for arg in args:
                if isinstance(arg, (list, tuple, int, float)):
                    arg = np.atleast_2d(arg)
                new_args.append(arg)
            return func(*new_args, **kwargs)[0]

        return func(*args, **kwargs)

    return wrapper


def sumar_filas(array):
    """
    Suma las filas de un array. Si el array es de 1 sola dimension suma todos los elementos
    """
    if array.ndim == 2:
        return np.sum(array, axis=1)
    else:
        return np.sum(array)


def soporte_numpy_2d(func):
    """Da soporte para arrays 2d a funciones que utilizan arrays 1d o scalares"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, np.ndarray) and arg.ndim == 2:
                results = np.empty(arg[:, 0].size)
                break

        else:
            for value in kwargs.values():
                if isinstance(value, np.ndarray) and value.ndim == 2:
                    results = np.empty(value[:, 0].size)
                    break
            else:
                return func(*args, **kwargs)

        for i in range(results.size):
            results[i] = func(
                *[arg[i] if isinstance(arg, np.ndarray) else arg for arg in args],
                **{key: value[i] for key, value in kwargs.items()})

        return results

    return wrapper
