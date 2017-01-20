"""Utilidades para el manejo de compuestos y corrientes"""


def compuestos_corriente(*corrientes):
    """Retorna una tupla con referencias a los compuestos de la/s corrientes introducidas"""
    _compuestos_encontrados = list()
    for corriente in corrientes:
        for compuesto, fraccion in corriente:
            if compuesto not in _compuestos_encontrados:
                _compuestos_encontrados.append(compuesto)
    return tuple(_compuestos_encontrados)
