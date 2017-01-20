"""Modulo con objetos y utilidades para el manejo de sustancias, mezclas y corrientes"""

import numpy as np


class Compuesto:
    """Representancion de una sustancia o compuesto"""

    def __init__(self, nombre, gestor_propiedades=None):
        self.nombre = nombre

        if gestor_propiedades:
            self.propiedades = gestor_propiedades

    def __getattr__(self, item):
        """redirecciona los metodos del gestor de propiedades para que puedan ser usados
        en el compuesto"""
        atributo = getattr(self.propiedades, item)
        if atributo:
            return atributo
        else:
            raise AttributeError('No existe el atributo o metodo')

    def __repr__(self):
        return f'<Compuesto {self.nombre}>'

    def __get__(self, instance, owner):
        return f'<Componente {self.nombre} en {owner} {instance.nombre}>'


class CorrienteMateria:
    '''
    Corriente de flujo masico.
    '''

    _ids = []

    def __init__(self, flujo, temperatura, compuestos, composicion, paquete_termodinamico,
                 presion=101325, nombre=None):
        """

        :param flujo: Flujo de la corriente (mol/h)
        :param temperatura: Temperatura de la corriente (K)
        :param paquete_termodinamico: paquete para calculo de propiedades de la mezcla
        :param compuestos: referencia a los compuestos que componen la corriente
        :param presion: presion de la corriente (atm)
        :param nombre: nombre de la corriente
        """
        self.flujo = flujo
        self.temperatura = temperatura
        self.compuestos = compuestos
        self.composicion = np.array(composicion)
        self.presion = presion
        self.nombre = nombre
        self.paquete_termodinamico = paquete_termodinamico
        self._entalpia = None

    def __iter__(self):
        for compuesto, fraccion in zip(self.compuestos, self.composicion):
            yield compuesto, fraccion

    @property
    def entalpia(self):
        return self.entalpia_especifica * self.flujo

    @property
    def estado(self):
        return self.paquete_termodinamico.estado(self.composicion,
                                                 self.temperatura,
                                                 self.presion)

    @property
    def entalpia_especifica(self):
        return self.paquete_termodinamico.entalpia(self.composicion,
                                                   self.temperatura,
                                                   self.presion)
    def calcular(self):
        '''
        Calcula el equilibrio entre los componentes a las condiciones dadas
        '''
        # Hace algo con el paquete termodinamico
