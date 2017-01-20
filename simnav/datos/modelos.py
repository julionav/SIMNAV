from .base_de_datos import db_reflection

"""
Accesa a la base de datos sqlite para obtener las tablas de propiedades de los componentes como objetos.
"""

Base, session = db_reflection('sqlite:///propiedades.sqlite')

# Asignando clases generadas por SQLalchemy
CapacidadesCalorificasLiquido = Base.classes.capacidades_calorificas_liquido
CapacidadesCalorificasGasPolinomial = Base.classes.Capacidades_calorificas_gas_polinomial
Componentes = Base.classes.componentes
ConstantesCriticasFactoresAcentricos = Base.classes.Constantes_criticas_y_factores_acentricos
CpGasHiperbolico = Base.classes.Cp_para_gas_de_forma_hiperbolica
Antoine = Base.classes.Parametros_ecuacion_de_antoine
CalorVaporizacionLiquidos = Base.classes.Calor_de_vaporizacion_de_liquidos


