from .modelos import (Componentes,
                      CapacidadesCalorificasGasPolinomial,
                      CapacidadesCalorificasLiquido,
                      ConstantesCriticasFactoresAcentricos,
                      CpGasHiperbolico,
                      CalorVaporizacionLiquidos,
                      Antoine,
                      session,
                      )

"""
Classes, funciones y utilidades para el manejo de propiedades
"""


class ComponenteNoExiste(Exception):
    pass


class Parametros:
    """Manejador de parametros de ecuaciones para el calculo de propiedades fisicoquimicas de simnav"""

    # Se utiliza una solicitud a la base de datos por cada componente por separado para obtener su información
    # asociada. Esto se realiza con el objetivo de mantener el orden de los componentes. Al ser la interacción con
    # la base de datos poca, realizar las solicitudes de esta manera no creara problemas de rendimiento.
    # TODO: Colocar ecuaciónes
    def __init__(self, *componentes):
        """El manejador se inicializa con los componentes a simular"""
        self.componentes = [componente.upper() for componente in componentes]

        self.componentes_id = []
        for componente in self.componentes:
            componente_id = session.query(Componentes.id).filter_by(NAME=componente).scalar()
            if componente_id is None:
                raise ComponenteNoExiste(f'El componente {componente} no existe en nuestra base de datos')
            self.componentes_id.append(componente_id)

    def _solicitar_datos(self, clase):
        """
        Realiza la solicitud a la base de datos para obtener los datos necesarios componente a componente
        :param Clase: Clase relaciónada con una tabla de la base de datos a utilizar para la solicitur
        :return: Una lista con objetos que representan las filas
        """
        return [session.query(clase).get(componente_id) for componente_id in self.componentes_id]

    def antoine(self):
        """Retorna los parametros de la ecuación de antoine"""
        return self._solicitar_datos(Antoine)

    def cp_gas_polinomial(self):
        """Retorna los parametros a utilizar en la ecuación para calculo de capacidades calorificas de gas en forma
        polinomial encontrada en el Perry"""
        return self._solicitar_datos(CapacidadesCalorificasGasPolinomial)

    def cp_liquido(self):
        """Retorna los parametros a utilizar en la ecuación para calculo de capacidades calorificas de liquido
        encontrada en el Perry"""
        return self._solicitar_datos(CapacidadesCalorificasLiquido)

    def constantes_criticas(self, componentes=None):
        """Retorna las constantes criticas de los componentes"""
        return self._solicitar_datos(ConstantesCriticasFactoresAcentricos)

    def cp_gas_hiperbolico(self):
        """Retorna los parametros a utilizar en la ecuación para calculo de capacidades calorificas de gas en forma
        hiperbolica encontrada en el Perry"""
        return self._solicitar_datos(CpGasHiperbolico)

    def calor_vaporizacion(self):
        """Retorna los parametros a utilizar en la ecuación para el calculo de calor de vaporización de liquidos
         encontrada en el Perry"""
        return self._solicitar_datos(CalorVaporizacionLiquidos)

