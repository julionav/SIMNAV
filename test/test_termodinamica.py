"""Pruebas para el paquete de termodinamica de simnav"""

import numpy as np

from CoolProp import CoolProp as CP

from simnav.corrientes import Compuesto
from simnav.termodinamica.paquetes import PaqueteIdeal
from simnav.opus.destilacion import DestilacionSemiRigurosa

from .utilidades import parse_components, error_relativo

# TODO: Crear componentes de forma aleatoria y realizar pruebas a cada uno de ellos. Al menos
# 100 componentes por prueba. Tambien debe ser aleatorios todos los parametros.
class TestPaqueteIdeal:
    """Realiza pruebas al paquete termodinamico ideal"""

    compuestos = [Compuesto('benzene'), Compuesto('toluene')]
    paquete = PaqueteIdeal(compuestos)
    numero_compuestos = len(compuestos)

    # Parametros a utilizar en las pruebas
    composicion = np.array([0.5, 0.5])
    composicion_2d = np.array(([0.5, 0.5], [0.3, 0.7], [0.1, 0.9], [0, 1]))
    mezcla_coolprop = parse_components(compuestos, composicion)

    @property
    def compuestos_CP(self):
        return parse_components(self.compuestos, self.composicion)

    def test_presion_vapor(self):
        temperatura = 300
        temperatura_numpy = np.array([300, 350, 400])
        presion_vapor = self.paquete.presion_vapor(temperatura)
        presion_vapor_numpy = self.paquete.presion_vapor(temperatura_numpy)
        for j in range(len(self.compuestos)):
            for i in range(temperatura_numpy.size):
                presion_cp = CP.PropsSI('P', 'T', temperatura_numpy[i], 'Q', 0,
                                        self.compuestos[j].nombre)
                error_relativo = np.abs((presion_vapor_numpy[i, j] - presion_cp) / presion_cp)
                assert error_relativo <= 1

        for presion, compuesto in zip(presion_vapor, self.compuestos):
            presion_cp = CP.PropsSI('P', 'T', temperatura, 'Q', 0, compuesto.nombre)
            error_rel = abs((presion - presion_cp) / presion_cp)
            assert error_rel <= 1

    def test_coeficiente_reparto(self):
        temperatura = np.array([300, 350, 400])
        presion = np.array(([101325, 110000, 150000]))
        coeficiente_reparto = self.paquete.coeficiente_reparto(temperatura, 101325)
        for j in range(len(self.compuestos)):
            for i in range(temperatura.size):
                presion_cp = CP.PropsSI('P', 'T', temperatura[i], 'Q', 0,
                                        self.compuestos[j].nombre)
                coeficiente_reparto_cp = presion_cp / presion[i]
                error_relativo = np.abs((coeficiente_reparto[i, j] - coeficiente_reparto_cp)
                                        / coeficiente_reparto_cp)
                assert error_relativo <= 1

    def test_entalpia_liquido_puro(self):
        temperaturas = np.array((300, 325, 350))
        entalpia_liquido = self.paquete.entalpia_liquido_puro(temperaturas)
        for j in range(len(self.compuestos)):
            for i in range(temperaturas.size):
                entalpia_liquido_cp = CP.PropsSI('Hmolar', 'P', 101325, 'T', temperaturas[i],
                                                 self.compuestos[j].nombre)
                error_relativo = np.abs((entalpia_liquido[i, j] - entalpia_liquido_cp)
                                        / entalpia_liquido_cp)
                assert error_relativo <= 1

    def test_entalpia_vaporizacion(self):
        calores_vaporizacion = self.paquete.entalpia_vaporizacion()
        for j in range(len(self.compuestos)):
            entalpia_vapor_cp = CP.PropsSI('Hmolar', 'P', 101325, 'Q', 1,
                                           self.compuestos[j].nombre)
            entalpia_liquido_cp = CP.PropsSI('Hmolar', 'P', 101325, 'Q', 0,
                                             self.compuestos[j].nombre)
            calor_vaporizacion_cp = entalpia_vapor_cp - entalpia_liquido_cp
            error_relativo = abs((calores_vaporizacion[j] - calor_vaporizacion_cp)
                                 / calor_vaporizacion_cp)
            assert error_relativo <= 1

    def test_entalpia_vapor_puro(self):
        # Prueba usando un scalar
        temperatura = 500
        entalpia_vapor = self.paquete.entalpia_vapor_puro(temperatura)
        for j in range(self.numero_compuestos):
            entalpia_vapor_cp = CP.PropsSI('Hmolar', 'P', 101325, 'T', temperatura,
                                           self.compuestos[j].nombre)
            assert error_relativo(entalpia_vapor[j], entalpia_vapor_cp)

        # Prueba usando un array
        temperaturas = np.array((400, 425, 450))
        entalpias_vapor = self.paquete.entalpia_vapor_puro(temperaturas)
        for j in range(len(self.compuestos)):
            for i in range(temperaturas.size):
                entalpia_vapor_cp = CP.PropsSI('Hmolar', 'P', 101325, 'T', temperaturas[i],
                                               self.compuestos[j].nombre)
                assert error_relativo(entalpias_vapor[i, j], entalpia_vapor_cp)

    def test_entalpia_vapor(self):
        temperatura = 500
        entalpia_mezcla_vapor = self.paquete.entalpia_vapor(composicion=self.composicion,
                                                            temperatura=temperatura)
        entalpia_mezcla_vapor_cp = CP.PropsSI('Hmolar', 'P', 101325, 'T', temperatura,
                                              self.compuestos_CP)

        assert error_relativo(entalpia_mezcla_vapor, entalpia_mezcla_vapor_cp)

    def test_entalpia_liquido(self):
        temperatura = 300
        entalpia_mezcla_liquido = self.paquete.entalpia_liquido(composicion=self.composicion,
                                                                temperatura=temperatura)
        entalpia_mezcla_liquido_cp = CP.PropsSI('Hmolar', 'P', 101325, 'T', temperatura,
                                                self.compuestos_CP)
        assert error_relativo(entalpia_mezcla_liquido, entalpia_mezcla_liquido_cp)

    def test_temperatura_saturacion(self):
        presion = 101325
        temperaturas_saturacion = self.paquete.temperatura_saturacion(presion)

        assert temperaturas_saturacion[0] - 353.2 <= 1  # Teb normal benceno
        assert temperaturas_saturacion[1] - 383.15 <= 1  # Teb normal toluene

    def test_temperatura_burbuja_1d(self):
        """Prueba de la temperatura de burbuja usando un array de 1d"""
        presion = 101325
        temperatura_burbuja = self.paquete.temperatura_burbuja(self.composicion,
                                                               presion=presion)
        temperatura_burbuja_cp = CP.PropsSI('T', 'P', presion, 'Q', 0,
                                            parse_components(self.compuestos,
                                                             self.composicion))
        assert error_relativo(temperatura_burbuja, temperatura_burbuja_cp)

    def test_temperatura_burbuja_2d(self):
        presiones = np.array([101325, 200000, 300000, 500000])
        temperaturas_burbuja_2d = self.paquete.temperatura_burbuja(self.composicion_2d,
                                                                   presion=presiones)
        for i in range(len(presiones)):
            temperatura_burbuja_cp = CP.PropsSI('T', 'P', presiones[i], 'Q', 0,
                                                parse_components(self.compuestos,
                                                                 self.composicion_2d[i]))
            assert error_relativo(temperaturas_burbuja_2d[i], temperatura_burbuja_cp)

    def test_temperatura_rocio_1d(self):
        """Prueba el calculod de temperatura de rocio"""
        presion = 101325
        temperatura_rocio = self.paquete.temperatura_rocio(self.composicion,
                                                           presion=presion)
        temperatura_rocio_cp = CP.PropsSI('T', 'P', presion, 'Q', 1,
                                          parse_components(self.compuestos,
                                                           self.composicion))
        assert error_relativo(temperatura_rocio, temperatura_rocio_cp)

    def test_temperatura_rocio_2d(self):
        presiones = np.array([101325, 200000, 300000, 500000])
        temperaturas_rocio_2d = self.paquete.temperatura_rocio(self.composicion_2d,
                                                               presion=presiones)
        for i in range(len(presiones)):
            temperatura_rocio_cp = CP.PropsSI('T', 'P', presiones[i], 'Q', 1,
                                              parse_components(self.compuestos,
                                                               self.composicion_2d[i]))
            assert error_relativo(temperaturas_rocio_2d[i], temperatura_rocio_cp)

    def test_calidad_vapor(self):
        """Coolprop no soporta calculos para equilibrio liquido-vapor"""


