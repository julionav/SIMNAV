from .db_handler import db_reflection

"""
Accesa a la base de datos sqlite para obtener las tablas de propiedades de los componentes
"""

Base, sesion = db_reflection('sqlite:///propiedades.sqlite')

# Asignando clases generadas por SQLalchemy
Componentes = Base.classes.componentes
CapacidadesCalorificasLiquido = Base.classes.capacidades_calorificas_liquido
