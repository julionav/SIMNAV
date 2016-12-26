from simnav.dynamic_reflec import DbReflection


# TEST
db = DbReflection('sqlite:///propiedades.sqlite')
session = db.create_sa_connection()[1]
tables = db.dynamic_reflec()
query = session.query(tables['Lista_de_componentes']).all()

for row in query:
    print(row.id)
