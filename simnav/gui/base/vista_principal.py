# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/julio/Desktop/SIMNAV/simnav/gui/base/ui/vista_principal.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VistaPrincipal(object):
    def setupUi(self, VistaPrincipal):
        VistaPrincipal.setObjectName("VistaPrincipal")
        VistaPrincipal.resize(473, 615)
        VistaPrincipal.setMinimumSize(QtCore.QSize(473, 615))
        VistaPrincipal.setMaximumSize(QtCore.QSize(473, 615))
        self.centralwidget = QtWidgets.QWidget(VistaPrincipal)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.dibujoTorre = QtWidgets.QLabel(self.centralwidget)
        self.dibujoTorre.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.dibujoTorre.setFont(font)
        self.dibujoTorre.setAcceptDrops(True)
        self.dibujoTorre.setText("")
        self.dibujoTorre.setPixmap(QtGui.QPixmap("../../imagenes/torre_destilacion.svg"))
        self.dibujoTorre.setScaledContents(False)
        self.dibujoTorre.setAlignment(QtCore.Qt.AlignCenter)
        self.dibujoTorre.setObjectName("dibujoTorre")
        self.verticalLayout.addWidget(self.dibujoTorre)
        self.infoLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(12)
        self.infoLabel.setFont(font)
        self.infoLabel.setObjectName("infoLabel")
        self.verticalLayout.addWidget(self.infoLabel)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        VistaPrincipal.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(VistaPrincipal)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 473, 25))
        self.menubar.setObjectName("menubar")
        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")
        VistaPrincipal.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(VistaPrincipal)
        self.statusbar.setObjectName("statusbar")
        VistaPrincipal.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(VistaPrincipal)
        self.toolBar.setObjectName("toolBar")
        VistaPrincipal.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionCompuestos = QtWidgets.QAction(VistaPrincipal)
        self.actionCompuestos.setObjectName("actionCompuestos")
        self.actionPropiedades = QtWidgets.QAction(VistaPrincipal)
        self.actionPropiedades.setObjectName("actionPropiedades")
        self.actionCorrientes = QtWidgets.QAction(VistaPrincipal)
        self.actionCorrientes.setObjectName("actionCorrientes")
        self.actionSimular = QtWidgets.QAction(VistaPrincipal)
        self.actionSimular.setObjectName("actionSimular")
        self.actionAbrir = QtWidgets.QAction(VistaPrincipal)
        self.actionAbrir.setObjectName("actionAbrir")
        self.actionCerrar = QtWidgets.QAction(VistaPrincipal)
        self.actionCerrar.setObjectName("actionCerrar")
        self.actionSalir = QtWidgets.QAction(VistaPrincipal)
        self.actionSalir.setObjectName("actionSalir")
        self.actionDestilacion = QtWidgets.QAction(VistaPrincipal)
        self.actionDestilacion.setObjectName("actionDestilacion")
        self.menuArchivo.addAction(self.actionAbrir)
        self.menuArchivo.addAction(self.actionCerrar)
        self.menuArchivo.addAction(self.actionSalir)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.toolBar.addAction(self.actionCompuestos)
        self.toolBar.addAction(self.actionPropiedades)
        self.toolBar.addAction(self.actionCorrientes)
        self.toolBar.addAction(self.actionDestilacion)
        self.toolBar.addAction(self.actionSimular)

        self.retranslateUi(VistaPrincipal)
        QtCore.QMetaObject.connectSlotsByName(VistaPrincipal)

    def retranslateUi(self, VistaPrincipal):
        _translate = QtCore.QCoreApplication.translate
        VistaPrincipal.setWindowTitle(_translate("VistaPrincipal", "MainWindow"))
        self.infoLabel.setText(_translate("VistaPrincipal", "Información"))
        self.menuArchivo.setTitle(_translate("VistaPrincipal", "Archivo"))
        self.toolBar.setWindowTitle(_translate("VistaPrincipal", "toolBar"))
        self.actionCompuestos.setText(_translate("VistaPrincipal", "Compuestos"))
        self.actionPropiedades.setText(_translate("VistaPrincipal", "Propiedades"))
        self.actionCorrientes.setText(_translate("VistaPrincipal", "Corrientes"))
        self.actionSimular.setText(_translate("VistaPrincipal", "Resultados"))
        self.actionAbrir.setText(_translate("VistaPrincipal", "Abrir"))
        self.actionCerrar.setText(_translate("VistaPrincipal", "Guardar"))
        self.actionSalir.setText(_translate("VistaPrincipal", "Salir"))
        self.actionDestilacion.setText(_translate("VistaPrincipal", "Destilacion"))

