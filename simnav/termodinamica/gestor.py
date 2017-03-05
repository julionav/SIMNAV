"""Gestor de paquetes termodinamicos"""
from .paquetes import PaqueteIdeal

class GestorPaquetes:
    """Gestor de paquetes termodinamicos. Actua como un objeto de alto nivel que realiza la
    conexion entre la simulación y el paquete termodinamico"""

    paquetes_disponibles = {
        'Ideal': PaqueteIdeal
    }

    def __init__(self, compuestos):
        self.paquete = PaqueteIdeal(compuestos)
        self.compuestos = compuestos

    def seleccionar_paquete(self, nombre_paquete):
        """
        Checkea si el paquete indicado esta disponible. Lo selecciona y asigna a la variable
        paquete.
        :param nombre_paquete: Nombre del paquete termodinamico deseado
        :return:
        """
        if not nombre_paquete or nombre_paquete == self.paquete.nombre:
            return

        if nombre_paquete in self.paquetes_disponibles:
            self.paquete = self.paquetes_disponibles[nombre_paquete](self.compuestos)

    def __getattr__(self, item):
        """Realiza el puente entre el gestor de paquetes y el paquete seleccionado"""
        return getattr(self.paquete, item)