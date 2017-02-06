"""
Classes, funciones y utilidades para el manejo de propiedades
"""

from simnav.errores import CompuestoNoEncontrado
from .db import (Componentes,
                 CapacidadesCalorificasGasPolinomial,
                 CapacidadesCalorificasLiquido,
                 ConstantesCriticasFactoresAcentricos,
                 CpGasHiperbolico,
                 CalorVaporizacionLiquidos,
                 Antoine,
                 session,
                 )


class GestorParametros:
    """Manejador de parametros de ecuaciones para el calculo de
    propiedades fisicoquimicas de simnav"""

    # Relacion instancia orm con variable de almacenamiento local (o nombre de parametros)
    #  para almacenamiento de resultados de solicitudes a base de datos
    ORM_parametros = {
        Antoine: '_antoine',
        CapacidadesCalorificasGasPolinomial: '_cp_gas_polinomial',
        CapacidadesCalorificasLiquido: '_cp_liquido',
        ConstantesCriticasFactoresAcentricos: '_constantes_criticas',
        CpGasHiperbolico: '_cp_gas_hiperbolico',
        CalorVaporizacionLiquidos: '_calor_vaporizacion'
    }

    def __init__(self, compuestos):
        """El manejador se inicializa con los componentes a simular"""
        self.compuestos = compuestos
        self.compuestos_id = []

        # Los componentes en la base de datos estan en ingles
        compuestos_upper = [compuesto.upper() for compuesto in self.compuestos]

        for compuesto in compuestos_upper:
            compuesto_id = session.query(Componentes.id).filter_by(NAME=compuesto).scalar()
            if compuesto_id is None:
                raise CompuestoNoEncontrado(
                    f'El compuesto {compuesto} no existe en nuestra base de datos')
            self.compuestos_id.append(compuesto_id)

    def _solicitar_datos(self, clase):
        """
        Realiza la solicitud a la base de datos para obtener los datos necesarios
        :param clase: instancia de orm para solicitud a base de datos
        :return: Una lista de objetos que contienen los parametros solicitados
        """
        nombre_parametros = self.ORM_parametros[clase]
        if hasattr(self, nombre_parametros):
            return getattr(self, nombre_parametros)
        else:
            resultado = [session.query(clase).get(compuesto_id)
                         for compuesto_id in self.compuestos_id]
            setattr(self, nombre_parametros, resultado)
            return resultado

    def antoine(self):
        """Retorna los parametros de la ecuación de antoine"""
        return self._solicitar_datos(Antoine)

    def cp_gas_polinomial(self):
        """Retorna los parametros a utilizar en la ecuación para calculo de capacidades
        calorificas de gas en forma polinomial encontrada en el Perry"""
        return self._solicitar_datos(CapacidadesCalorificasGasPolinomial)

    def cp_liquido(self):
        """Retorna los parametros a utilizar en la ecuación para calculo de capacidades
        calorificas de liquido encontrada en el Perry"""
        return self._solicitar_datos(CapacidadesCalorificasLiquido)

    def constantes_criticas(self):
        """Retorna las constantes criticas de los componentes"""
        return self._solicitar_datos(ConstantesCriticasFactoresAcentricos)

    def cp_gas_hiperbolico(self):
        """Retorna los parametros a utilizar en la ecuación para calculo de capacidades
        calorificas de gas en forma hiperbolica encontrada en el Perry"""
        return self._solicitar_datos(CpGasHiperbolico)

    def calor_vaporizacion(self):
        """Retorna los parametros a utilizar en la ecuación para el calculo de calor de
        vaporización de liquidos encontrada en el Perry"""
        return self._solicitar_datos(CalorVaporizacionLiquidos)

    def temperaturas_criticas(self):
        """Retorna las temperaturas criticas de los componentes simulados"""
        return [parametros_criticos.Tc for parametros_criticos in self.constantes_criticas()]


class Parametros(GestorParametros):
    """Gestor de parametros propio de cada componente"""

    def __init__(self, nombre_compuesto):
        self.compuesto = nombre_compuesto.upper()
        self.compuesto_id = session.query(Componentes.id). \
            filter_by(NAME=self.compuesto).scalar()

    def _solicitar_datos(self, clase):
        """
        Realiza la solicitud a la base de datos para obtener los datos necesarios del componente
        :param clase: instancia de orm para solicitud a base de datos
        :return: Una lista con objetos que representan las filas
        """
        nombre_parametros = self.ORM_parametros[clase]
        if hasattr(self, nombre_parametros):
            return getattr(self, nombre_parametros)
        else:
            resultado = session.query(clase).get(self.compuesto_id)
            setattr(self, nombre_parametros, resultado)
            return resultado
