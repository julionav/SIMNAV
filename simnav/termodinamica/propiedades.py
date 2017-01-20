"""Paquetes y gestores de propiedades"""
import logging

from functools import partial

import numpy as np

from simnav.datos import Parametros, GestorParametros
from simnav.termodinamica import ideal


class BasePropiedades:
    """Clase base para los gestores de propiedades de sustancias puras"""

    def __init__(self, nombre_compuesto, temperatura_referencia=None):
        self.parametros = Parametros(nombre_compuesto)
        if temperatura_referencia is None:
            self.temperatura_referencia = 298.15

        self._propiedades_criticas = self.parametros.constantes_criticas()

    @property
    def Tc(self):
        """Retorna la temperatura critica"""
        return self._propiedades_criticas.Tc

    @property
    def Pc(self):
        """Retorna la presion critica"""
        return self._propiedades_criticas.Pc

    @property
    def Vc(self):
        """Retorna el volumen critico"""
        return self._propiedades_criticas.Vc

    @property
    def factor_acentrico(self):
        return self._propiedades_criticas.factor_acentrico


class PropiedadesIdeales(BasePropiedades):
    """Paquete de propiedades termodinamicas ideal para sustancias puras"""
    _antoine = None  # Parametros de la ecuación de antoine
    _cp_liquido = None  # Parametros de calculo de cp liquido

    def presion_vapor(self, temperatura):
        """Determina la presión de vapor usando la ecuacion de antoine"""
        if self._antoine is None:
            self._antoine = self.parametros.antoine()

        return ideal.antoine(temperatura, self._antoine.C1, self._antoine.C2,
                             self._antoine.C3, self._antoine.C4, self._antoine.C5)

    def fraccion_vapor(self, fraccion_liquido, temperatura, presion):
        """Retorna la fraccion molar de la fase vapor para la condiciones dadas"""
        presion_vapor = self.presion_vapor(temperatura)
        return ideal.raoult(fraccion_liquido, presion_vapor, presion)

    def coeficiente_reparto(self, temperatura, presion):
        """Determina el coeficiente de reparto a las condiciones dadas usando la ecuación de
        antoine para el calculo de presión de vapor"""
        Pv = self.presion_vapor(temperatura)
        return Pv / presion

    def entalpia_liquido(self, temperatura):
        delta_T = temperatura - self.temperatura_referencia
        if self._cp_liquido is None:
            self._cp_liquido = self.parametros.cp_liquido()

        if self._cp_liquido.Ecuacion == 1:
            ecuacion_cp = partial(ideal.cp_liquido1,
                                  C1=self._cp_liquido.C1,
                                  C2=self._cp_liquido.C2,
                                  C3=self._cp_liquido.C3,
                                  C4=self._cp_liquido.C4,
                                  C5=self._cp_liquido.C5)
        elif self._cp_liquido.Ecuacion == 2:
            ecuacion_cp = partial(ideal.cp_liquido2,
                                  Tc=self.Tc,
                                  C1=self._cp_liquido.C1,
                                  C2=self._cp_liquido.C2,
                                  C3=self._cp_liquido.C3,
                                  C4=self._cp_liquido.C4)

        else:
            print('Parametro Ecuacion mal formateado')
        return ideal.entalpia_cp(T1=temperatura,
                                 T2=self.self.temperatura_referencia,
                                 ecuacion_cp=ecuacion_cp)


class GestorPropiedades:
    """
    Gestor de propiedades a usar con multiples componentes. Retorna listas de propiedades en
    el mismo orden que se introducen los componentes.
    Usa la libreria numpy.
    """

    def __init__(self, compuestos, temperatura_referencia=298):
        """

        :param compuestos: Lista de compuestos
        """
        self.compuestos = compuestos
        self.numero_compuestos = len(compuestos)
        self.parametros = GestorParametros(compuestos)
        self.temperatura_referencia = temperatura_referencia
        self.logger = logging.getLogger(__name__)

    def presion_vapor(self, temperatura):
        _presiones_vapor = np.zeros((len(temperatura), self.numero_compuestos))
        for indice, parametros in enumerate(self.parametros.antoine()):
            _presiones_vapor[:, indice] = ideal.antoine(temperatura,
                                                     parametros.C1,
                                                     parametros.C2,
                                                     parametros.C3,
                                                     parametros.C4,
                                                     parametros.C5)
        return _presiones_vapor

    def coeficiente_reparto(self, temperatura, presion):
        return self.presion_vapor(temperatura) / presion

    def entalpia_liquido(self, temperatura):
        _entalpia_liquido = np.array(self.numero_compuestos)
        parametros_criticos = self.parametros.constantes_criticas()

        for indice, parametros in enumerate(self.parametros.cp_liquido()):

            if parametros.Ecuacion == 1:
                ecuacion_cp = partial(ideal.cp_liquido1,
                                      C1=parametros.C1,
                                      C2=parametros.C2,
                                      C3=parametros.C3,
                                      C4=parametros.C4,
                                      C5=parametros.C5)
            elif parametros.Ecuacion == 2:
                ecuacion_cp = partial(ideal.cp_liquido2,
                                      Tc=parametros_criticos.Tc,
                                      C1=parametros.C1,
                                      C2=parametros.C2,
                                      C3=parametros.C3,
                                      C4=parametros.C4)
            else:
                print('Parametro Ecuacion mal formateado')

            _entalpia_liquido[indice] = ideal.entalpia_cp(T1=temperatura,
                                                          T2=self.temperatura_referencia,
                                                          ecuacion_cp=ecuacion_cp)
        return _entalpia_liquido

    def entalpia_vapor(self, temperatura):
        _entalpia_vapor = np.array(self.numero_compuestos)
        # Determinacion de ecuacion de cp en funcion de solo T
        # La ecuacion de cp existe en 2 formas. Polinomial y hiperbolica
        # Se utilizara la ecuacion en la cual la temperatura entre en su rango de uso
        _polinomial = self.parametros.cp_gas_polinomial()
        _hiperbolico = self.parametros.cp_gas_hiperbolico()

        # Se determina la entalpia componente a componente
        for i in range(self.numero_compuestos):
            if _polinomial[i] and _polinomial[i].TminK <= temperatura <= _polinomial[i].TmaxK:
                ecuacion_cp = partial(ideal.cp_polinomial,
                                      C1=_polinomial[i].C1,
                                      C2=_polinomial[i].C2,
                                      C3=_polinomial[i].C3,
                                      C4=_polinomial[i].C4,
                                      C5=_polinomial[i].C5)
            else:
                # Si la temperatura esta fuera del rango permitido se emite una advertencia
                if _hiperbolico[i].TminK > temperatura > _hiperbolico[i].TmanK:
                    self.logger.warning('La termperatura usada para el calculo de cp no esta '
                                        'en el rango permitido')
                # Sin embargo se calcula de igual manera el cp con la ecuación hiperbolica
                ecuacion_cp = partial(ideal.cp_hiperbolico,
                                      C1=_hiperbolico[i].C1,
                                      C2=_hiperbolico[i].C2,
                                      C3=_hiperbolico[i].C3,
                                      C4=_hiperbolico[i].C4,
                                      C5=_hiperbolico[i].C5)
            _entalpia_vapor[i] = ideal.entalpia_cp(T1=temperatura,
                                                   T2=self.temperatura_referencia,
                                                   ecuacion_cp=ecuacion_cp)
        return _entalpia_vapor
