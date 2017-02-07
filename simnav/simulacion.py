"""Interfaz de alto nivel con el simulador"""

from simnav.corrientes import CorrienteMateria
from simnav.termodinamica import PaqueteIdeal
from simnav.datos.db import Componentes, session
from simnav.opus.destilacion import DestilacionSemiRigurosa

class Simulacion:
    """LLeva el control de alto nivel de la simulacion"""

    def __init__(self):
        self.compuestos = []
        self.corrientes = []
        self.__paquete_propiedades = None
        self.destilacion = DestilacionSemiRigurosa()

    @property
    def paquete_propiedades(self):
        return self.__paquete_propiedades

    @paquete_propiedades.setter
    def paquete_propiedades(self, paquete):
        """Inicializa el paquete de propiedades segun el nombre provisto"""
        if paquete == 'Ideal':
            self.__paquete_propiedades = PaqueteIdeal(self.compuestos)
        elif paquete == 'Peng-Robinson':
            "Este paquete no ha sido implementado aun. Pronto lo sera"
            self.__paquete_propiedades = PaqueteIdeal(self.compuestos)

    def lista_compuestos(self):
        """Retorna la lista de compuestos disponibles en la base de datos"""
        return [compuesto for compuesto in session.query(Componentes).all()]

    def crear_corriente(self, nombre, flujo=None, temperatura=None, composicion=None,
                        presion=None):
        """Crea una corriente en la simulacion con los parametros provistos"""
        self.corrientes.append(
            CorrienteMateria(nombre, self.compuestos, self.paquete_propiedades, flujo,
                             temperatura, composicion, presion))

    def actualizar(self):
        """Actualiza los objetos que son parte de la simulacion si es necesario.
        (cuando cambian la cantidad de compuestos es necesario)"""
        self.paquete_propiedades.actualizar()
