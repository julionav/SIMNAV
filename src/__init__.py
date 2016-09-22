import db_engine

db = db_engine.DbEngine()

comps = ['BROMINE', 'TOLUENE']

print(list(map(db.get_parametros_antoine, comps)))
