# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Developer-old/Qt/TextEditor/mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(452, 383)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.search_term = QtGui.QLineEdit(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_term.sizePolicy().hasHeightForWidth())
        self.search_term.setSizePolicy(sizePolicy)
        self.search_term.setObjectName(_fromUtf8("search_term"))
        self.gridLayout.addWidget(self.search_term, 0, 0, 1, 1)
        self.run_search = QtGui.QPushButton(self.centralWidget)
        self.run_search.setDefault(True)
        self.run_search.setObjectName(_fromUtf8("run_search"))
        self.gridLayout.addWidget(self.run_search, 0, 1, 1, 1)
        self.search_results = QtGui.QPlainTextEdit(self.centralWidget)
        self.search_results.setObjectName(_fromUtf8("search_results"))
        self.gridLayout.addWidget(self.search_results, 1, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 452, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.search_term.returnPressed.connect(self.run_search.click)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.search_term.setPlaceholderText(_translate("MainWindow", "Insert name of an article you\'ve cited", None))
        self.run_search.setText(_translate("MainWindow", "Run", None))

