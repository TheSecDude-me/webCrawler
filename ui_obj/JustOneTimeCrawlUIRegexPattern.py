from ui.JustOneTimeCrawlUIRegexPattern import Ui_Form as JustOneTimeCrawlUIRegexPattern
from PyQt6 import QtWidgets
from PyQt6.QtCore import *
import sys
import json

class JustOneTimeCrawlUI(QtWidgets.QMainWindow, JustOneTimeCrawlUIRegexPattern):
    project_name = pyqtSignal(str)

    def __init__(self, *args, obj=None, **kwargs):
        super(JustOneTimeCrawlUI, self).__init__(*args, **kwargs)
        
        self.setupUi(self)

        with open("projects/" + self.project_name + "/just_one_no_more_patterns.txt", "r") as f_:
            try:
                self.patterns = json.loads(f_.read())
            except:
                self.patterns = []

        header = self.patterns_tableWidget.horizontalHeader()  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        row = 0
        for pattern in self.patterns:
            self.patterns_tableWidget.insertRow(self.patterns_tableWidget.rowCount())
            self.patterns_tableWidget.setItem(row , 0, QtWidgets.QTableWidgetItem(pattern['pattern']))
            self.patterns_tableWidget.setItem(row , 1, QtWidgets.QTableWidgetItem(pattern['example']))
            row += 1

        self.add_pushButton.clicked.connect(self.add)
        self.save_pushButton.clicked.connect(self.save)
        self.remove_pushButton.clicked.connect(self.remove)
        self.cancel_pushButton.clicked.connect(self.cancel)

    def add(self):
        self.patterns_tableWidget.insertRow(self.patterns_tableWidget.rowCount())
    def remove(self):
        self.patterns_tableWidget.removeRow(self.patterns_tableWidget.currentRow())
    def save(self):
        row = 0
        with open("projects/" + self.project_name + "/just_one_no_more_patterns.txt", "w") as f_:
            patterns = []
            while row < self.patterns_tableWidget.rowCount():
                if self.patterns_tableWidget.item(row, 0).text() == "" or self.patterns_tableWidget.item(row, 1).text() == "":
                    print("Pattern and Example are required .")
                    continue
                patterns.append({
                    "pattern": self.patterns_tableWidget.item(row, 0).text(),
                    "example": self.patterns_tableWidget.item(row, 1).text()
                })
                row += 1
            f_.write(json.dumps(patterns))
        self.close()
    def cancel(self):
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = JustOneTimeCrawlUI()
    window.show()
    app.exec()