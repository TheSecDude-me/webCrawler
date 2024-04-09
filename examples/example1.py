import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit
from PyQt6.QtCore import QProcess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Run External Process")
        self.setGeometry(100, 100, 500, 300)

        self.output_text_edit = QTextEdit(self)
        self.output_text_edit.setGeometry(10, 30, 480, 200)
        self.output_text_edit.setReadOnly(True)

        self.button = QPushButton("Run External Process", self)
        self.button.setGeometry(10, 240, 200, 30)
        self.button.clicked.connect(self.run_external_process)

    def run_external_process(self):
        self.output_text_edit.clear()
        process = QProcess(self)
        process.readyReadStandardOutput.connect(self.on_ready_read_output)

        # Replace 'python_script.py' with the path to your Python script
        # Replace 'arg1' and 'arg2' with your command-line arguments
        script_path = "examples/python_script.py"
        args = ["arg1", "arg23"]

        print("Starting process:", script_path, args)
        process.start("../.venv/Scripts/python.exe", [script_path] + args)
        if not process.waitForStarted():
            self.output_text_edit.append("Failed to start process.")
        print(process.exitCode())
    def on_ready_read_output(self):
        process = self.sender()
        if process is not None and isinstance(process, QProcess):
            output = process.readAllStandardOutput().data().decode()
            self.output_text_edit.append(output)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
