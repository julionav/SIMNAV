from CoolProp import CoolProp as CP

from simnav.corrientes.materia import CorrienteMateria, Compuesto
from simnav.termodinamica.paquetes import PaqueteIdeal

from .utilidades import parse_components, error_relativo


class TestCorrientes:
    compuestos = [Compuesto('benzene'), Compuesto('toluene')]
    paquete = PaqueteIdeal(compuestos)

    def test_parametros(self):
        composicion = [0.5, 0.5]
        corriente = CorrienteMateria(flujo=100,
                                     temperatura=300,
                                     compuestos=self.compuestos,
                                     composicion=composicion,
                                     paquete_termodinamico=self.paquete,
                                     nombre='CORRIENTE1')

        entalpia_cp = CP.PropsSI('Hmolar', 'T', 300, 'P', 101325 + 101325 / 14.96,
                                 parse_components(self.compuestos, composicion))
        assert corriente.estado == 'Liquido'
        assert corriente.nombre == 'CORRIENTE1'
        assert error_relativo(corriente.entalpia_especifica, entalpia_cp)
