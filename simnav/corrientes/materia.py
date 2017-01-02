from itertools import count
import numpy as np

"""Modulo con objetos y utilidades para el manejo de sustancias, mezclas y corrientes"""

class Sustancia:
    """Representación de una sustancia pura"""
    _ids = count(0)

    def __init__(self, nombre, pc=None, tc=None, zc=None, factor_acentrico=None):
        self.id = next(self._ids) + 1
        self.nombre = nombre
        self.tc = tc
        self.pc = pc
        self.zc = zc
        self.factor_acentrico = factor_acentrico

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return f'<Class Sustancia nombre:{self.nombre} id:{self.id}>'


class Componente:
    """Representación de una sustancia (componente) en una corriente o mezcla"""
    entalpia = None
    flujo = None

    def __init__(self, sustancia, composicion=None):
        self.x = composicion
        self.nombre = sustancia.nombre
        self.sustancia = sustancia


class CorrienteMateria:
    '''
    Corriente de flujo masico.
    '''

    def __init__(self, flujo, temperatura, paquete_termodinamico, presion=1, nombre=None, *componentes):
        self.nombre = nombre
        self.flujo = flujo
        self.temperatura = temperatura
        self.presion = presion
        self.paquete_termodinamico = paquete_termodinamico
        self.componentes = componentes
        self.calcular()

    def __iter__(self):
        for componente in self.componentes:
            yield componente

    def calcular(self):
        '''
        Calcula el equilibrio entre los componentes a las condiciones dadas
        '''
        # Hace algo con el paquete termodinamico


