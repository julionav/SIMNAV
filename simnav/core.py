# -*- coding: utf-8 -*-


'''
Created on 18/09/2016

@author: Julio Navarro
'''

# Librerias estandar
from math import exp, log


class ModeloEquilibrioIdeal:

    """
    Modelo de equilibrio vapor-liquido ideal
    """

    def __init__(self, p_antoine, cp_liquido, cp_polinomial, cp_hiperbolico,
                 calor_vap, prop_criticas):
        """
        Se inicia la clase con los parametros constantes de las distintas
        ec a utilizar
        """
        self.p_antonine = p_antoine
        self.cp_liquido = cp_liquido
        self.cp_polinomial = cp_polinomial
        self.calor_vap = calor_vap
        self.prop_criticas = prop_criticas

    def P_vapor_antoine(self, temperatura):
        """
        Toma como parametro la temperatura del fluido y determina su presion
        de vapor ideal
        """
        T = temperatura

        presion_vapor = exp(self.P_antine[0] + self.P_antoine[1] / T +
                            self.antoine[2] * log(T) + self.P_antoine[3] *
                            T ** self.P_antoine[4])
        return presion_vapor
