from ui.main_window import Ui_MainWindow as MainWindow
from PyQt6 import QtWidgets
from seleniumwire import webdriver 
from seleniumwire.utils import decode as sw_decode
from selenium.webdriver.common.by import By
from ui_obj.gui_helpers import add_link
from PyQt6.QtCore import *
import json
import time
import re
from urllib.parse import urlparse
import random
from difflib import SequenceMatcher


with open("mimeData.json", "r") as f_:
    mimes = f_.read()
mimes = json.loads(mimes)

class Interceptor(QThread):
    def __init__(self):
        super(Interceptor, self).__init__()
        self.driver = None
        self.requests_tableWidget = None

    def run(self):
        self.driver.response_interceptor = self.interceptor

    def add_to_listWidget(self, req, res):
        self.requests_tableWidget.insertRow(0)
        self.requests_tableWidget.setItem(0 , 0, QtWidgets.QTableWidgetItem(req.host))
        self.requests_tableWidget.setItem(0 , 1, QtWidgets.QTableWidgetItem(req.method))
        self.requests_tableWidget.setItem(0 , 2, QtWidgets.QTableWidgetItem(req.path))
        if len(req.params):
            params = "&".join([str(key) + ":" + str(req.params[key]) for key in req.params])
        else:
            params = ""
        self.requests_tableWidget.setItem(0 , 3, QtWidgets.QTableWidgetItem(params))
        self.requests_tableWidget.setItem(0 , 4, QtWidgets.QTableWidgetItem(str(res.status_code) + " " + res.reason))
        self.requests_tableWidget.setItem(0 , 6, QtWidgets.QTableWidgetItem(res.headers['Length']))
        self.requests_tableWidget.setItem(0 , 6, QtWidgets.QTableWidgetItem(req.headers['Content-Type']))
    def interceptor(self, req, res):
        self.add_to_listWidget(req, res)
    
