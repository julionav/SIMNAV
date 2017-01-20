"""Clases de pruebas base para el simulador"""

"""Pruebas para el paquete de termodinamica de simnav"""

from pytest import approx

import numpy as np

from CoolProp import CoolProp as CP

from simnav.corrientes import Compuesto
from simnav.termodinamica.paquetes import PaqueteIdeal
from simnav.opus.destilacion import DestilacionSemiRigurosa

