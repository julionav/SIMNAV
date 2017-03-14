"""Modelos matematicos para operaciones unitarias de destilación"""
import logging

import numpy as np

from simnav.metodos_matematicos import metodo_tomas


class DestilacionSemiRigurosa:
    """
    Modelo matematico estacionario de una torre de destilacion de platos para sistemas
    multicomponentes con un condensador parcial resuelto con una matriz tridiagonal
    """

    def __init__(self, numero_platos=10, destilado=50, reflujo=1.5, alimentaciones=[],
                 salidas_laterales=[], paquete_termodinamico=None, presion=101325):
        """
        :param numero_platos: numero de platos de la torre
        :param destilado: flujo de destilado de la torre (kmol/h)
        :param reflujo: relacion de reflujo de la torre
        :param alimentaciones: lista de corrientes de alimentacion [plato, corriente]
        :param salidas_laterales: lista de flujos (kmol/h) de salida lateral [plato, flujo]
        :param paquete_termodinamico: instancia del un paquete termodinamico
        :param presion:
        """
        self.numero_platos = numero_platos  # Numero de platos de la torre
        self.reflujo = reflujo  # Relación de reflujo
        self.destilado = destilado  # Flujo de destilado de la torre
        self.alimentaciones = alimentaciones  # en la forma (corriente, plato)
        self.salidas_laterales = salidas_laterales  # en la forma (flujo, plato)
        self.presion = presion
        self.propiedades = paquete_termodinamico
        self.condensador = "Parcial"

        # Logging
        self.logger = logging.getLogger(__name__)

    def simular(self):
        """
        Determina las composciciones, flujos y temperaturas plato a plato en la torre
        """
        # Se crean referencias de atajo para los parametros de la torre
        N, R, D = self.numero_platos, self.reflujo, self.destilado
        NC = len(self.propiedades.compuestos)

        # Tipo de condensador
        condensador_parcial = self.condensador == 'Parcial'

        # Presion de cada plato. Considerando que no hay caida de presion.
        # TODO: Considerar caida de presion
        P = np.array([self.presion] * N)

        # Se inicializan los array que contendran las variables de calculo plato plato
        Q = np.zeros(N)  # Flujo de calor
        SL = np.zeros(N)  # Retiro de liquido  #TODO: Esto debe llenarse con corrientes salida
        SV = np.zeros(N)  # Retiro de vapor
        F = np.zeros(N)  # Flujo de materia de entrada
        zF = np.zeros((N, NC))  # Composicion de las corrientes de entrada
        hF = np.zeros(N)  # Entalpia de la alimentacion
        V = np.zeros(N)  # Flujo vapor
        V_nuevo = np.zeros(N)  # Valores nuevos de flujo de vapor. Para calculo de error
        x = np.zeros((N, NC))  # Composicion de los componentes plato a plato

        # Se toman los parametros necesarios de las corrientes de entrada
        self.logger.debug('Tomando los datos de las alimentaciones')
        for plato, corriente in self.alimentaciones:
            indice = plato - 1  # Los inidices de los array comienzan en 0. Los platos en 1
            F[indice] = corriente.flujo
            hF[indice] = corriente.entalpia_especifica
            zF[indice] = corriente.composicion

        # Valores iniciales de calculo
        if condensador_parcial:
            V[0] = D  # El flujo de vapor de salida por el tope (etapa 0) es igual al destilado
            V[1] = D * (R + 1)  # Flujo de vapor
            print(V[1])
            V[2:] = V[1]  # Se toma como valores iniciales para el flujo de vapor V1
        else:
            V[0] = D * (R + 1)
            V[1:] = V[0]  # TODO: Esto puede ser mejorado

        # TODO: La temperatura inicial deberia ser en funcion de las temperaturas de entrada
        T = np.linspace(300, N * 10, N)  # Temperatura plato a plato con valores iniciales

        # Se inicializan arrays para las variables de espacio de estado del modelo
        A = np.zeros(N)
        sum_materia = np.zeros(N)

        # Sumatoria de materia alimentada y extraida en cada etapa
        for n in range(N):
            sum_materia[n] = (F[:n + 1] - SV[:n + 1] - SL[:n + 1]).sum()

        # Valores iniciales de error de las variables T y V para iniciar iteracion
        errorT = 1000
        errorV = 1000

        # Contadores de iteraciones
        contador_T = 0
        contador_V = 0
        self.logger.debug('Iniciando Iteración de la destilación')
        # La iteración se realiza con 2 ciclos. El ciclo interior corrige la temperatura de los
        # y el exterior el flujo de vapor por los platos
        while errorV >= 0.0001:
            while errorT >= 0.0001:
                # Se inicia calculando el coeficiente de reparto
                K = self.propiedades.coeficiente_reparto(temperatura=T,
                                                         presion=self.presion)
                # Se calculan los parametros A, B, C y D.
                A[1:] = V[1:] + sum_materia[:-1] - D  # A[0] siempre es cero

                for i in range(NC):
                    B = -(np.append(V, 0)[1:] + sum_materia - D + SL + (V + SV) * K[:, i])
                    C = np.append(V[1:] * K[1:, i], 0)  # Se agrega un cero al final del array
                    E = -F * zF[:, i]

                    # Se utilizan las variables de estado calculadas para el calculo de
                    # composicion plato a plato usando el metodo de tomas para resolucion de
                    # matrices tridiagonales
                    x[:, i] = metodo_tomas(A, B, C, E)

                # Se normalizan las composiciones.
                for n in range(N):
                    x[n, :] = x[n, :] / sum(x[n, :])

                # Se determina la temperatura de burbuja de cada plato
                # TODO: A partir de la segunda iteración se deberia utilizar la temperatura
                # Calculada enteriormente
                try:
                    temp_burbuja = self.propiedades.temperatura_burbuja(composicion_liquido=x,
                                                                        presion=P)
                except RuntimeError as e:
                    print(contador_T)
                    print(contador_V)
                    raise e

                # Calculo de error para determinar paro de iteracion de ciclo interno
                errorT = np.sum((temp_burbuja - T) ** 2)
                T = temp_burbuja

                contador_T += 1
                if contador_T >= 200:
                    raise RuntimeError('Contador de ciclo de temperatura over 200')

            # Calculo de composicion de gas
            y = K * x

            # Calculo de flujo de liquido en la torre
            L = np.append(V, 0)[1:] + sum_materia - D
            print("L", L)
            print("V", V)

            # Calculo de entalpias de la alimentacion y plato a plato
            hV = self.propiedades.entalpia_vapor(composicion=y,
                                                 temperatura=T)
            hL = self.propiedades.entalpia_liquido(composicion=x,
                                                   temperatura=T)
            # Calculo de calor en condensador y rehervidor
            Q[0] = -(D * hV[0] - L[0] * hL[0] + V[1] * hV[1])  # Calor condensador

            # Calor rehervidor
            Q[-1] = -Q[0] + D * hV[0] + L[-1] * hL[-1] - np.sum(F * hF - SV * hV - SL * hL)

            # Calculo del flujo de vapor en la torre
            for n in range(N - 1, 0, -1):
                if n == N - 1:
                    V_nuevo[n] = ((L[n - 1] * hL[n - 1] - (L[n] + SL[n]) * hL[n] + F[n] * hF[n]
                                   + Q[n]) / hV[n] - SV[n])
                else:
                    V_nuevo[n] = ((L[n - 1] * hL[n - 1] - (L[n] + SL[n]) * hL[n] +
                                   V[n + 1] * hV[n + 1] + F[n] * hF[n] + Q[n]) / hV[n] - SV[n])

            # Criterio de error en el flujo de vapor
            if condensador_parcial:
                errorV = np.sum((V_nuevo[2:] - V[2:]) ** 2)
                V[2:] = V_nuevo[2:]

            else:
                errorV = np.sum((V_nuevo[1:] - V[1:]) ** 2)
                V[1:] = V_nuevo[1:]

            print(errorV)
            # Reseteando el error en la temperatura
            errorT = 100
            contador_V += 1
            contador_T = 0
            if contador_V >= 100:
                raise RuntimeError('Contador de ciclo de vapor over 200')

        return {
            'vapor': V,
            'liquido': L,
            'temperatura': T,
            'fraccion_liquido': x,
            'fraccion_vapor': y,
            'contador_ciclo_vapor': contador_V,
        }