class Crawler(): #QThread):
    def __init__(self):
        super(Crawler, self).__init__()
        self.quit_flag = False
        self.settings = {}
        self.links = []
        self.listWidget = None
        self.current_url_label = None
        self.requests_tableWidget = None
        self.counter_label = "0/0"
        self.project_name = ""

    def add_to_listWidget(self, link):
        self.listWidget.insertRow(0)
        self.listWidget.setItem(0 , 0, QtWidgets.QTableWidgetItem(link))
        self.listWidget.setItem(0 , 1, QtWidgets.QTableWidgetItem(str(0)))

    def link_absolute_maker(self, link, current_url):
        if len([y for y in self.settings['schemes'] if y in link]) == 0:
            current_url = urlparse(current_url).scheme + "://" + urlparse(current_url).netloc
            if link.startswith("/"):
                link = current_url + link
            elif link.startswith("/") == False:
                link = current_url + "/" + link
        return link

    def link_validation_chk(self, links, link, depth):
        # Bad links check
        for bad in self.settings['bad_links']:
            if bad in link:
                return (False, "Bad_link_detected")

        # Not be duplicate
        if len([y for y in links if y['link'] == link]) > 0:
            return (False, "Duplicated")
        
        # Not be in url patterns
        for pattern in self.settings['url_regex_patterns']:
            if re.match(pattern['pattern'], link):
                for l in [y for y in links]:
                    if re.match(pattern['pattern'], l['link']):
                        return (False, "url_regex_patterns_matched")
            

        # Not be file
        name = urlparse(url=link).path.split("/")[-1]
        try:
            ext = "." + name.split(".")[-1]
            fileType = [y['name'] for y in mimes if ext in y['fileTypes']]
            if len([y for y in self.settings['files'] if y in fileType[0]]) != 0:
                return (False, "is_file")
        except:
            pass

        # Not be in disallowed origins
        link_origin = urlparse(link).scheme + "://" + urlparse(link).netloc + "/"
        if link_origin in self.settings['origins']["disallowed"]:
                return (False, "disallowed_origin")
        elif link_origin not in self.settings['origins']['allowed'] and link_origin not in self.settings['origins']['disallowed']:
            if self.settings['origin_contains']:
                if len([y for y in self.settings['origin_contains_list'] if y in link_origin]):
                    self.settings['origins']["allowed"].append(link_origin)
                    with open("./projects/" + self.project_name + "/settings.json", "w") as f_:
                            f_.write(json.dumps(self.settings))
                else:
                    self.settings['origins']["disallowed"].append(link_origin)
                    with open("./projects/" + self.project_name + "/settings.json", "w") as f_:
                        f_.write(json.dumps(self.settings))
                    return (False, "disallowed_origin")
            if self.settings['origin_compare']:
                _tmp = [SequenceMatcher(None, y, link_origin).ratio() > self.settings['origin_compare_ratio'] for y in self.settings['origins']['allowed']]
                if len([y for y in _tmp if y == True]) > len([y for y in _tmp if y == False]):
                    self.settings['origins']["allowed"].append(link_origin)
                    with open("./projects/" + self.project_name + "/settings.json", "w") as f_:
                            f_.write(json.dumps(self.settings))
                elif len([y for y in _tmp if y == True]) == 0:
                    self.settings['origins']["disallowed"].append(link_origin)
                    with open("./projects/" + self.project_name + "/settings.json", "w") as f_:
                        f_.write(json.dumps(self.settings))
                    return (False, "disallowed_origin")
        return (True, "is_valid")
    
    def run(self):
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(self.settings['reqs_timeout'])

        self.interceptor = Interceptor()
        self.interceptor.driver = self.driver
        self.interceptor.requests_tableWidget = self.requests_tableWidget
        self.interceptor.start()


        while True:
            if not self.quit_flag:
                while len([x for x in self.links if x["checked"] == 0]) != 0:
                    for link in [x for x in self.links if x["checked"] == 0]:
                        self.current_url_label.setText("Current URL : " + link['link'])

                        try:
                            self.driver.get(url=link['link'])

                            self.counter_label.setText("Seen " + str(len([y for y in self.links if y['checked'] == 1])) + "/ Not Seen " + str(len([y for y in self.links if y['checked'] == 0])))
                            if self.settings['random_reqs_delay']:
                                time.sleep(random.randrange(self.settings['random_reqs_delay_from'], self.settings['random_reqs_delay_to']))
                            else:
                                time.sleep(self.settings['reqs_delay'])
                        except Exception as e:
                            continue
                        
                        self.links[self.links.index(link)]['checked'] = 1
                        for xpath in self.settings['link_xpaths']:
                            elms = self.driver.find_elements(By.XPATH, xpath['xpath'])
                            for elm in elms:
                                try:
                                    lnk = elm.get_dom_attribute(xpath['attr'])
                                    lnk = self.link_absolute_maker(link=lnk, current_url=self.driver.current_url)
                                    try:
                                        depth = [y['depth'] for y in self.links if y['link'] == self.driver.current_url][0] + 1
                                    except:
                                        depth = 0
                                    validation = self.link_validation_chk(self.links, lnk, depth)
                                    if validation[0] == True:
                                        self.links = add_link(self.links, lnk, depth=depth)
                                        print(self.links[-1])
                                        self.add_to_listWidget(link=lnk)
                                        self.counter_label.setText("Seen " + str(len([y for y in self.links if y['checked'] == 1])) + "/ Not Seen " + str(len([y for y in self.links if y['checked'] == 0])))
                                except Exception as e:
                                    print(e)
                                    continue
                self.quit_flag = True
            else:
                break
        # self.driver.close()
        # self.interceptor.quit()
        # self.interceptor.wait()
        # self.quit()
        # self.wait()


class MainWindow(QtWidgets.QMainWindow, MainWindow):
    def __init__(self, string_received, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.project_name = string_received
        print(self.project_name)
        self.setupUi(self)
        
        with open("projects/" + self.project_name + "/settings.json", "r") as f_:
            self.settings = json.loads(f_.read())
        with open("projects/" + self.project_name + "/links_found.json", "r") as f_:
            self.links = add_link(json.loads(f_.read()), self.settings['url'])

        self.depth = 3

        self.requests_tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.links_tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.current_url_label
        self.counter_label
        
        self.start_pushButton
        self.start_pushButton.setText("Start")
        self.start_pushButton.clicked.connect(self.create_process)
        
    def create_process(self):
        if self.start_pushButton.text() == "Start":
            self.start_pushButton.setText("Stop")
            self.crawler = Crawler()
            self.crawler.counter_label = self.counter_label
            self.crawler.project_name = self.project_name
            self.crawler.listWidget = self.links_tableWidget
            self.crawler.current_url_label = self.current_url_label
            self.crawler.links = self.links
            self.crawler.settings = self.settings
            self.crawler.requests_tableWidget = self.requests_tableWidget
            self.crawler.run()
            # self.crawler.start()
        else:
            self.crawler.quit_flag = True
            self.crawler.wait()
            print("Stopped")
            self.start_pushButton.setText("Start")

    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()