"""Paquetes termodinamicos"""

import logging
from functools import partial

import numpy as np
from scipy.optimize import newton

from simnav.termodinamica import ideal
from simnav.datos import GestorParametros

from .utilidades import sumar_filas, soporte_numpy_2d, soporte_scalar


class PaqueteIdeal:
    """Paquete termodinamico ideal"""

    nombre = "Ideal"

    # Variables para guardar valores de propiedades constantes. Como lo es la entalpia de
    # vaporizacion a T de referencia
    _entalpias_vaporizacion = None


    numero_compuestos = 0
    parametros = None  # Gestor de parametros
    temperaturas_ref = None  # Array de temperaturas de referencia

    def __init__(self, compuestos):
        """
        Inicializa el paquete termodinamico con una referencia a los compuestos de la
        simulación
        :param compuestos: Lista de compuestos
        """
        self.compuestos = compuestos
        self.parametros = GestorParametros(self.compuestos)

        # Funciones vectorizadas
        self.entalpia_cp = np.vectorize(ideal.entalpia_cp, excluded=['T1', 'ecuacion_cp'])


        # Variables para guardar valores de propiedades constantes. Como lo es la entalpia de
        # vaporizacion a T de referencia
        self._entalpias_vaporizacion = None

        self.numero_compuestos = 0
        self.temperaturas_ref = None  # Array de temperaturas de referencia

        # Logging
        self.logger = logging.getLogger(__name__)

    def preparar(self):
        """Metodo a ser llamado antes de iniciar la simulacion"""
        self.logger.debug("Preparando paquete termodinamico")
        self.numero_compuestos = len(self.compuestos)
        self.parametros = GestorParametros(self.compuestos)

        # Temperatura de referencia (h=0, s=0 para liquido saturado a 1atm)
        self.temperaturas_ref = np.array(self.temperatura_saturacion(101325))

    def actualizar(self):
        """Actualiza la instancia del objeto con los nuevos compuestos.
        Se usa cuando la lista de compuestos a sido modificada"""
        self.__init__(self.compuestos)

    @soporte_scalar
    def presion_vapor(self, temperatura):
        """Retorna la presion de vapor de cada compuesto para la temperatura dada"""
        presiones_vapor = np.zeros((temperatura.size, self.numero_compuestos))
        for indice, parametros in enumerate(self.parametros.antoine()):
            presiones_vapor[:, indice] = ideal.antoine(temperatura,
                                                       parametros.C1,
                                                       parametros.C2,
                                                       parametros.C3,
                                                       parametros.C4,
                                                       parametros.C5)
        return presiones_vapor

    def temperatura_saturacion(self, presion_saturacion):
        """Retorna la temperatura de saturación para la presión dada"""
        temperatura_saturacion = np.zeros(self.numero_compuestos)
        for indice, parametros in enumerate(self.parametros.antoine()):
            ecuacion_presion_vapor = partial(ideal.antoine,
                                             C1=parametros.C1,
                                             C2=parametros.C2,
                                             C3=parametros.C3,
                                             C4=parametros.C4,
                                             C5=parametros.C5)
            # Ecuacion igual a cero en funcion de la temperatura. 0 = presion
            ec_saturacion = (lambda temp, presion_saturacion: presion_saturacion
                                                              - ecuacion_presion_vapor(temp))
            temperatura_saturacion[indice] = newton(ec_saturacion,
                                                    x0=300,
                                                    args=(presion_saturacion,))
        return temperatura_saturacion

    def coeficiente_reparto(self, temperatura, presion):
        """Retorna el coeficiente de reparto para cada compuesto a la temperatura y
        presion dada"""
        return self.presion_vapor(temperatura) / presion

    @soporte_scalar
    def entalpia_liquido_puro(self, temperatura):
        """Retorna la entalpia de liquido puro para la temperatura dada. Puede usarse
        con un escalar de temperatura o un array de numpy"""
        entalpia_liquido = np.zeros((temperatura.size, self.numero_compuestos))
        temperaturas_critica = self.parametros.temperaturas_criticas()

        for indice, parametros in enumerate(self.parametros.cp_liquido()):
            if int(parametros.Ecuacion) == 1:
                ecuacion_cp = partial(ideal.cp_liquido1,
                                      C1=parametros.C1,
                                      C2=parametros.C2,
                                      C3=parametros.C3,
                                      C4=parametros.C4,
                                      C5=parametros.C5)
            elif int(parametros.Ecuacion) == 2:
                ecuacion_cp = partial(ideal.cp_liquido2,
                                      Tc=temperaturas_critica[indice],
                                      C1=parametros.C1,
                                      C2=parametros.C2,
                                      C3=parametros.C3,
                                      C4=parametros.C4)
            else:
                print('Parametro Ecuacion mal formateado')

            entalpia_liquido[:, indice] = self.entalpia_cp(T1=self.temperaturas_ref[indice],
                                                           T2=temperatura,
                                                           ecuacion_cp=ecuacion_cp)
        return entalpia_liquido

    def entalpia_liquido(self, composicion, temperatura):
        """Retorna la entalpia de una mezcla en estado liquido"""
        return sumar_filas(self.entalpia_liquido_puro(temperatura) * composicion)

    @soporte_scalar
    def entalpia_vapor_puro(self, temperatura):
        """Retorna el cambio de entalpia desde el estado de referencia (liquido saturado a
        1 atm) hasta la temperatura provista"""
        entalpias_vapor = np.zeros((temperatura.size, self.numero_compuestos))

        # La entalpia del vapor desde el estado de referencia (liquido saturado a 1 atm)
        # sera la sumatoria de el delta de vaporacion mas el cambio de entalpia desde
        # el vapor saturado hasta la temperatura actual del vapor. Se inicia con el
        # calculo de la entalpia de vaporización
        entalpias_vaporizacion = self.entalpia_vaporizacion()

        # parametros
        p_polinomiales = self.parametros.cp_gas_polinomial()
        p_hiperbolicos = self.parametros.cp_gas_hiperbolico()

        # Funcion auxiliar para calcular el delta de entalpia que ocurre en el vapor.
        def delta_entalpia(temperatura_inicial, temperatura_final, ecuacion, parametros):
            """Retorna el delta de entalpia entre las temperaturas dadas usando
            la ecuacion indicada
            ecuacion == 0 para la ecuacion polinomial
            ecuacion == 1 para la ecuacion hiperbolica
            parametros: parametros de la ecuacion a utilizar
            """
            if ecuacion == 0:
                ecuacion_cp = partial(ideal.cp_polinomial,
                                      C1=parametros.C1,
                                      C2=parametros.C2,
                                      C3=parametros.C3,
                                      C4=parametros.C4,
                                      C5=parametros.C5)
            if ecuacion == 1:
                ecuacion_cp = partial(ideal.cp_hiperbolico,
                                      C1=parametros.C1,
                                      C2=parametros.C2,
                                      C3=parametros.C3,
                                      C4=parametros.C4,
                                      C5=parametros.C5)

            return ideal.entalpia_cp(T1=temperatura_inicial,
                                     T2=temperatura_final,
                                     ecuacion_cp=ecuacion_cp)

        # Temperatura a temperatura para todos los componentes se comprueba que ecuacion
        # utilizar en cada caso. Se debe comprobar en que ecuacion cae la temperatura de
        # referencia y en cual cae la temperatura del fluido. 0 corresponde a la ec polinomial.
        # 1 para la hiperbolica
        # TODO: Agregar logeo en caso de salida de los rangos permitidos
        # TODO: Documentar mejor esta parte.
        # TODO: Refactor this.
        lista_parametros = [p_polinomiales,
                            p_hiperbolicos]  # Lista de parametros para facilidad de uso.
        for i in range(self.numero_compuestos):
            if p_polinomiales[i]:  # Solo 60 componentes poseen parametros polinomiales
                ec_Tref = 0 if self.temperaturas_ref[i] < p_polinomiales[i].TmaxK else 1
                ec_Treal = None
            else:
                ec_Tref = 1
                ec_Treal = 1
            for n in range(temperatura.size):
                if ec_Treal is None:
                    ec_Treal = 0 if temperatura[n] < p_polinomiales[i].TmaxK else 1
                if ec_Tref == ec_Treal:
                    delta_vapor = delta_entalpia(temperatura_inicial=self.temperaturas_ref[i],
                                                 temperatura_final=temperatura[n],
                                                 ecuacion=ec_Treal,
                                                 parametros=lista_parametros[ec_Treal][i])
                else:
                    if temperatura[n, i] > self.temperaturas_ref[i]:
                        temp_cambio_ec = p_polinomiales[i].TmaxK
                    else:
                        temp_cambio_ec = p_hiperbolicos[i].TminK

                    # desde la T_ref hasta cambio de ec
                    delta_vapor_1 = delta_entalpia(
                        temperatura_inicial=self.temperaturas_ref[i],
                        temperatura_final=temp_cambio_ec,
                        ecuacion=ec_Tref,
                        parametros=lista_parametros[ec_Tref][i])

                    # desde cambio de ec hasta T_final
                    delta_vapor_2 = delta_entalpia(
                        temperatura_inicial=temp_cambio_ec,
                        temperatura_final=temperatura[n, i],
                        ecuacion=ec_Treal,
                        parametros=lista_parametros[ec_Treal][i])

                    delta_vapor = delta_vapor_1 + delta_vapor_2
                entalpias_vapor[n, i] = delta_vapor + entalpias_vaporizacion[i]

        return entalpias_vapor

    def entalpia_vapor(self, composicion, temperatura):
        """Retorna la entalpia de una mezcla en estado vapor"""
        return sumar_filas(self.entalpia_vapor_puro(temperatura) * composicion)

    def entalpia_vaporizacion(self):
        """Retorna la entalpia de vaporizacion para cada componente a la temperatura
        de referencia de cada uno de estos (liquido saturado a 1atm)"""
        temperaturas_criticas = self.parametros.temperaturas_criticas()

        # Se retornan las entalpias de vaporización previamente calculadas si lo han sido.
        if self._entalpias_vaporizacion is not None:
            return self._entalpias_vaporizacion

        entalpias = []
        datos = zip(temperaturas_criticas,
                    self.parametros.calor_vaporizacion(),
                    self.temperaturas_ref)
        for temperatura_critica, parametros, temperatura_referencia in datos:
            entalpias.append(ideal.calor_vaporizacion(T=temperatura_referencia,
                                                      Tc=temperatura_critica,
                                                      C1=parametros.C1,
                                                      C2=parametros.C2,
                                                      C3=parametros.C3,
                                                      C4=parametros.C4))

        return entalpias

    def fraccion_vapor(self, fracciones_liquido, temperatura, presion):
        """Retorna la fraccion de vapor ideal para las condiciones dadas"""
        return ideal.raoult_vapor(fracciones_liquido, self.presion_vapor(temperatura), presion)

    def fraccion_liquido(self, fracciones_vapor, temperatura, presion):
        """Retorna la fraccion de liquido ideal para las condiciones dadas"""
        return ideal.raoult_liquido(fracciones_vapor, self.presion_vapor(temperatura), presion)

    @soporte_numpy_2d
    def temperatura_burbuja(self, composicion_liquido, presion, temperatura_inicial=None):
        """
        Punto de burbuja de una mezcla multicomponente ideal. Cumpliendo la condición de que la
        sumatoria de los componentes en fase gaseosa(y) es igual a 1.
        :param composicion_liquido: composicion en fraccion molar de la fase liquida
        :param presion: presion del sistema
        :param temperatura_inicial: temperatura inicial para la determinación del punto de burbuja
        :return: punto de burbuja para la mezcla
        """

        if temperatura_inicial is None:
            # En caso de no proveer temperatura inicial, esta sera dada por la contribucion
            # de la temperatura de saturacion pura de cada componente
            temperatura_inicial = np.sum(composicion_liquido * self.temperaturas_ref)

        def sumatoria_fraccion_vapor(temperatura, _composicion_liquido, _presion):
            """Determinacion de la sumatoria de las fracciones de vapor (y). Siguiendo la ecuacion
            ideal"""
            fracciones_vapor = self.fraccion_vapor(_composicion_liquido, temperatura, _presion)
            return 1 - np.sum(fracciones_vapor)

        return newton(sumatoria_fraccion_vapor, temperatura_inicial,
                      args=(composicion_liquido, presion))

    @soporte_numpy_2d
    def temperatura_rocio(self, composicion_vapor, presion, temperatura_inicial=None):
        """
        Punto de burbuja de una mezcla multicomponente ideal. Cumpliendo la condición de que la
        sumatoria de los componentes en fase gaseosa(y) es igual a 1.
        :param composicion_vapor: composicion en fraccion molar de la fase liquida
        :param presion: presion del sistema
        :param temperatura_inicial: temperatura para la determinación del punto de burbuja
        :return: punto de burbuja para la mezcla
        """
        if temperatura_inicial is None:
            # En caso de no proveer temperatura inicial, esta sera dada por la contribucion
            # de la temperatura de saturacion pura de cada componente
            temperatura_inicial = np.sum(composicion_vapor * self.temperaturas_ref)

        # TODO: Derivar esto.
        def sumatoria_fraccion_liquido(temperatura, composicion_vapor, presion):
            fracciones_liquido = self.fraccion_liquido(composicion_vapor, temperatura, presion)
            return 1 - np.sum(fracciones_liquido)

        return newton(sumatoria_fraccion_liquido, temperatura_inicial,
                      args=(composicion_vapor, presion))

    @soporte_numpy_2d
    def calidad_vapor(self, composicion, temperatura, presion):
        """Determina la calidad del vapor para una mezcla en equilibrio liquido-vapor"""
        K = self.coeficiente_reparto(temperatura, presion)

        # Valor inicial para iteracion
        calidad_inicial = 0.5  # TODO: MEJORAR ESTO

        funcion = lambda q, z, k: sumar_filas(z / (K + q * (1 - K))) - 1
        funcion_prima = lambda q, z, k: sumar_filas(- (z * (1 - K) / (K + q * (1 - K)) ** 2))

        calidad = 1 - newton(funcion, calidad_inicial, funcion_prima, args=(composicion, K))[0]
        if calidad < 0 or calidad > 1:
            raise RuntimeError(f"La calidad del vapor {calidad} esta fuera de rango (0, 1)")
        else:
            return calidad

    def entalpia(self, composicion, temperatura, presion, calidad_vapor=None):
        """Determina la entalpia de una mezcla multicomponentes. La funcion define el estado
        termodinamico de la mezcla usando la temperatura de burbuja y rocio. Si la mezcla
        esta ene estado liquido-vapor, calcula la calidad del vapor y determina la entalpia
        en funcion de la contribucion de cada una de las fases de la mezcla.
        ::param composicion:: composicion de la mezcla
        ::param temperatura:: temperatura de la mezcla
        ::param presion:: presion del sistema
        ::calidad_vapor:: calidad del vapor si se tiene, en caso de no tenerlo se calcula.
        ::return:: la entalpia de la mezcla
        """

        # Identificacion de estado:
        estado = self.estado(composicion, temperatura, presion, como_numero=True)
        if estado == 0:
            # Vapor
            return self.entalpia_liquido(composicion, temperatura)
        elif estado == 1:
            # Liquido
            return self.entalpia_vapor(composicion, temperatura)
        else:
            # Liquido-Vapor
            if calidad_vapor is None:
                calidad_vapor = self.calidad_vapor(composicion, temperatura, presion)
            composicion_liquido = self.composicion_fase_liquida(composicion,
                                                                temperatura,
                                                                presion,
                                                                calidad_vapor)
            composicion_vapor = self.fraccion_vapor(composicion_liquido,
                                                    temperatura,
                                                    presion)
            entalpia_liquido = self.entalpia_liquido(composicion_liquido,
                                                     temperatura)
            entalpia_vapor = self.entalpia_vapor(composicion_vapor,
                                                 temperatura)
            return entalpia_vapor * calidad_vapor + entalpia_liquido * (1 - calidad_vapor)

    def composicion_fase_liquida(self, composicion, temperatura, presion, calidad_vapor):
        """Determina la composición de la fase liquida de una mezcla liquido-vapor
        ::param composicion:: composicion total de la mezcla liquido-vapor
        ::return :: La composicion de la fase liquida de la mezcla
        """
        K = self.coeficiente_reparto(temperatura, presion)
        return composicion / (K + calidad_vapor * (1 - K))

    def estado(self, composicion, temperatura, presion, como_numero=False):
        """
        Identifica el estado termodinamico de una mezcla
        :param composicion: composicion de la mezcla
        :param temperatura: temperatura de la mezcla
        :param presion: presion de la mezcla
        :param como_numero: cambia la forma en como se retorna el estado termodinamico
        :return: el estado del sistema. Si como_numero es Verdadero retorna el estado como un
        numero: 0 para liquido, 1 para vapor, 2 para mezcla liquido-vapor. Si como_numero es
        false retorna una palabra que identifica el estado
        """
        print('estado', composicion, temperatura, presion)
        temperatura_burbuja = self.temperatura_burbuja(composicion_liquido=composicion,
                                                       presion=presion,
                                                       temperatura_inicial=temperatura)

        temperatura_rocio = self.temperatura_rocio(composicion_vapor=composicion,
                                                   presion=presion,
                                                   temperatura_inicial=temperatura)

        if como_numero:
            estado = [0, 1, 2]
        else:
            estado = ['Liquido', 'Vapor', 'Mezcla liquido-vapor']

        if temperatura <= temperatura_burbuja:
            return estado[0]

        elif temperatura >= temperatura_rocio:
            return estado[1]

        if temperatura_burbuja < temperatura < temperatura_rocio:
            return estado[2]
