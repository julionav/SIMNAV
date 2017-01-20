"""Ecuaciones termodinamicas ideales para el calculo de propiedades termodinamicas
del Manual del ingeniero quimico Perry"""

from math import sinh, cosh
from scipy import integrate

import numpy as np


def antoine(T, C1, C2, C3, C4, C5):
    """Ecuación para calculo de presión de vapor (Pa)"""
    return np.exp(C1 + C2/T + C3*np.log(T) + C4*T**C5)


def calor_vaporizacion(T, Tc, C1, C2, C3, C4):
    """Calor de vaporización de liquidos organicos e inorganicos [J/(mol.K)]"""
    Tr = T / Tc
    return C1*(1 - Tr)**(C2 + C3*Tr + C4*Tr**2) / 1000


def cp_polinomial(T, C1, C2, C3, C4, C5):
    """Capacidad calorifica a presion constante de compuestos inorganicos y organicos en el
    estado ideal como una ecuación polinomial [J/(mol.K)]"""
    return (C1 + C2*T + C3*T**2 + C4*T**3 + C5*T**4) / 1000


def cp_hiperbolico(T, C1, C2, C3, C4, C5):
    """Capacidad calorifica a presión constante para compuestos organicos e inorganicos
    en el estado ideal como una ecuación hiperbolica [J/(mol.K)]"""
    return (C1 + C2*((C3/T) / sinh(C3/T))**2 + C4*((C5/T) / cosh(C5/T))**2) / 1000


def cp_liquido1(T, C1, C2, C3, C4, C5):
    """Ecuación 1 para el calculo de capacidad calorifica de liquidos inorganicos y
    organicos [J/(mol.K)]"""
    return (C1 + C2*T +C3*T**2 + C4*T**3 + C5*T**4) / 1000


def cp_liquido2(T, Tc, C1, C2, C3, C4):
    """Ecuación 2 para el calculo de capacidad calorifica de liquidos inorganicos y
    organicos [J/(mol.K)]"""
    t = 1 - T/Tc  # t = 1 - Tr
    return (((C1**2)/t + C2 - 2*C1*C3*t - C1*C4*t**2 - (C3**2*t**3)/3 - (C3*C4*t**4)/2
            - (C4**2*t**5)/5) / 1000)


def entalpia_cp(T1, T2, ecuacion_cp):
    """Calcula la entalpia para una sustancia pura usando la capacidad calorifica a presión
    constante con la siguiente ecuación: dH = ∫cp dT

    :param T1: temperatura inicial para la integración
    :param T2: temperatura final para la integración
    :param ecuacion_cp: ecuación para calculo de cp en función de solo la temperatura
    :return: delta de entalpia entre las temperaturas provistas
    """
    return integrate.quad(ecuacion_cp, T1, T2)[0]


def raoult_vapor(fraccion_liquido, presion_vapor, presion):
    """Calculo de fracción molar de vapor mediante la ecuación de Raoult"""
    return fraccion_liquido * presion_vapor / presion


def raoult_liquido(fraccion_vapor, presion_vapor, presion):
    """Calcula la fraccion molar de liquido mediante la ec de Raoult"""
    return fraccion_vapor * presion / presion_vapor