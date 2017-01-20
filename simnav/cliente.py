from simnav.corrientes import Compuesto, CorrienteMateria
from simnav.termodinamica.paquetes import PaqueteIdeal
from simnav.opus.destilacion import DestilacionSemiRigurosa


compuestos = (Compuesto('benzene'),
              Compuesto('toluene'))
paquete_termodinamico = PaqueteIdeal(compuestos)
composicion = [0.45, 0.55]
corriente = CorrienteMateria(flujo=100,
                             temperatura=54.4+273.15,
                             paquete_termodinamico=paquete_termodinamico,
                             compuestos=compuestos,
                             composicion=composicion)
entradas = [
    (corriente, 5)
]

destilador = DestilacionSemiRigurosa(numero_platos=10,
                                     destilado=55,
                                     reflujo=1.3,
                                     corrientes_entrada=entradas,
                                     corrientes_salida='foo',
                                     paquete_termodinamico=paquete_termodinamico)
destilador.calcular()