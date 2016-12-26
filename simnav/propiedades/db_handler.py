# -*- coding: utf-8 -*-


"""
Dynamic reflecting of an existing db using SQLalchemy

"""

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


def db_reflection(connection_string):
    """
    Reflects an existing db to use his data.
    :param connection_string:
    :return: A dict containing all the tables in the given db and a session.
    """
    # Creating the engine
    engine = create_engine(connection_string, echo=False)

    # Reflecting the db
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    # Session
    session = Session(engine)
    return Base, session

