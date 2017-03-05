"""Interfaz de alto nivel con el simulador"""
import logging

from simnav.corrientes import CorrienteMateria
from simnav.termodinamica import PaqueteIdeal
from simnav.datos.db import Componentes, session
from simnav.opus.destilacion import DestilacionSemiRigurosa

class Simulacion:
    """LLeva el control de alto nivel de la simulacion"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Inicializando simulacion')

        self.compuestos = []
        self.corrientes = []
        self._paquete_propiedades = None
        self.destilacion = DestilacionSemiRigurosa()

    @property
    def paquete_propiedades(self):
        return self._paquete_propiedades

    @paquete_propiedades.setter
    def paquete_propiedades(self, paquete):
        """Inicializa el paquete de propiedades segun el nombre provisto"""

        if (self._paquete_propiedades and paquete == self._paquete_propiedades.nombre) or not paquete:
            return

        if paquete == 'Ideal':
            self._paquete_propiedades = PaqueteIdeal(self.compuestos)
        elif paquete == 'Peng-Robinson':
            "Este paquete no ha sido implementado aun. Pronto lo sera"
            self._paquete_propiedades = PaqueteIdeal(self.compuestos)

        self.logger.debug('paquete de propiedades a sido asginado')

    def lista_compuestos(self):
        """Retorna la lista de compuestos disponibles en la base de datos"""
        self.logger.debug('Lista de compuestos a sido requerida')
        return [compuesto for compuesto in session.query(Componentes).all()]

    def crear_corriente(self, nombre, flujo=None, temperatura=None, composicion=None,
                        presion=None):
        """Crea una corriente en la simulacion con los parametros provistos"""
        self.logger.debug('Se esta creando una corriente con nombre {}'.format(nombre))

        self.corrientes.append(
            CorrienteMateria(nombre, self.compuestos, self.paquete_propiedades, flujo,
                             temperatura, composicion, presion))
