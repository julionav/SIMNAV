"""Utilidades para la interfaz de usuario grafica"""

import logging
from PyQt5 import QtGui


class LogToStdOut(logging.StreamHandler):
    """Envia el registro a la salida estandar"""
    def emit(self, record):
        print(self.format(record))


class StdOutToTextBox:
    """Redirecciona la salida extandar a una caja de texto"""
    def __init__(self, textbox):
        self.cursor = textbox.textCursor()

    def write(self, text):
        self.cursor.movePosition(QtGui.QTextCursor.End)
        self.cursor.insertText(text)
