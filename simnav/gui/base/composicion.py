# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simnav/gui/vistas/diseños/designer/composicion.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Composicion(object):
    def setupUi(self, Composicion):
        Composicion.setObjectName("Composicion")
        Composicion.resize(268, 336)
        Composicion.setMinimumSize(QtCore.QSize(234, 336))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Composicion)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Composicion)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tablaComposicion = QtWidgets.QTableWidget(Composicion)
        self.tablaComposicion.setObjectName("tablaComposicion")
        self.tablaComposicion.setColumnCount(2)
        self.tablaComposicion.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tablaComposicion.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablaComposicion.setHorizontalHeaderItem(1, item)
        self.tablaComposicion.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tablaComposicion)
        self.normalizar = QtWidgets.QPushButton(Composicion)
        self.normalizar.setObjectName("normalizar")
        self.verticalLayout.addWidget(self.normalizar)
        self.aceptar = QtWidgets.QPushButton(Composicion)
        self.aceptar.setObjectName("aceptar")
        self.verticalLayout.addWidget(self.aceptar)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Composicion)
        QtCore.QMetaObject.connectSlotsByName(Composicion)

    def retranslateUi(self, Composicion):
        _translate = QtCore.QCoreApplication.translate
        Composicion.setWindowTitle(_translate("Composicion", "Form"))
        self.label.setText(_translate("Composicion", "Composición (fracción molar)"))
        item = self.tablaComposicion.horizontalHeaderItem(0)
        item.setText(_translate("Composicion", "Compuesto"))
        item = self.tablaComposicion.horizontalHeaderItem(1)
        item.setText(_translate("Composicion", "Fracción molar"))
        self.normalizar.setText(_translate("Composicion", "Normalizar"))
        self.aceptar.setText(_translate("Composicion", "Aceptar"))

