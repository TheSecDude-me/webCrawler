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
        self.project_name = "test"

        with open("projects/" + self.project_name + "/settings.json", "r") as f_:
            self.settings = json.loads(f_.read())
        



        
        self.url_lineEdit.setText(self.settings['url'])
        
        self.origins_compare_radioButton.clicked.connect(self.compare_origins)
        self.origins_compare_ratio_horizontalSlider.setDisabled(self.settings['origin_compare'])
        self.origins_compare_ratio_horizontalSlider.valueChanged.connect(self.origins_compare_ratio)
        self.origins_compare_ratio_horizontalSlider.setValue(int(self.settings['origin_compare_ratio'] * 10))
        self.origins_compare_ratio_label.setDisabled(False)
        self.origins_compare_ratio_help_label.setDisabled(False)

        self.origins_contain_radioButton.clicked.connect(self.origins_contain)
        self.origins_contain_help_label.setDisabled(self.settings['origin_contains'])
        self.origins_contain_lineEdit.setDisabled(True)

        self.next_pushButton.clicked.connect(self.next)
        self.cancel_pushButton.clicked.connect(self.cancel)

        # Timing settings
        self.random_reqs_delay_checkBox.setChecked(self.settings['random_reqs_delay'])
        self.random_reqs_delay_checkBox.clicked.connect(self.random_reqs_delay)



        # Regex patterns
        header = self.patterns_tableWidget.horizontalHeader()  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        row = 0
        for pattern in self.settings['url_regex_patterns']:
            self.patterns_tableWidget.insertRow(self.patterns_tableWidget.rowCount())
            self.patterns_tableWidget.setItem(row , 0, QtWidgets.QTableWidgetItem(pattern['pattern']))
            self.patterns_tableWidget.setItem(row , 1, QtWidgets.QTableWidgetItem(pattern['example']))
            row += 1


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
        self.initTables()


    def initTables(self):
        row = 0
        for l in self.settings['bad_links']:
            self.bad_links_tableWidget.insertRow(self.bad_links_tableWidget.rowCount())
            self.bad_links_tableWidget.setItem(row , 0, QtWidgets.QTableWidgetItem(l))
            row += 1

        row = 0
        for x in self.settings['link_xpaths']:
            self.links_xpath_tableWidget.insertRow(self.links_xpath_tableWidget.rowCount())
            self.links_xpath_tableWidget.setItem(row , 0, QtWidgets.QTableWidgetItem(x))
            row += 1

        row = 0
        for s in self.settings['schemes']:
            self.schemes_tableWidget.insertRow(self.schemes_tableWidget.rowCount())
            self.schemes_tableWidget.setItem(row , 0, QtWidgets.QTableWidgetItem(s))
            row += 1
        row = 0
        for f in self.settings['files']:
            self.files_tableWidget.insertRow(self.files_tableWidget.rowCount())
            self.files_tableWidget.setItem(row , 0, QtWidgets.QTableWidgetItem(f))
            row += 1
        row = 0
        for t in self.settings['search_for_tags']:
            self.tags_tableWidget.insertRow(self.tags_tableWidget.rowCount())
            self.tags_tableWidget.setItem(row , 0, QtWidgets.QTableWidgetItem(t))
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
        if obj == "origins_compare_ratio_help_label":
            QMessageBox.information(self, "Origin Compare Ratio", """
What is origin compare ratio settings ?
Of course you  do not want to check all URLs with any origin, so you should set some settings to crawl just some specific ones with certain origin . 
Compare Ratio will compare origin of an URL with allowed origins, If it was similare to them cralwer will crawl it too .
So you need to set sensitivity of the comparison with the slider element .

این واسه اینه که هر اوریجینی رو تست نکنه . فرض کنید که میخواید یک وب سایت به ادرس زیر رو تست کنید :
https://site.dm
توی این سایت ممکن هست که لینکهایی از اوریجین های مختلف وجود داشته باشه و شما نخواید که همه رو تست کنید .
با فعال کردن این گزینه میتونید یک درجه شباهت به اوریجین دامنه اصلی بهش بدید و اوریجین هایی که شباهت با 
اوریجین اصلی دارن رو تشخیص میده و براتون اونها رو هم کرال میکنه .
            """)
        elif obj == "origins_contain_help_label":
            QMessageBox.information(self, "Origin Contain Settings", """
What is origin contain settings ?
Of course you  do not want to check all URLs with any origin, so you should set some settings to crawl just some specific ones with certain origin . 
Origin contain settings will allow you to set some spicific words, Crawler will cralw URLs with an origin that contains at least one of these words .
For example, If you set site,blog,news, Cralwer will crawl site.com, news.com, blog,com, news.site.com, ... but it won't cralw airport.com

این مورد واسه اینه که شما یک کلمه کلیدی رو قرار بدید و اوریجینی که اون کلمه کلیدی رو داره رو واسه شما تست میکنه . 
حتی میتونید تعداد متعددی کلمه کلیدی رو تعریف کنید به شکل زیر :
site,blog,news
اوریجین های مختلف رو تشخیص میده و بررسی میکنه که ایا این کلمات کلیدی توش هست یا خیر . اگه باشه اونها رو هم کرال میکنه وگرنه نادیده گرفته میشه .
            """)
        elif obj == "regex_pattern_help_label":
            QMessageBox.information(self, "Regex Patterns", """
Why you need to set some regex pattern for better crawling ?
Imagine you target is a shop website . It has a lot of products by shop.com/products/[product_id] URL . 
All of products pages have same structure and you do not need to check all of them and checking all of them is wasting time and resources .
You can set some regex pattern for some specific URLs like shop.com/products/[product_id] to check one of them not any more . 
Regex pattern and it's example should be matched and if they are not matched you will receive some errors .
                                    
یک تارگت میتونه تعدادی لینک داشته باشه که محتوای اون صفحه ساختار یکسانی داشته باشه . مثلا سایت زیر رو در نظر بگیرید :
https://shop.dm
این فروشگاه صفحات مخصوص محصولات داره که عینا واسه هر محصول تکرار میشه به شکل زیر :
https://shop.dm/products/12
https://shop.dm/products/15
...
شما میتونید با تعریف ریجکس این ادرس ها رو تشخیص بدید و کرالر فقط یک بار اونها رو کرال میکنه و بار دیگر نادیده میگیره .
            """)
        elif obj == "bad_links_help_label":
            QMessageBox.information(self, "Bad links", """
What is a bad link ?
Sometimes crawler detects some strings that are not link but their structures are like links . 
You can filter them here to not to waist your time by crawling wrong links . 
For example: "resource://", "chrome://", "data:image" are some strings who are not a real link,
by adding them to this list you can ignore them .
                                    
ممکن هست برخی از ادرس ها توسط کرالر اشتباه شناسایی شوند که در حقیقت ادرس یو ار ال درست نیستند . میتونید اونها رو توی این لیست تعریف کنید و کافیه که پروتکل اونها رو بنویسید و کرالر اونها رو نادیده میگیره .مثلا :
resource://, chrome://, data:image, ...
""")
        elif obj == "links_xpath_help_label":
            QMessageBox.information(self, "Links XPATH", """
What is xpath link ?
In a HTML document we have some attributes that can have links in themselves .
By extracting them from a HTML page we can find the links .
For example, href attributes, src attributes and ...
You can add your attributes to this list .

توی یک صفحه اچ تی ام ال لینک ها توی خصیصه هایی قرار داده میشوند مثلا :
src, href, action, ...
توی این جدول میتونید اونها رو تعریف کنید و کرالر توی صفحه لینک هایی که توی انها قرار داره رو استخراج میکنه . دقت کنید که باید ایکس پت اونها رو هم بنویسید .
""")
        elif obj == "schemes_help_label":
            QMessageBox.information(self, "Schemes", """
What is scheme ?
If you want to search for links with specific scheme you can add that scheme here to search for .
For example links that start with https:// or http:// .

هر لینکی یک پروتکلی داره و شما میتونید با تعریف پروتکل هایی توی این لیست به کرالر بگید که لینک هایی رو تشخیص بده که این پروتکل رو دارند . مثلا : 
https://, http://, ...
""")
        elif obj == "tags_help_label":
            QMessageBox.information(self, "Tags Table", """
Why we should add some tags here ?
If you add some tags to this list, Crawler will search for them in crawled web pages and will add them to a file in project folder .
For example, by default input, form, textarea are some tags that crawler will search for them inside a HTML document .
                                    
ممکن هست که علاوه بر لینک های توی یک صفحه به دنبال تگ های مختلفی باشید . مثلا تگهای :
input, form, textarea, ...
میتونید اونها رو توی این لیست تعریف کنید و کرالر علاوه بر لینکها این تگها رو هم پیدا میکنه و توی یک فایل برای شما ذخیره خواهد کرد تا بعدا بتونید به راحتی بهشون دسترسی پیدا کنید .
""")
        elif obj == "files_help_label":
            QMessageBox.information(self, "Files exclude table", """
Why we should add files mime here ?
By default crawler will search in all files from a target . 
For example, Javascript files, CSS files, JPG files and ...
We know that some of them have no links inside and you can add their mime type to this list to not to crawl them . 
For example, JPG files are binary and crawling inside them is waisting time . 

برخی از فایل ها هستند که محتوایی حاوی لینک ندارند . مثلا فایل های :
jpeg, png, ...
میتونید با تعریف میم تایپ اونها توی این لیست به کرالر بگید که در صورتی که به این لینک ها رسید اونها رو نادیده بگیره و کرال نکنه .           
""")

    
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
        self.settings['link_xpaths'] = self.getTableItems(self.links_xpath_tableWidget)
        self.settings['schemes'] = self.getTableItems(self.schemes_tableWidget)
        self.settings['search_for_tags'] = self.getTableItems(self.tags_tableWidget)
        self.settings['files'] = self.getTableItems(self.files_tableWidget)
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