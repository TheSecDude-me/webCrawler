from ui.project_settings import Ui_Form as project_settings
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QMessageBox
from gui_helpers import delete_folder
import sys
import json
from urllib.parse import urlparse
import re

class ProjectSettingsWindow(QtWidgets.QMainWindow, project_settings):

    def __init__(self, *args, obj=None, **kwargs):
        super(ProjectSettingsWindow, self).__init__(*args, **kwargs)
        
        self.setupUi(self)
        self.project_name = "salam"

        self.settings = {
            "url": self.url_lineEdit.text(),
            "reqs_timeout": int(self.reqs_timeout_spinBox.text()),

            "origin_compare": False,
            "origin_compare_ratio": float(self.origins_compare_ratio_label.text()),

            "origin_contains": False,
            "origin_contains_list": []
        }
        print(self.settings)
        self.url_lineEdit
        self.reqs_timeout_spinBox
        
        self.origins_compare_radioButton.clicked.connect(self.compare_origins)
        self.origins_compare_ratio_horizontalSlider.setDisabled(False)
        self.origins_compare_ratio_horizontalSlider.valueChanged.connect(self.origins_compare_ratio)
        self.origins_compare_ratio_label.setDisabled(False)
        self.origins_compare_ratio_help_label.setDisabled(False)

        self.origins_contain_radioButton.clicked.connect(self.origins_contain)
        self.origins_contain_help_label.setDisabled(True)
        self.origins_contain_lineEdit.setDisabled(True)

        self.next_pushButton.clicked.connect(self.next)
        self.cancel_pushButton.clicked.connect(self.cancel)


        # Help buttons
        self.origins_compare_ratio_help_label.mousePressEvent = self.origins_compare_ratio_help
        self.origins_contain_help_label.mousePressEvent = self.origins_contain_help
        self.regex_pattern_help_label.mousePressEvent = self.regex_pattern_help

        # Regex patterns
        self.patterns_tableWidget
        self.add_pattern_pushButton
        self.remove_pattern_pushButton
        self.regex_pattern_help_label
        header = self.patterns_tableWidget.horizontalHeader()  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        with open("projects/" + self.project_name + "/url_regex_patterns.json", "r") as f_:
            try:
                self.patterns = json.loads(f_.read())
            except:
                self.patterns = []
        row = 0
        for pattern in self.patterns:
            self.patterns_tableWidget.insertRow(self.patterns_tableWidget.rowCount())
            self.patterns_tableWidget.setItem(row , 0, QtWidgets.QTableWidgetItem(pattern['pattern']))
            self.patterns_tableWidget.setItem(row , 1, QtWidgets.QTableWidgetItem(pattern['example']))
            row += 1
        self.add_pattern_pushButton.clicked.connect(self.add_pattern)
        self.remove_pattern_pushButton.clicked.connect(self.remove_pattern)

    def regex_pattern_help(self, event):
        QMessageBox.information(self, "Regex Patterns", """
Why you need to set some regex pattern for better crawling ?
Imagine you target is a shop website . It has a lot of products by shop.com/products/[product_id] URL . 
All of products pages have same structure and you do not need to check all of them and checking all of them is wasting time and resources .
You can set some regex pattern for some specific URLs like shop.com/products/[product_id] to check one of them not any more . 
Regex pattern and it's example should be matched and if they are not matched you will receive some errors .
            """)


    def origins_contain_help(self, event):
        QMessageBox.information(self, "Origin Contain Settings", """
What is origin contain settings ?
Of course you  do not want to check all URLs with any origin, so you should set some settings to crawl just some specific ones with certain origin . 
Origin contain settings will allow you to set some spicific words, Crawler will cralw URLs with an origin that contains at least one of these words .
For example, If you set site,blog,news, Cralwer will crawl site.com, news.com, blog,com, news.site.com, ... but it won't cralw airport.com
            """)

    def origins_compare_ratio_help(self, event):
        QMessageBox.information(self, "Origin Compare Ratio", """
What is origin compare ratio settings ?
Of course you  do not want to check all URLs with any origin, so you should set some settings to crawl just some specific ones with certain origin . 
Compare Ratio will compare origin of an URL with allowed origins, If it was similare to them cralwer will crawl it too .
So you need to set sensitivity of the comparison with the slider element .
            """)

    # Regex 
    def add_pattern(self):
        self.patterns_tableWidget.insertRow(self.patterns_tableWidget.rowCount())
    def remove_pattern(self):
        self.patterns_tableWidget.removeRow(self.patterns_tableWidget.currentRow())


    def compare_origins(self):
        self.origins_contain_help_label.setDisabled(True)
        self.origins_contain_lineEdit.setDisabled(True)
        self.origins_compare_ratio_horizontalSlider.setDisabled(False)
        self.origins_compare_ratio_label.setDisabled(False)
        self.origins_compare_ratio_help_label.setDisabled(False)

    def origins_compare_ratio(self):
        value = self.origins_compare_ratio_horizontalSlider.value() / 10
        self.origins_compare_ratio_label.setText(str(value))



    def origins_contain(self):
        self.origins_compare_ratio_horizontalSlider.setDisabled(True)
        self.origins_compare_ratio_label.setDisabled(True)
        self.origins_compare_ratio_help_label.setDisabled(True)
        self.origins_contain_help_label.setDisabled(False)
        self.origins_contain_lineEdit.setDisabled(False)


    def next(self):
        if self.url_lineEdit.text() == "":
            QMessageBox.critical(self, "Error", "Please Enter URL correctly .")
            return
        if self.url_lineEdit.text().startswith("http") == False:
            QMessageBox.critical(self, "Error", "URL must start with http:// or https:// .")
            return
            
        if self.url_lineEdit.text().endswith("/") == False:
            self.url_lineEdit.setText(self.url_lineEdit.text() + "/")
        
        self.settings['url'] = self.url_lineEdit.text()
        self.settings['reqs_timeout'] = int(self.reqs_timeout_spinBox.text())

        if self.origins_compare_radioButton.isChecked():
            self.settings["origin_compare"] = self.origins_compare_radioButton.isChecked()
            self.settings["origin_compare_ratio"] = float(self.origins_compare_ratio_label.text())
            self.settings["origin_contains"] = self.origins_contain_radioButton.isChecked()
            self.settings["origin_contains_list"] = []
        if self.origins_contain_radioButton.isChecked():
            if self.origins_contain_lineEdit.text() == "":
                QMessageBox.critical(self, "Error", "Please enter correct value in origins contain text box .")
                return
            self.settings["origin_compare"] = self.origins_compare_radioButton.isChecked()
            self.settings["origin_compare_ratio"] = 0.0
            self.settings["origin_contains"] = self.origins_contain_radioButton.isChecked()
            self.settings["origin_contains_list"] = [y.replace(" ", "") for y in self.origins_contain_lineEdit.text().split(",") if y != ""]

        with open("projects/" + self.project_name + "/settings.json", "w") as f_:
            f_.write(json.dumps(self.settings))

        with open("projects/" + self.project_name + "/origins_conf.json", "r") as f_:
            origins_conf = json.loads(f_.read())
            origins_conf["allowed"].append(urlparse(self.settings['url']).scheme + "://" + urlparse(self.settings['url']).netloc + "/")
            with open("./projects/" + self.project_name + "/origins_conf.json", "w") as f_:
                    f_.write(json.dumps(origins_conf))  

        # Regex patterns
        if self.patterns_tableWidget.rowCount() != 0:
            row = 0
            with open("projects/" + self.project_name + "/url_regex_patterns.json", "w") as f_:
                patterns = []
                wrong_patterns = []
                while row < self.patterns_tableWidget.rowCount():
                    if self.patterns_tableWidget.item(row, 0) == None or self.patterns_tableWidget.item(row, 1) == None:
                        self.patterns_tableWidget.removeRow(row)
                        row += 1
                        continue


                    pattern = self.patterns_tableWidget.item(row, 0).text()
                    example = self.patterns_tableWidget.item(row, 1).text()
                    
                    if bool(re.match(pattern, example)) == False:
                        self.patterns_tableWidget.item(row, 0).setBackground(QtGui.QColor('red'))
                        self.patterns_tableWidget.item(row, 1).setBackground(QtGui.QColor('red'))
                        wrong_patterns.append(row)
                    else:
                        self.patterns_tableWidget.item(row, 0).setBackground(QtGui.QColor('transparent'))
                        self.patterns_tableWidget.item(row, 1).setBackground(QtGui.QColor('transparent'))
                    patterns.append({
                        "pattern": self.patterns_tableWidget.item(row, 0).text(),
                        "example": self.patterns_tableWidget.item(row, 1).text()
                    })
                    row += 1
                if len(wrong_patterns) == 0:
                    f_.write(json.dumps(patterns))
                else:
                    QMessageBox.critical(self, "Error", "Patterns are not match with examples .")
                    return
        self.close()
        # Show next window   


    def cancel(self):
        try:
            reply = QMessageBox.question(self, 'Cancel', 'Are you sure you want to cancel it ?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            
            if(reply == QMessageBox.StandardButton.Yes):
                delete_folder("projects/" + self.project_name) 
                self.close()       
        except:
            return

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ProjectSettingsWindow()
    window.show()
    app.exec()