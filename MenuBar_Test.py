import random
import string

from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox, QVBoxLayout, QPushButton, QWidget, QApplication, QTextEdit, QMenuBar


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setWindowTitle("Test MenuBar")
        self.resize(500, 400)

    def setup_ui(self):
        self.create_layouts()
        self.create_menu_bar()
        self.create_widgets()
        self.modify()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_layouts(self):
        self.main_layout = QVBoxLayout(self)

    def create_menu_bar(self):
        self.menuBar = QMenuBar(self)

        def create_file_menu():
            self.file_menu = self.menuBar.addMenu("&File")

            self.action_newPage = self.file_menu.addAction(QIcon("icons/new.png"), "New page")
            self.file_menu.addSeparator()
            self.action_exit = self.file_menu.addAction(QIcon("icons/exit.png"), "Exit")

            self.action_newPage.triggered.connect(self.clear_text)
            self.action_exit.triggered.connect(self.close_appli)

        def create_edit_menu():
            self.edit_menu = self.menuBar.addMenu("&Edit")

            self.action_random_msg = self.edit_menu.addAction(QIcon("icons/add.png"), "write word")
            self.action_random_msg.triggered.connect(self.write_msg)

        def create_help_menu():
            self.help_menu = self.menuBar.addMenu("&Help")

            self.action_about = self.help_menu.addAction(QIcon("icons/about_(info).png"), "About")
            self.action_about.triggered.connect(self.show_about)

        create_file_menu()
        create_edit_menu()
        create_help_menu()

    def create_widgets(self):
        self.te_content = QTextEdit()

    def modify(self):
        pass

    def add_widgets_to_layouts(self):
        self.main_layout.setMenuBar(self.menuBar)
        self.main_layout.addWidget(self.te_content)

    def setup_connections(self):
        pass

    ############################
    def clear_text(self):
        self.timer.stop()
        self.te_content.clear()

    def close_appli(self):
        QApplication.quit()

    def write_msg(self):
        self.num = 0
        all_words = string.ascii_lowercase

        def add_letter():
            if self.num < 500:
                random_number = random.randint(0, len(all_words) - 1)
                text = all_words[random_number]
                self.te_content.insertPlainText(text)
                self.num += 1
            else:
                self.timer.stop()

        self.timer = QTimer()  # start timer
        self.timer.timeout.connect(add_letter)
        self.timer.start(10)  # while timer isn't stop he going to call add_letter

    def show_about(self):
        QMessageBox.information(self, "About Application", "Test menuBar v1.0\nCreate with PySide6.")


app = QApplication()
win = MainWindow()
win.show()
app.exec()
