"""Interfaz de alto nivel con el simulador"""
import logging

from simnav.corrientes import CorrienteMateria
from simnav.termodinamica import GestorPaquetes
from simnav.datos.db import Componentes, session
from simnav.opus.destilacion import DestilacionSemiRigurosa


class Simulacion:
    """LLeva el control de alto nivel de la simulacion"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Inicializando simulacion')

        self.compuestos = []
        self.corrientes = []
        self._paquete_propiedades = GestorPaquetes(self.compuestos)
        self.destilacion = DestilacionSemiRigurosa(
            paquete_termodinamico=self.paquete_propiedades)

    @property
    def paquete_propiedades(self):
        return self._paquete_propiedades

    @paquete_propiedades.setter
    def paquete_propiedades(self, paquete):
        """Inicializa el paquete de propiedades segun el nombre provisto"""
        self._paquete_propiedades.seleccionar_paquete(paquete)

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

    def simular(self):
        """Corre la simulación de la columna de destilacion"""
        self.paquete_propiedades.preparar()
        resultados = self.destilacion.simular()
        print(resultados)