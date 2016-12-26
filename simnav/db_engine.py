# -*- coding: utf-8 -*-


'''
Created on 18/09/2016

@author: Julio Navarro
'''

from .propiedades.dynamic_reflect import DbReflection


class ParameterHandler:
    """
    Clase encargada de manejar los parametros de la base de datos de simnav
    """
    db = DbReflection('sqlite:///propiedades.sqlite')
    tables = db.dynamic_reflect()
    session = db.session()

    def __init__(self, componentes):
        '''
        Se inicializa con los componentes requeridos
        '''
        self.componentes = componentes



    def _lazy_getdata(self, table, componente, constantes):
        """
        Retorna los parametros especificados de una tabla para los componentes
        dados
        """

        data = {}
        query = self.session.query(table).filter_by(NAME=componente).all()
        for row in query:
            for constante in constantes:
                data[constante] = (getattr(row, constante))
        return data

    def get_component_list(self):
        "Retorna todos los componentes de la base de datos"

        tabla_componentes = self.tables['Lista_de_componentes']
        query = self.session.query(tabla_componentes).all()

        for componente in query:
            yield componente

    def get_parametros_antoine(self):
        """
        Retorna los parametros de la ecuacion de antoine para los componentes
        dados
        """
        _tabla = self.tables['Parametros_ecuacion_de_antoine']
        for componente in self.componentes:

            _constantes = [
                            'C1', 'C2', 'C3',
                            'C4', 'C5', 'TminK',
                            'PaTmin', 'TmaxK', 'PaTmax'
                            ]

            parametros = self._lazy_getdata(_tabla,
                                            componente,
                                            _constantes)
            yield parametros

    def get_calor_vaporizacion_liquidos(self):
        """
        Retorna los parametros de para el calculo de calor de vaporización de
        liquidos para los componentes dados.
        """
        _tabla = self.tables['Calor_de_vaporizacion_de_liquidos']
        for componente in self.componentes:

            _constantes = [
                            'C1', 'C2', 'C3',
                            'C4', 'TminK', 'dH_a_Tmin',
                            'TmaxK', 'dH_a_Tmax'
                            ]

            parametros = self._lazy_getdata(_tabla,
                                            componente,
                                            _constantes)
            yield parametros

    def get_capacidades_calorificas_liquidos(self):
        """
        Retorna los parametros de para el calculo de capacidades calorificas
        de liquidos para los componentes dados
        """
        _tabla = self.tables['Capacidades_calorificas_de_liquidos']
        for componente in self.componentes:

            _constantes = [
                            'C1', 'C2', 'C3',
                            'C4', 'C5', 'TminK', 'cpTmin',
                            'TmaxK', 'cpTmax'
                            ]

            parametros = self._lazy_getdata(_tabla,
                                            componente,
                                            _constantes)
            yield parametros

    def get_capacidades_calorificas_gas_polinomial(self):
        """
        Retorna los parametros de para el calculo de capacidades
        calorifica de gas mediante una ecuacion polinomial
        para los componentes dados
        """
        _tabla = self.tables['Capacidades_calorificas_gas_polinomial']
        for componente in self.componentes:

            _constantes = [
                            'C1', 'C2', 'C3',
                            'C4', 'C5', 'TminK', 'cpTmin',
                            'TmaxK', 'cpTmax'
                            ]

            parametros = self._lazy_getdata(_tabla,
                                            componente,
                                            _constantes)
            yield parametros

    def get_capacidades_calorificas_gas_hiperbolico(self):
        """
        Retorna los parametros de para el calculo de capacidades
        calorifica de gas mediante una ecuacion polinomial
        para los componentes dados
        """
        _tabla = self.tables['Cp_para_gas_de_forma_hiperbolica']
        for componente in self.componentes:

            _constantes = [
                            'C1', 'C2', 'C3',
                            'C4', 'C5', 'TminK', 'cpTmin',
                            'TmaxK', 'cpTmax'
                            ]

            parametros = self._lazy_getdata(_tabla,
                                            componente,
                                            _constantes)
            yield parametros

    def get_constantes_criticas_y_factores_acentricos(self):
        """
        Retorna los parametros de para el calculo de capacidades
        calorifica de gas mediante una ecuacion polinomial
        para los componentes dados
        """
        _tabla = self.tables['Constantes_criticas_y_factores_acentricos']
        for componente in self.componentes:

            _constantes = [
                            'TcK', 'PcMpa', 'Vcm3/kmol',
                            'Zc', 'FACTORACENTRICO']


            parametros = self._lazy_getdata(_tabla,
                                            componente,
                                            _constantes)
            yield parametros



if __name__ == '__main__':
    comps = ['BENZENE', 'TOLUENE']
    db = ParameterHandler(comps)
    parametros0 = []
    parametros1 = []
    parametros2 = []
    parametros3 = []
    parametros4 = []
    parametros5 = []
    parametros6 = []

    # Test
    for constantes in db.get_parametros_antoine():
        parametros0.append(constantes)

    print('parametros_antoine', parametros0, parametros1,
          sep="\n", end='\n\n')

    for constantes in db.get_capacidades_calorificas_liquidos():
        parametros1.append(constantes)

    print('Capacidades_calorificas_liquidos', parametros1,
          sep="\n", end='\n\n')

    for constantes in db.get_calor_vaporizacion_liquidos():
        parametros2.append(constantes)

    print('calor_vaporizacion_liquidos', parametros2,
          sep="\n", end='\n\n')

    for constantes in db.get_capacidades_calorificas_gas_polinomial():
        parametros3.append(constantes)

    print('capacidades_calorificas_gas_polinomial', parametros3,
          sep="\n", end='\n\n')

    for constantes in db.get_capacidades_calorificas_gas_hiperbolico():
        parametros4.append(constantes)

    print('capacidades_calorificas_gas_hiperbolico', parametros4,
          sep="\n", end='\n\n')

    for constantes in db.get_constantes_criticas_y_factores_acentricos():
        parametros5.append(constantes)

    print('capacidades_calorificas_gas_hiperbolico', parametros5,
          sep="\n", end='\n\n')
