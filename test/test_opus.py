"""Pruebas para las operaciones unitarias de simnav"""

from pytest import approx

import numpy as np

from CoolProp import CoolProp as CP

from simnav.corrientes import Compuesto, CorrienteMateria
from simnav.termodinamica.paquetes import PaqueteIdeal
from simnav.opus.destilacion import DestilacionSemiRigurosa


class TestDestilacionSemiRigurosa:
    platos = 10
    compuestos = [Compuesto('benzene'), Compuesto('toluene')]
    paquete = PaqueteIdeal(compuestos)
    numero_compuestos = len(compuestos)
    corriente_entrada = CorrienteMateria(flujo=100000,
                                         temperatura=381.483,
                                         compuestos=compuestos,
                                         composicion=[0.5, 0.5],
                                         paquete_termodinamico=paquete)

    torre = DestilacionSemiRigurosa(numero_platos=10,
                                    destilado=55000,
                                    reflujo=1.5,
                                    corrientes_entrada=[(corriente_entrada, 5)],
                                    corrientes_salida='we need this',
                                    paquete_termodinamico=paquete)

    def test_respuesta(self):
        self.torre.calcular(destilador_parcial=True)