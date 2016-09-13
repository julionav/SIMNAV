# -*- coding: utf-8 -*-


"""
Dynamic reflecting of an existing db using SQLalchemy

"""

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class DbReflection:

    def __init__(self, connection_string):
        self.connection_string = connection_string

    def create_sa_connection(self):
        
        engine = create_engine(self.connection_string, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        return engine, session

    def reflect_db(self):
        # Get the engine and the session we need to use engine for core and session for orm
        engine, session = self.create_sa_connection()

        # Reflect the database to allow for declarative and using core
        Base = automap_base()
        Base.prepare(engine, reflect=True)

        return Base

    def dynamic_reflex(self):
        tables = {}
        Base = self.reflect_db()

        for key in Base.classes.keys():
            tables[key] = Base.classes.get(key)

        return tables
# TEST
db = DbReflection('sqlite:///simnavDB.sqlite')
session = db.create_sa_connection()[1]
tables = db.dynamic_reflec()
query = session.query(tables['Lista_de_componentes']).all()

for row in query:
    print (row.id)
