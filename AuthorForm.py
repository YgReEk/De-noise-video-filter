# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AuthorForm.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
from raven import Client
client = Client('https://164afd8685654ca2a89b153dbe963b0f:c79397a4affc4e9c8533cb88a0e17b46@sentry.io/116042')

class Ui_Author(object):
    def setupUi(self, Author):
        Author.setObjectName("Author")
        Author.resize(256, 128)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resourses/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Author.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(Author)
        self.label.setGeometry(QtCore.QRect(10, 9, 211, 31))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Author)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 201, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Author)
        self.label_3.setGeometry(QtCore.QRect(20, 60, 201, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Author)
        self.label_4.setGeometry(QtCore.QRect(20, 80, 201, 21))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Author)
        QtCore.QMetaObject.connectSlotsByName(Author)

    def retranslateUi(self, Author):
        _translate = QtCore.QCoreApplication.translate
        Author.setWindowTitle(_translate("Author", "Dialog"))
        self.label.setText(_translate("Author", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Nemikhin Igor</span></p></body></html>"))
        self.label_2.setText(_translate("Author", "<html><head/><body><p><span style=\" font-size:10pt;\">GitHub: https://github.com/YgReEk</span></p></body></html>"))
        self.label_3.setText(_translate("Author", "<html><head/><body><p><span style=\" font-size:10pt;\">E-mail: nemikhin@outlook.com</span></p></body></html>"))
        self.label_4.setText(_translate("Author", "<html><head/><body><p><span style=\" font-size:10pt;\">VK: vk.com/nemihin</span></p></body></html>"))



def init():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Author = QtWidgets.QDialog()
    ui = Ui_Author()
    ui.setupUi(Author)
    Author.show()
    app.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Author = QtWidgets.QDialog()
    ui = Ui_Author()
    ui.setupUi(Author)
    Author.show()
    sys.exit(app.exec_())

