# -*- coding: utf-8 -*-


'''
Created on 18/09/2016

@author: Julio Navarro
'''

from db.dynamic_reflect import DbReflection


class DbEngine:

    def __init__(self):
        self.db = DbReflection('sqlite:///db/simnavDB.sqlite')
        self.tables = self.db.dynamic_reflect()
        self.session = self.db.session()

    def get_id(self, componente):

        componentes = self.tables['Lista_de_componentes']
        query = self.session.query(componentes.id).\
            filter_by(NAME=componente)
        for id, in query:
            return id

    def get_parametros_antoine(self, componente):
        parametros_antoine = self.tables['Parametros_ecuacion_de_antoine']
        query = self.session.query(parametros_antoine).\
            filter_by(NAME=componente).all()
        for parametros in query:
            C1 = parametros.C1
            C2 = parametros.C2
            C3 = parametros.C3
            C4 = parametros.C4
            C5 = parametros.C5
            TminK = parametros.TminK
            PaTminK = parametros.PaTmin
            TmaxK = parametros.TmaxK
            PaTmax = parametros.PaTmax

        return(C1, C2, C3, C4, C5, TminK, PaTminK, TmaxK, PaTmax)

    def get_calor_vaporizacion_liquidos(self, componente):
        calor_vaporizacion_liquidos = self.tables[
            'Calor_de_vaporizacion_de_liquidos']
        query = self.session.query(calor_vaporizacion_liquidos).\
            filter_by(NAME=componente).all()

        for parametros in query:
            C1 = parametros.C1x1e_7 * 1 ** (-7)
