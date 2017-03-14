"""Interfaz de alto nivel con el simulador"""
import logging

import yaml
import csv

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
        self.resultados = None
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
        for compuesto in datos['compuestos']:
            self.compuestos.append(compuesto)

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
        for corriente in self.corrientes:
            corriente.actualizar()

        self.paquete_propiedades.preparar()
        self.resultados = self.destilacion.simular()
        self.exportar()

    def exportar(self):
        """Exporta los resultados de la simulación"""
        with open('resultados.csv', 'w') as f:
            encabezado = ['Flujo de vapor', 'Flujo de liquido', 'Temperatura']

            # Luego de los flujos de vapor y liquido es mostrada la composicion de la fase
            # liquida seguida por la de la fase vapor
            seccion_composicion_liquido = [f'x - {compuesto}' for compuesto in self.compuestos]
            seccion_composicion_vapor = [f'y - {compuesto}' for compuesto in self.compuestos]

            encabezado.extend(seccion_composicion_liquido)
            encabezado.extend(seccion_composicion_vapor)

            escribidor = csv.DictWriter(f, encabezado)
            escribidor.writeheader()

            r = self.resultados
            filas = zip(r['vapor'], r['liquido'], r['fraccion_liquido'],
                        r['fraccion_vapor'], r['temperatura'])

            for V, L, x, y, T in filas:
                composicion_liquido = {f'x - {compuesto}': fraccion for compuesto, fraccion in
                                       zip(self.compuestos, x)}
                composicion_vapor = {f'y - {compuesto}': fraccion for compuesto, fraccion in
                                     zip(self.compuestos, y)}

                fila = {'Flujo de vapor': V, 'Temperatura': T, 'Flujo de liquido': L,
                        **composicion_liquido, **composicion_vapor,}

                escribidor.writerow(fila)
