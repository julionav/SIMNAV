"""Modulo con objetos y utilidades para el manejo de sustancias, mezclas y corrientes"""

import logging

class CorrienteMateria:
    """
    Corriente de flujo masico.
    """

    def __init__(self, nombre, compuestos, paquete_termodinamico, flujo=None, temperatura=None,
                 composicion=None, presion=None):
        """

        :param flujo: Flujo de la corriente (mol/h)
        :param temperatura: Temperatura de la corriente (K)
        :param paquete_termodinamico: paquete para calculo de propiedades de la mezcla
        :param compuestos: referencia a los compuestos que componen la corriente
        :param presion: presion de la corriente (Pa)
        :param nombre: nombre de la corriente
        """
        # Valores por defecto
        self.flujo = flujo or 100
        self.temperatura = temperatura or 273.15
        self.presion = presion or 101325

        self.compuestos = compuestos
        self.nombre = nombre
        self.paquete_termodinamico = paquete_termodinamico
        self._entalpia = None

        # Compuestos conocidos por la corriente (pueden cambiar)
        self.compuestos_conocidos = list(compuestos)

        # Composicion de uso interno
        self.composicion = composicion or [0 for _ in range(len(self.compuestos))]

        # Logging
        self.logger = logging.getLogger(__name__)

    def __iter__(self):
        for compuesto, fraccion in zip(self.compuestos, self.composicion):
            yield compuesto, fraccion

    def actualizar(self):
        """Actualiza la corriente con los nuevos datos de simulación (nuevos compuestos)"""
        self.logger.debug(f'actualizando corriente {self.nombre}')
        print(self.compuestos, self.compuestos_conocidos)
        if self.compuestos != self.compuestos_conocidos:
            # Se resetea la composicion si los compuestos han cambiado
            self.logger.debug(f'Reseteando composicion de corriente {self.nombre}')
            self.composicion = [0 for _ in range(len(self.compuestos))]
            self.compuestos_conocidos = list(self.compuestos)

    @property
    def entalpia(self):
        """Retorna la entalpia absoluta de la corriente"""
        return self.entalpia_especifica * self.flujo

    @property
    def estado(self):
        """Retorna un string con el estado fisico en el que se encuentra al corriente"""
        return self.paquete_termodinamico.estado(self.composicion,
                                                 self.temperatura,
                                                 self.presion)

    @property
    def entalpia_especifica(self):
        """Retorna la entalpia especifica de la corriente"""
        return self.paquete_termodinamico.entalpia(self.composicion,
                                                   self.temperatura,
                                                   self.presion)
