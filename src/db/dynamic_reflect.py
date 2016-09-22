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

    def session(self):
        engine = self.engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def engine(self):

        engine = create_engine(self.connection_string, echo=False)
        return engine

    def reflect_db(self):
        engine = self.engine()

        # Reflect the database to allow for declarative and using core
        Base = automap_base()
        Base.prepare(engine, reflect=True)

        return Base

    def dynamic_reflect(self):
        tables = {}
        Base = self.reflect_db()

        for key in Base.classes.keys():
            tables[key] = Base.classes.get(key)

        return tables
