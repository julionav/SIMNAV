from .db_handler import db_reflection

"""
Accesa a la base de datos sqlite para obtener las tablas de propiedades de los componentes
"""

db = DbReflection('sqlite:///propiedades.sqlite')
tablas = db.dynamic_reflect()

"""
    def dynamic_reflect(self):
        "It return all the tables objects in the Db as a dict"
        tables = {}
        Base = self.reflect_db()

        for key in Base.classes.keys():
            tables[key] = Base.classes.get(key)

        return tables"""