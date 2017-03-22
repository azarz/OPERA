# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OPERA_dialog_base.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_OperaDialogBase(object):
    def setupUi(self, OperaDialogBase):
        OperaDialogBase.setObjectName(_fromUtf8("OperaDialogBase"))
        OperaDialogBase.resize(531, 390)
        self.button_box = QtGui.QDialogButtonBox(OperaDialogBase)
        self.button_box.setGeometry(QtCore.QRect(-10, 350, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.radio_MRE = QtGui.QRadioButton(OperaDialogBase)
        self.radio_MRE.setGeometry(QtCore.QRect(380, 180, 151, 22))
        self.radio_MRE.setObjectName(_fromUtf8("radio_MRE"))
        self.radio_niveau = QtGui.QButtonGroup(OperaDialogBase)
        self.radio_niveau.setObjectName(_fromUtf8("radio_niveau"))
        self.radio_niveau.addButton(self.radio_MRE)
        self.radio_MRD = QtGui.QRadioButton(OperaDialogBase)
        self.radio_MRD.setGeometry(QtCore.QRect(380, 160, 151, 22))
        self.radio_MRD.setObjectName(_fromUtf8("radio_MRD"))
        self.radio_niveau.addButton(self.radio_MRD)
        self.radio_MRP = QtGui.QRadioButton(OperaDialogBase)
        self.radio_MRP.setGeometry(QtCore.QRect(380, 200, 116, 22))
        self.radio_MRP.setObjectName(_fromUtf8("radio_MRP"))
        self.radio_niveau.addButton(self.radio_MRP)
        self.checkBox = QtGui.QCheckBox(OperaDialogBase)
        self.checkBox.setGeometry(QtCore.QRect(170, 290, 271, 22))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.massifs = QtGui.QComboBox(OperaDialogBase)
        self.massifs.setGeometry(QtCore.QRect(380, 50, 78, 27))
        self.massifs.setObjectName(_fromUtf8("massifs"))
        self.massifs.addItem(_fromUtf8(""))
        self.massifs.addItem(_fromUtf8(""))
        self.massifs.addItem(_fromUtf8(""))
        self.massifs.addItem(_fromUtf8(""))
        self.massifs.addItem(_fromUtf8(""))
        self.massifs.addItem(_fromUtf8(""))
        self.label = QtGui.QLabel(OperaDialogBase)
        self.label.setGeometry(QtCore.QRect(10, 10, 271, 191))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("/home/dpts/.qgis2/python/plugins/Opera/doc/logo.jpg")))
        self.label.setScaledContents(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(OperaDialogBase)
        self.label_2.setGeometry(QtCore.QRect(330, 130, 171, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(OperaDialogBase)
        self.label_3.setGeometry(QtCore.QRect(330, 30, 121, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label.raise_()
        self.button_box.raise_()
        self.radio_MRE.raise_()
        self.radio_MRD.raise_()
        self.radio_MRP.raise_()
        self.checkBox.raise_()
        self.massifs.raise_()
        self.label_2.raise_()
        self.label_3.raise_()

        self.retranslateUi(OperaDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), OperaDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), OperaDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(OperaDialogBase)

    def retranslateUi(self, OperaDialogBase):
        OperaDialogBase.setWindowTitle(_translate("OperaDialogBase", "Opera", None))
        self.radio_MRE.setText(_translate("OperaDialogBase", "MRE (elementaire)", None))
        self.radio_MRD.setText(_translate("OperaDialogBase", "MRD (debutant)", None))
        self.radio_MRP.setText(_translate("OperaDialogBase", "MRP (expert)", None))
        self.checkBox.setText(_translate("OperaDialogBase", "Chargement automatique du BRA", None))
        self.massifs.setItemText(0, _translate("OperaDialogBase", "Thabor", None))
        self.massifs.setItemText(1, _translate("OperaDialogBase", "Pelvoux", None))
        self.massifs.setItemText(2, _translate("OperaDialogBase", "Champsaur", None))
        self.massifs.setItemText(3, _translate("OperaDialogBase", "Devoluy", None))
        self.massifs.setItemText(4, _translate("OperaDialogBase", "Queyras", None))
        self.massifs.setItemText(5, _translate("OperaDialogBase", "Embrunais-Parapaillon", None))
        self.label_2.setText(_translate("OperaDialogBase", "Niveau de réduction :", None))
        self.label_3.setText(_translate("OperaDialogBase", "Massif :", None))

