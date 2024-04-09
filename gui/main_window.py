from ui.main_window import Ui_MainWindow as MainWindow
from PyQt6 import QtWidgets
from gui_helpers import add_link
from PyQt6.QtCore import *
import json
from settings import paths

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
        self.start_pushButton.setText("Stop")
        print("Executing process")
        process = QProcess(self)
        process.readyReadStandardOutput.connect(self.on_ready_read_output)

        # Replace 'python_script.py' with the path to your Python script
        # Replace 'arg1' and 'arg2' with your command-line arguments
        python_path = paths['python_path']
        crawler_path = paths['crawler_path']
        process.start(python_path, [crawler_path, self.project_name])
        if not process.waitForStarted():
            print("Failed to start process.")


    def on_ready_read_output(self):
        process = self.sender()
        if process is not None and isinstance(process, QProcess):
            output = process.readAllStandardOutput().data().decode()
            if "Current link:" in output:
                # self.current_url_label.setText(output.replace("Current link: ", ""))
                print(output)
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()