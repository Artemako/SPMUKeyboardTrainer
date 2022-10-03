# Form implementation generated from reading ui file 'Wiki_1.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Wiki(object):
    def setupUi(self, Wiki):
        Wiki.setObjectName("Wiki")
        Wiki.resize(600, 460)
        Wiki.setMinimumSize(QtCore.QSize(0, 0))
        Wiki.setMaximumSize(QtCore.QSize(10000, 10000))
        self.wikifindbutton = QtWidgets.QPushButton(Wiki)
        self.wikifindbutton.setGeometry(QtCore.QRect(440, 150, 150, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wikifindbutton.sizePolicy().hasHeightForWidth())
        self.wikifindbutton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.wikifindbutton.setFont(font)
        self.wikifindbutton.setToolTip("")
        self.wikifindbutton.setStyleSheet("background-color: #7b8691;\n"
"color: rgb(255, 255, 255);")
        self.wikifindbutton.setAutoRepeat(False)
        self.wikifindbutton.setObjectName("wikifindbutton")
        self.wikisearchline = QtWidgets.QLineEdit(Wiki)
        self.wikisearchline.setGeometry(QtCore.QRect(10, 150, 420, 40))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.wikisearchline.setFont(font)
        self.wikisearchline.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 4px solid rgb(245, 121, 32);")
        self.wikisearchline.setObjectName("wikisearchline")
        self.wikilogo = QtWidgets.QLabel(Wiki)
        self.wikilogo.setGeometry(QtCore.QRect(0, 0, 600, 153))
        self.wikilogo.setText("")
        self.wikilogo.setPixmap(QtGui.QPixmap("pics/wiki_logo.png"))
        self.wikilogo.setScaledContents(True)
        self.wikilogo.setObjectName("wikilogo")
        self.result_title = QtWidgets.QLabel(Wiki)
        self.result_title.setGeometry(QtCore.QRect(10, 200, 330, 40))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.result_title.setFont(font)
        self.result_title.setObjectName("result_title")
        self.wikiluckybutton = QtWidgets.QPushButton(Wiki)
        self.wikiluckybutton.setGeometry(QtCore.QRect(440, 200, 150, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wikiluckybutton.sizePolicy().hasHeightForWidth())
        self.wikiluckybutton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.wikiluckybutton.setFont(font)
        self.wikiluckybutton.setToolTip("")
        self.wikiluckybutton.setStyleSheet("background-color: #7b8691;\n"
"color: rgb(255, 255, 255);")
        self.wikiluckybutton.setAutoRepeat(False)
        self.wikiluckybutton.setObjectName("wikiluckybutton")
        self.loadwikitextbutton = QtWidgets.QPushButton(Wiki)
        self.loadwikitextbutton.setGeometry(QtCore.QRect(10, 410, 580, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadwikitextbutton.sizePolicy().hasHeightForWidth())
        self.loadwikitextbutton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.loadwikitextbutton.setFont(font)
        self.loadwikitextbutton.setToolTip("")
        self.loadwikitextbutton.setStyleSheet("background-color: #7b8691;\n"
"color: rgb(255, 255, 255);")
        self.loadwikitextbutton.setAutoRepeat(False)
        self.loadwikitextbutton.setObjectName("loadwikitextbutton")
        self.wikitext = QtWidgets.QTextEdit(Wiki)
        self.wikitext.setGeometry(QtCore.QRect(10, 240, 580, 160))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self.wikitext.setFont(font)
        self.wikitext.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 4px solid #7b8691;")
        self.wikitext.setReadOnly(True)
        self.wikitext.setObjectName("wikitext")

        self.retranslateUi(Wiki)
        QtCore.QMetaObject.connectSlotsByName(Wiki)

    def retranslateUi(self, Wiki):
        _translate = QtCore.QCoreApplication.translate
        Wiki.setWindowTitle(_translate("Wiki", "Загрузка с Wikipedia"))
        self.wikifindbutton.setText(_translate("Wiki", "Найти"))
        self.wikisearchline.setPlaceholderText(_translate("Wiki", "Введите название статьи (на англ.)"))
        self.result_title.setText(_translate("Wiki", "Результат поиска:"))
        self.wikiluckybutton.setText(_translate("Wiki", "Мне повезет!"))
        self.loadwikitextbutton.setText(_translate("Wiki", "Загрузить текст"))
        self.wikitext.setHtml(_translate("Wiki", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))