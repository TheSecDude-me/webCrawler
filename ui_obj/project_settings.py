from ui.project_settings import Ui_Form as project_settings
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QMessageBox
from gui_helpers import delete_folder, help_messages
import sys
import json
from urllib.parse import urlparse
import re

class ProjectSettingsWindow(QtWidgets.QMainWindow, project_settings):

    def __init__(self, *args, obj=None, **kwargs):
        super(ProjectSettingsWindow, self).__init__(*args, **kwargs)
        
        self.setupUi(self)
        self.project_name = "divar"

        with open("projects/" + self.project_name + "/settings.json", "r") as f_:
            self.settings = json.loads(f_.read())
        
        self.url_lineEdit.setText(self.settings['url'])
        
        self.origins_compare_radioButton.clicked.connect(self.compare_origins)
        self.origins_compare_ratio_horizontalSlider.valueChanged.connect(self.origins_compare_ratio)
        self.origins_contain_radioButton.clicked.connect(self.origins_contain)
        self.next_pushButton.clicked.connect(self.next)
        self.cancel_pushButton.clicked.connect(self.cancel)
        # Timing settings
        self.random_reqs_delay_checkBox.clicked.connect(self.random_reqs_delay)

        # Strech columns in tables
        self.patterns_tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.patterns_tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.bad_links_tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.links_xpath_tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.links_xpath_tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.schemes_tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tags_tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.files_tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Help buttons
        self.origins_compare_ratio_help_label.mousePressEvent = lambda x: self.help(self, obj=self.origins_compare_ratio_help_label.objectName())
        self.origins_contain_help_label.mousePressEvent = lambda x: self.help(self, obj=self.origins_contain_help_label.objectName())
        self.regex_pattern_help_label.mousePressEvent = lambda x: self.help(self, obj=self.regex_pattern_help_label.objectName())
        self.tags_help_label.mousePressEvent = lambda x: self.help(self, obj=self.tags_help_label.objectName())
        self.files_help_label.mousePressEvent = lambda x: self.help(self, obj=self.files_help_label.objectName())
        self.schemes_help_label.mousePressEvent = lambda x: self.help(self, obj=self.schemes_help_label.objectName())
        self.bad_links_help_label.mousePressEvent = lambda x: self.help(self, obj=self.bad_links_help_label.objectName())
        self.links_xpath_help_label.mousePressEvent = lambda x: self.help(self, obj=self.links_xpath_help_label.objectName())
        

        # Tables add button
        self.add_bad_link_pushButton.mousePressEvent = lambda x: self.add(self, table=self.bad_links_tableWidget)
        self.add_link_xpath_pushButton.mousePressEvent = lambda x: self.add(self, table=self.links_xpath_tableWidget)
        self.add_scheme_pushButton.mousePressEvent = lambda x: self.add(self, table=self.schemes_tableWidget)
        self.add_tag_pushButton.mousePressEvent = lambda x: self.add(self, table=self.tags_tableWidget)
        self.add_file_pushButton.mousePressEvent = lambda x: self.add(self, table=self.files_tableWidget)
        self.add_pattern_pushButton.mousePressEvent = lambda x: self.add(self, table=self.patterns_tableWidget)
        # Tables remove button
        self.remove_bad_link_pushButton.mousePressEvent = lambda x: self.remove(self, table=self.bad_links_tableWidget)
        self.remove_link_xpath_pushButton.mousePressEvent = lambda x: self.remove(self, table=self.links_xpath_tableWidget)
        self.remove_scheme_pushButton.mousePressEvent = lambda x: self.remove(self, table=self.schemes_tableWidget)
        self.remove_tag_pushButton.mousePressEvent = lambda x: self.remove(self, table=self.tags_tableWidget)
        self.remove_file_pushButton.mousePressEvent = lambda x: self.remove(self, table=self.files_tableWidget)
        self.remove_pattern_pushButton.mousePressEvent = lambda x: self.remove(self, table=self.patterns_tableWidget)

        # Init tables
        self.init()


    def init(self):
        # Set init values
        self.reqs_timeout_spinBox.setValue(int(self.settings['reqs_timeout']))
        self.req_delay_lineEdit.setText(str(self.settings["reqs_delay"]))
        self.rnd_req_delay_from_lineEdit.setText(str(self.settings['random_reqs_delay_from']))
        self.rnd_req_delay_to_lineEdit.setText(str(self.settings['random_reqs_delay_to']))
        self.origins_compare_ratio_horizontalSlider.setValue(int(self.settings['origin_compare_ratio'] * 10))
        self.origins_contain_lineEdit.setText(",".join(self.settings['origin_contains_list']))
        self.proxy_address_lineEdit.setText(self.settings["proxy"]['address'])
        self.proxy_port_lineEdit.setText(str(self.settings["proxy"]['port']))

        # Set init checked 
        self.random_reqs_delay_checkBox.setChecked(self.settings['random_reqs_delay'])

        # Set init disability
        if self.settings['random_reqs_delay']:
            self.rnd_req_delay_from_lineEdit.setDisabled(False)
            self.rnd_req_delay_to_lineEdit.setDisabled(False)
            self.req_delay_lineEdit.setDisabled(True)
        else:
            self.rnd_req_delay_from_lineEdit.setDisabled(True)
            self.rnd_req_delay_to_lineEdit.setDisabled(True)
            self.req_delay_lineEdit.setDisabled(False)
        
        if self.settings['origin_compare']:
            self.origins_compare_radioButton.setChecked(True)
            self.origins_compare_ratio_horizontalSlider.setDisabled(False)
            self.origins_compare_ratio_label.setDisabled(False)
            self.origins_compare_ratio_help_label.setDisabled(False)

            self.origins_contain_lineEdit.setDisabled(True)
            self.origins_contain_help_label.setDisabled(True)
        else:
            self.origins_contain_radioButton.setChecked(True)
            self.origins_compare_ratio_horizontalSlider.setDisabled(True)
            self.origins_compare_ratio_label.setDisabled(True)
            self.origins_compare_ratio_help_label.setDisabled(True)

            self.origins_contain_lineEdit.setDisabled(False)
            self.origins_contain_help_label.setDisabled(False)

        # Table init 
        self.init_tables(tableWidget=self.bad_links_tableWidget, values=self.settings['bad_links'])
        self.init_tables(tableWidget=self.schemes_tableWidget, values=self.settings['schemes'])
        self.init_tables(tableWidget=self.files_tableWidget, values=self.settings['files'])
        self.init_tables(tableWidget=self.tags_tableWidget, values=self.settings['search_for_tags'])
        self.init_tables(tableWidget=self.links_xpath_tableWidget, values=self.settings['link_xpaths'], keys=["xpath", "attr"])
        self.init_tables(tableWidget=self.patterns_tableWidget, values=self.settings['url_regex_patterns'], keys=['pattern', 'example'])
    def init_tables(self, tableWidget, values, keys=[]):
        row = 0
        for t in values:
            if tableWidget.columnCount() <= 1:
                tableWidget.insertRow(tableWidget.rowCount())
                tableWidget.setItem(row , 0, QtWidgets.QTableWidgetItem(t))
            else:
                col = 0
                tableWidget.insertRow(tableWidget.rowCount())
                for key in keys:
                    tableWidget.setItem(row , col, QtWidgets.QTableWidgetItem(t[key]))
                    col += 1
            row += 1


    # Timing Settings:
    def random_reqs_delay(self):
        if self.random_reqs_delay_checkBox.isChecked():
            self.req_delay_lineEdit.setDisabled(True)
            self.rnd_req_delay_from_lineEdit.setDisabled(False)
            self.rnd_req_delay_to_lineEdit.setDisabled(False)

        else:
            self.req_delay_lineEdit.setDisabled(False)
            self.rnd_req_delay_from_lineEdit.setDisabled(True)
            self.rnd_req_delay_to_lineEdit.setDisabled(True)

    def help(self, event, obj):
        QMessageBox.information(self, help_messages[obj]['title'], help_messages[obj]['message'])

    # Table actions
    def add(self, event, table):
        table.insertRow(table.rowCount())
    def remove(self, event, table):
        table.removeRow(table.currentRow())

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

    def getTableItems(self, tableWidget):
        records = []
        if tableWidget.rowCount() != 0: # Check for not beign empty
            row = 0
            while row < tableWidget.rowCount(): # Remove empty rows
                if tableWidget.item(row, 0) == None:
                    tableWidget.removeRow(row)
                    row += 1
                    continue

                records.append(tableWidget.item(row, 0).text())
                row += 1
        return records
    
    def next(self):
        if self.url_lineEdit.text() == "":
            QMessageBox.critical(self, "Error", "Please Enter URL correctly .")
            return
        if self.url_lineEdit.text().startswith("http") == False:
            QMessageBox.critical(self, "Error", "URL must start with http:// or https:// .")
            return
        
        try:
            self.settings['reqs_delay'] = float(self.req_delay_lineEdit.text())
            self.settings['random_reqs_delay'] = self.random_reqs_delay_checkBox.isChecked()
            self.settings["random_reqs_delay_from"] = int(self.rnd_req_delay_from_lineEdit.text())
            self.settings["random_reqs_delay_to"] = int(self.rnd_req_delay_to_lineEdit.text())
        except:
            QMessageBox.critical(self, "Error", "Request delay should be a number .")
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

        # # Regex patterns
        if self.patterns_tableWidget.rowCount() != 0:
            row = 0
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
                self.settings["url_regex_patterns"] = patterns
            else:
                QMessageBox.critical(self, "Error", "Patterns are not match with examples .")
                return
                
        
        self.settings['bad_links'] = self.getTableItems(self.bad_links_tableWidget)
        self.settings['schemes'] = self.getTableItems(self.schemes_tableWidget)
        self.settings['search_for_tags'] = self.getTableItems(self.tags_tableWidget)
        self.settings['files'] = self.getTableItems(self.files_tableWidget)

        self.settings['proxy']['address'] = self.proxy_address_lineEdit.text()
        try:
            self.settings['proxy']['port'] = int(self.proxy_port_lineEdit.text())
        except:
            QMessageBox.critical(self, "Error", "Proxy port should be a number .")
            return
        print(self.settings)

        with open("projects/" + self.project_name + "/settings.json", "w") as f_:
            f_.write(json.dumps(self.settings))
        # self.close()
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