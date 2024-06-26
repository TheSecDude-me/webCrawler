from ui.create_new_project import Ui_Form as create_new_project
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QMessageBox
from gui_helpers import delete_folder, create_new_project_next
from PyQt6.QtCore import *
import sys
import os
from project_settings import ProjectSettingsWindow

class CreateNewProjectWindow(QtWidgets.QMainWindow, create_new_project):

    def __init__(self, *args, obj=None, **kwargs):
        super(CreateNewProjectWindow, self).__init__(*args, **kwargs)
        
        self.setupUi(self)

        self.get_recent_projects()

    def get_recent_projects(self):
        model = QtGui.QStandardItemModel()
        self.projects_listView.setModel(model)
        for project in os.listdir("projects"):
            item = QtGui.QStandardItem(project)
            model.appendRow(item)
        
        self.remove_pushButton.clicked.connect(self.remove)
        self.next_pushButton.clicked.connect(self.next)

    def remove(self):
        reply = QMessageBox.question(self, 'Remove', 'Are you sure you want to remove this project ?',
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        
        if(reply == QMessageBox.StandardButton.Yes):
            for index in self.projects_listView.selectedIndexes():
                item = self.projects_listView.model().itemFromIndex(index)
                project = item.text()
                delete_folder("./projects/" + project)
                self.projects_listView.model().removeRow(index.row())
    def next(self):

        project_name = self.project_name_lineEdit.text()
        
        # Create a new project or open recent project ?
        selected_project = self.projects_listView.selectedIndexes()
        if selected_project:
            project_name = selected_project[0].data()
            result = [True, ""]
        else:
            result = create_new_project_next(project_name)

        if result[0] == False:
            QMessageBox.critical(self, result[1], result[2])
            return 
        if result[0] == True:
            self.get_recent_projects()
            self.close()
            # Now show next window
            self.project_settings_window = ProjectSettingsWindow(string_received=project_name)
            self.project_settings_window.show()
            self.close()    
            return
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CreateNewProjectWindow()
    window.show()
    app.exec()