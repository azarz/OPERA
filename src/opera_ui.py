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
        OperaDialogBase.resize(584, 688)
        self.button_box = QtGui.QDialogButtonBox(OperaDialogBase)
        self.button_box.setGeometry(QtCore.QRect(220, 630, 341, 32))
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
        self.radio_MRD.setChecked(True)
        self.radio_MRD.setObjectName(_fromUtf8("radio_MRD"))
        self.radio_niveau.addButton(self.radio_MRD)
        self.radio_MRP = QtGui.QRadioButton(OperaDialogBase)
        self.radio_MRP.setGeometry(QtCore.QRect(380, 200, 116, 22))
        self.radio_MRP.setObjectName(_fromUtf8("radio_MRP"))
        self.radio_niveau.addButton(self.radio_MRP)
        self.checkBox = QtGui.QCheckBox(OperaDialogBase)
        self.checkBox.setGeometry(QtCore.QRect(160, 260, 271, 22))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.massifs = QtGui.QComboBox(OperaDialogBase)
        self.massifs.setGeometry(QtCore.QRect(380, 50, 131, 27))
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
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Opera/doc/logo.jpg")))
        self.label.setScaledContents(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(OperaDialogBase)
        self.label_2.setGeometry(QtCore.QRect(330, 130, 171, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(OperaDialogBase)
        self.label_3.setGeometry(QtCore.QRect(330, 30, 121, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(OperaDialogBase)
        self.label_4.setGeometry(QtCore.QRect(100, 380, 111, 111))
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Opera/mont.PNG")))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(OperaDialogBase)
        self.label_5.setGeometry(QtCore.QRect(320, 380, 161, 111))
        self.label_5.setText(_fromUtf8(""))
        self.label_5.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Opera/rose.png")))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.N = QtGui.QCheckBox(OperaDialogBase)
        self.N.setGeometry(QtCore.QRect(370, 360, 70, 17))
        self.N.setText(_fromUtf8(""))
        self.N.setObjectName(_fromUtf8("N"))
        self.NE = QtGui.QCheckBox(OperaDialogBase)
        self.NE.setGeometry(QtCore.QRect(420, 380, 70, 17))
        self.NE.setText(_fromUtf8(""))
        self.NE.setObjectName(_fromUtf8("NE"))
        self.E = QtGui.QCheckBox(OperaDialogBase)
        self.E.setGeometry(QtCore.QRect(430, 426, 70, 21))
        self.E.setText(_fromUtf8(""))
        self.E.setObjectName(_fromUtf8("E"))
        self.SE = QtGui.QCheckBox(OperaDialogBase)
        self.SE.setGeometry(QtCore.QRect(420, 470, 70, 17))
        self.SE.setText(_fromUtf8(""))
        self.SE.setObjectName(_fromUtf8("SE"))
        self.S = QtGui.QCheckBox(OperaDialogBase)
        self.S.setGeometry(QtCore.QRect(370, 490, 70, 17))
        self.S.setText(_fromUtf8(""))
        self.S.setObjectName(_fromUtf8("S"))
        self.SO = QtGui.QCheckBox(OperaDialogBase)
        self.SO.setGeometry(QtCore.QRect(320, 480, 70, 17))
        self.SO.setText(_fromUtf8(""))
        self.SO.setObjectName(_fromUtf8("SO"))
        self.O = QtGui.QCheckBox(OperaDialogBase)
        self.O.setGeometry(QtCore.QRect(300, 427, 70, 20))
        self.O.setText(_fromUtf8(""))
        self.O.setObjectName(_fromUtf8("O"))
        self.NO = QtGui.QCheckBox(OperaDialogBase)
        self.NO.setGeometry(QtCore.QRect(320, 380, 70, 17))
        self.NO.setText(_fromUtf8(""))
        self.NO.setObjectName(_fromUtf8("NO"))
        self.label_6 = QtGui.QLabel(OperaDialogBase)
        self.label_6.setGeometry(QtCore.QRect(30, 490, 251, 41))
        self.label_6.setTextFormat(QtCore.Qt.AutoText)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.riskHigh = QtGui.QComboBox(OperaDialogBase)
        self.riskHigh.setGeometry(QtCore.QRect(130, 420, 41, 20))
        self.riskHigh.setObjectName(_fromUtf8("riskHigh"))
        self.riskHigh.addItem(_fromUtf8(""))
        self.riskHigh.addItem(_fromUtf8(""))
        self.riskHigh.addItem(_fromUtf8(""))
        self.riskHigh.addItem(_fromUtf8(""))
        self.riskHigh.addItem(_fromUtf8(""))
        self.riskLow = QtGui.QComboBox(OperaDialogBase)
        self.riskLow.setGeometry(QtCore.QRect(130, 450, 41, 20))
        self.riskLow.setObjectName(_fromUtf8("riskLow"))
        self.riskLow.addItem(_fromUtf8(""))
        self.riskLow.addItem(_fromUtf8(""))
        self.riskLow.addItem(_fromUtf8(""))
        self.riskLow.addItem(_fromUtf8(""))
        self.riskLow.addItem(_fromUtf8(""))
        self.altiThresh = QtGui.QSpinBox(OperaDialogBase)
        self.altiThresh.setGeometry(QtCore.QRect(190, 430, 61, 22))
        self.altiThresh.setMaximum(9999)
        self.altiThresh.setObjectName(_fromUtf8("altiThresh"))
        self.chemin_chkbx = QtGui.QCheckBox(OperaDialogBase)
        self.chemin_chkbx.setGeometry(QtCore.QRect(60, 580, 181, 17))
        self.chemin_chkbx.setObjectName(_fromUtf8("chemin_chkbx"))
        self.couche_chemin = QtGui.QComboBox(OperaDialogBase)
        self.couche_chemin.setEnabled(True)
        self.couche_chemin.setGeometry(QtCore.QRect(70, 610, 101, 22))
        self.couche_chemin.setObjectName(_fromUtf8("couche_chemin"))
        self.label.raise_()
        self.button_box.raise_()
        self.radio_MRE.raise_()
        self.radio_MRD.raise_()
        self.radio_MRP.raise_()
        self.checkBox.raise_()
        self.massifs.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.N.raise_()
        self.NE.raise_()
        self.E.raise_()
        self.SE.raise_()
        self.S.raise_()
        self.SO.raise_()
        self.O.raise_()
        self.NO.raise_()
        self.label_6.raise_()
        self.riskHigh.raise_()
        self.riskLow.raise_()
        self.altiThresh.raise_()
        self.chemin_chkbx.raise_()
        self.couche_chemin.raise_()

        self.retranslateUi(OperaDialogBase)
        self.riskHigh.setCurrentIndex(0)
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
        self.massifs.setItemText(5, _translate("OperaDialogBase", "Embrunais-Parpaillon", None))
        self.label_2.setText(_translate("OperaDialogBase", "Niveau de réduction :", None))
        self.label_3.setText(_translate("OperaDialogBase", "Massif :", None))
        self.label_6.setText(_translate("OperaDialogBase", "Si évolution (flèche) prendre la valeur la plus haute", None))
        self.riskHigh.setItemText(0, _translate("OperaDialogBase", "1", None))
        self.riskHigh.setItemText(1, _translate("OperaDialogBase", "2", None))
        self.riskHigh.setItemText(2, _translate("OperaDialogBase", "3", None))
        self.riskHigh.setItemText(3, _translate("OperaDialogBase", "4", None))
        self.riskHigh.setItemText(4, _translate("OperaDialogBase", "5", None))
        self.riskLow.setItemText(0, _translate("OperaDialogBase", "1", None))
        self.riskLow.setItemText(1, _translate("OperaDialogBase", "2", None))
        self.riskLow.setItemText(2, _translate("OperaDialogBase", "3", None))
        self.riskLow.setItemText(3, _translate("OperaDialogBase", "4", None))
        self.riskLow.setItemText(4, _translate("OperaDialogBase", "5", None))
        self.chemin_chkbx.setText(_translate("OperaDialogBase", "Risque selon un chemin", None))

