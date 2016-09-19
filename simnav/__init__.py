import db_engine
import numpy as np

db = db_engine.DbEngine()

comps = ['BENZENE', 'TOLUENE']

list(map(db.get_id, comps))

print(a)