# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HowToForm.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
from raven import Client
client = Client('https://164afd8685654ca2a89b153dbe963b0f:c79397a4affc4e9c8533cb88a0e17b46@sentry.io/116042')

class Ui_HowTo(object):
    def setupUi(self, HowTo):
        HowTo.setObjectName("HowTo")
        HowTo.resize(800, 460)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resourses/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        HowTo.setWindowIcon(icon)
        self.graphicsView = QtWidgets.QGraphicsView(HowTo)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 460, 276))
        self.graphicsView.setObjectName("graphicsView")
        self.textBrowser = QtWidgets.QTextBrowser(HowTo)
        self.textBrowser.setGeometry(QtCore.QRect(480, 10, 311, 441))
        self.textBrowser.setObjectName("textBrowser")
        self.graphicsView_2 = QtWidgets.QGraphicsView(HowTo)
        self.graphicsView_2.setGeometry(QtCore.QRect(10, 290, 260, 161))
        self.graphicsView_2.setAutoFillBackground(False)
        self.graphicsView_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.graphicsView_2.setCacheMode(QtWidgets.QGraphicsView.CacheNone)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.textBrowser_2 = QtWidgets.QTextBrowser(HowTo)
        self.textBrowser_2.setGeometry(QtCore.QRect(280, 290, 191, 161))
        self.textBrowser_2.setObjectName("textBrowser_2")

        self.retranslateUi(HowTo)
        QtCore.QMetaObject.connectSlotsByName(HowTo)

    def retranslateUi(self, HowTo):
        _translate = QtCore.QCoreApplication.translate
        HowTo.setWindowTitle(_translate("HowTo", "Dialog"))
        self.textBrowser.setHtml(_translate("HowTo", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. Menu bar is used for same actions like the main window + showing some extra information.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. Preview windows: at the left it shows you the original image or first video frame whereas at the right - preview of denoised one (if it\'s ready, of course).</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. Those two panels gives you information about estimated denoising time (in minutes) and memory use (in gigabytes) that you\'ll need for denoising.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4. Here you can change color flag if you need it. Denoising of grayscale image supposed to take less time and resourses.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5. Progress bar shows you progress of denoising (for video) or, at least, gives you information that it\'s complete.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">6. &quot;Denoise it!&quot; is the magic button that\'ll do all the work if you define file path.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">7. By these sliders you can define filter strenght for different noise. Of course, if you set color flag to grayslace, filter color strenght is just a game, enjoy :) Also remind that higher filter strengh means not only better denoising but fewer detailes remained also. So optimal settings are written beneath so you can return filter strenght to it\'s defaults easilly.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">8. Here you can define the resolution of output file if you want to change it. Please remind that higher resolution means moch more resourses to denoise it.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">9. And by this panel you can define file path manually or using standart system view, as you wish.</p></body></html>"))
        self.textBrowser_2.setHtml(_translate("HowTo", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">It\'s graph showing denoising time (in minutes) dependency on resolution (in megapixels).</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Used formula is 8.31088e^(1.73277×MP). It\'s the result of several aproximations.</p></body></html>"))


def init():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HowTo = QtWidgets.QDialog()
    ui = Ui_HowTo()
    ui.setupUi(HowTo)
    HowTo.show()
    app.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HowTo = QtWidgets.QDialog()
    ui = Ui_HowTo()
    ui.setupUi(HowTo)
    HowTo.show()
    sys.exit(app.exec_())

