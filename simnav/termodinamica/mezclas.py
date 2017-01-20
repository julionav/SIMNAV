"""Ecuaciónes y utilidades para el manejo de propiedades termodinamicas de mezclas"""

from scipy.optimize import newton


class BasePropiedadesMezcla:
    """
    Clase base para propiedades de mezclas
    Todos los metodos de las clases son para mezclas y se introduciran los parametros como una
    lista o array en el orden en que se introducen los compuestos
    """
    temperatura_referencia = 298.15

    def __init__(self, compuestos):
        """Las propiedades de mezclas es inicializada con los compuestos de la simulación"""
        self.compuestos = compuestos


class PropiedadesMezclaIdeal(BasePropiedadesMezcla):
    """Propiedades de mezclas ene l estado ideal"""

    def punto_burbuja(self, composicion, presion, temperatura=None):
        """
        Punto de burbuja de una mezcla multicomponente ideal. Cumpliendo la condición de que la
        sumatoria de los componentes en fase gaseosa(y) es igual a 1.
        :param composicion: composicion en fraccion molar de la fase liquida
        :param presion: presion del sistema
        :param temperatura: temperatura inicial para la determinación del punto de burbuja
        :return: punto de burbuja para la mezcla
        """
        def sumatoria_fraccion_vapor(composicion, temperatura, presion):
            """Determinacion de la sumatoria de las fracciones de vapor (y). Siguiendo la ecuacion
            ideal"""
            sumatoria_y = 0
            for compuesto, fraccion_molar in zip(self.compuestos, composicion):
                sumatoria_y += compuesto.fraccion_vapor(fraccion_molar, temperatura, presion)

            return sumatoria_y

        return newton(sumatoria_fraccion_vapor, temperatura)
