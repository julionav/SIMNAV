"""Cliente de simnav. Encargado de proveer inicializar los modelos y las vistas"""

import sys
import logging
from pathlib import Path

from PyQt5 import QtWidgets

from simnav import Simulacion
from simnav.gui.vistas import VistaPrincipal

carpeta_actual = Path(__file__).parent

class Aplicacion(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        """Inicializa la simulacion y las vistas. Pasando la referencia de la
        simulacion a la vista principal"""
        super().__init__(sys_argv)

        # Logging
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        logger.info('Inciando Aplicación')

        self.simulacion = Simulacion(carpeta_actual / 'ejemplo.yaml')
        self.main_view = VistaPrincipal(self.simulacion)
        self.main_view.show()


if __name__ == '__main__':
    app = Aplicacion(sys.argv)
    sys.exit(app.exec_())