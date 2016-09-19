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

        return query.first()
"""
    def get_parametros_antoine(self, id):
        parametros_antoine = self.tables['Parametros_ecuacion_de_antoine']
        query = self.session.query(compoen)
        """