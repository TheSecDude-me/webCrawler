# Form implementation generated from reading ui file 'ui\JustOneTimeCrawlUIRegexPattern.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(602, 245)
        font = QtGui.QFont()
        font.setFamily("Arial")
        Form.setFont(font)
        self.patterns_tableWidget = QtWidgets.QTableWidget(parent=Form)
        self.patterns_tableWidget.setGeometry(QtCore.QRect(10, 10, 581, 192))
        self.patterns_tableWidget.setObjectName("patterns_tableWidget")
        self.patterns_tableWidget.setColumnCount(2)
        self.patterns_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.patterns_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.patterns_tableWidget.setHorizontalHeaderItem(1, item)
        self.patterns_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.patterns_tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.add_pushButton = QtWidgets.QPushButton(parent=Form)
        self.add_pushButton.setGeometry(QtCore.QRect(100, 210, 75, 23))
        self.add_pushButton.setObjectName("add_pushButton")
        self.remove_pushButton = QtWidgets.QPushButton(parent=Form)
        self.remove_pushButton.setGeometry(QtCore.QRect(10, 210, 75, 23))
        self.remove_pushButton.setObjectName("remove_pushButton")
        self.save_pushButton = QtWidgets.QPushButton(parent=Form)
        self.save_pushButton.setGeometry(QtCore.QRect(510, 210, 75, 23))
        self.save_pushButton.setObjectName("save_pushButton")
        self.cancel_pushButton = QtWidgets.QPushButton(parent=Form)
        self.cancel_pushButton.setGeometry(QtCore.QRect(430, 210, 75, 23))
        self.cancel_pushButton.setObjectName("cancel_pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Just one time crawl regex patterns"))
        item = self.patterns_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Regex"))
        item = self.patterns_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Example"))
        self.add_pushButton.setText(_translate("Form", "New"))
        self.remove_pushButton.setText(_translate("Form", "Remove"))
        self.save_pushButton.setText(_translate("Form", "Save"))
        self.cancel_pushButton.setText(_translate("Form", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())