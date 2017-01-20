def parse_components(compuestos, composicion):
    """Retorna un string con los nombres y composicion de los componentes compatible con
    PropsSI de CoolProp"""
    formatted_string = ''
    string_items = [f'{compuesto.nombre}[{fraccion}]' for compuesto, fraccion
                    in zip(compuestos, composicion)]
    return '&'.join(string_items)


def error_relativo(valor_calculado, valor_real):
    return abs((valor_calculado - valor_real) / valor_real) < 1