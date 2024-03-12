from ui.main_window import Ui_MainWindow as MainWindow
from PyQt6 import QtWidgets
from PyQt6 import QtGui

class MainWindow(QtWidgets.QMainWindow, MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.project_name = "divar"
        self.setupUi(self)
        
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()