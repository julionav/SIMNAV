# -*- coding: utf-8 -*-

import numpy as np

'''
Created on 06/11/2016

@author: Julio Navarro
'''

class CorrienteMateria:
    '''
    Corriente de flujo masico. 
    '''
    def __init__(self, nombre, flujo, temperatura, presion, paquete_termodinamico, componentes):
        self.nombre = nombre
        self.flujo = flujo
        self.temperatura = temperatura
        self.presion = presion
        self.paquete_termodinamico = paquete_termodinamico
        self.componentes = np.array(componentes) # Al inicio de la simulacion los componentes son elegidos y se les asigna una posicion en el array de componentes
        self.normalizar()
        self.calcular()
        

    def dibujar(self):
        pass

    def calcular(self):
        '''
        Calcula el equilibrio entre los componentes a las condiciones dadas
        '''
        # Hace algo con el paquete termodinamico
        
    def normalizar(self):
        '''normaliza la composicion de la corriente'''
        self.componentes = self.componentes/np.sum(self.componentes)


class CorrienteEnergia:
    pass