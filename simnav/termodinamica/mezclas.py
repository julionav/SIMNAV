"""Ecuaciónes y utilidades para el manejo de propiedades termodinamicas de mezclas"""

from scipy.optimize import newton


def punto_burbuja(componentes, P, T=None):
    """
    Punto de burbuja de una mezcla multicomponente ideal. Cumpliendo la condición de que la
    sumatoria de los componentes en fase gaseosa(y) es igual a 1.
    :param componentes: componentes del sistema (instancia de la clase Componente)
    :param P: presion del sistema
    :param T: temperatura inicial para la determinación del punto de burbuja
    :return: punto de burbuja para la mezcla
    """
    if T is None:
        T = 298.15  # Valor de temperatura arbitrario para comenzar la iteracion (25°C)

    def sumatoria_fraccion_vapor(T):
        """Determinacion de la sumatoria de las fracciones de vapor (y). Siguiendo la ecuacion
        ideal"""
        sumatoria_y = 0
        for componente in componentes:
            sumatoria_y += componente.fraccion_vapor(T)

        return sumatoria_y

    return newton(sumatoria_fraccion_vapor, T)



