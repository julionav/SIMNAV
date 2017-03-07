"""Interfaz de alto nivel con el simulador"""
import logging

import yaml

from simnav.corrientes import CorrienteMateria
from simnav.termodinamica import GestorPaquetes
from simnav.datos.db import Componentes, session
from simnav.opus.destilacion import DestilacionSemiRigurosa


class Simulacion:
    """LLeva el control de alto nivel de la simulacion"""

    def __init__(self, direccion_archivo_simulacion=None):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Inicializando simulacion')

        self.compuestos = []
        self.corrientes = []
        self._paquete_propiedades = GestorPaquetes(self.compuestos)
        self.destilacion = DestilacionSemiRigurosa(
            paquete_termodinamico=self.paquete_propiedades)

        if direccion_archivo_simulacion:
            self.cargar_simulacion(direccion_archivo_simulacion)

    def cargar_simulacion(self, direccion_archivo_simulacion):
        """
        Carga los datos de simulación guardadas en el archivo de simulación suministrado
        :return:
        """
        self.logger.info("cargando datos de simulación")
        with open(direccion_archivo_simulacion, 'r') as datos_yaml:
            datos = yaml.load(datos_yaml)

        # Cargando compuestos
        self.compuestos = datos['compuestos']

        # Cargando corrientes
        for datos_corriente in datos['corrientes']:
            self.crear_corriente(**datos_corriente)

        # Cargando datos de simulación
        for parametro, valor in datos['destilacion'].items():
            if parametro == 'alimentaciones':
                # Las alimentaciones estan guardadas como [plato, posicion corriente]
                alimentaciones = []
                for alimentacion in valor:
                    # Con la posicion de la corriente se obtiene la referencia a la corrietne
                    corriente = self.corrientes[alimentacion['posicion_corriente']]
                    alimentaciones.append([alimentacion['plato'], corriente])

                self.destilacion.alimentaciones = alimentaciones

            else:
                setattr(self.destilacion, parametro, valor)

        # Cargando paquete de propiedades
        self.paquete_propiedades = datos['paquete propiedades']


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
