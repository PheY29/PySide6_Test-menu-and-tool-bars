import random
import string
import json
import os

from PySide6.QtCore import QTimer, QSize
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (QMessageBox, QVBoxLayout, QWidget, QApplication, QTextEdit, QFileDialog,
                               QToolBar, QMainWindow)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.save_dir = os.path.join(os.path.dirname(__file__), "save")
        self.actual_text = ""

        self.setup_ui()
        self.setWindowTitle("Test MenuBar")
        self.resize(500, 400)

    def setup_ui(self):
        self.create_layouts()
        self.create_widgets()
        self.create_action()
        self.create_menu_bar()
        self.create_tool_bar()
        self.modify()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_layouts(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

    def create_action(self):
        # File
        self.action_newPage = QAction(QIcon("icons/new.png"), "New", self)
        self.action_newPage.triggered.connect(self.new_page)
        self.action_openFile = QAction(QIcon("icons/open.png"), "Open...", self)
        self.action_openFile.triggered.connect(self.open_file)
        self.action_saveFile = QAction(QIcon("icons/save.png"), "Save", self)
        self.action_saveFile.triggered.connect(self.save_file)
        self.action_saveFileAs = QAction(QIcon("icons/save_as.png"), "Save As...", self)
        self.action_saveFileAs.triggered.connect(self.save_file_as)
        self.action_exit = QAction(QIcon("icons/exit.png"), "Exit", self)
        self.action_exit.triggered.connect(self.close_appli)

        # Edit
        self.action_random_msg = QAction(QIcon("icons/write.png"), "Write word", self)
        self.action_random_msg.triggered.connect(self.write_word)
        self.action_undo = QAction(QIcon("icons/undo.png"), "Undo", self)
        self.action_undo.triggered.connect(self.undo_action)
        self.action_undo.setShortcut("Ctrl+Z")
        self.action_undo.setEnabled(False)
        self.action_redo = QAction(QIcon("icons/redo.png"), "Redo", self)
        self.action_redo.triggered.connect(self.redo_action)
        self.action_redo.setShortcut("Ctrl+Y")
        self.action_redo.setEnabled(False)
        self.action_copyText = QAction(QIcon("icons/copy.png"), "Copy", self)
        self.action_copyText.triggered.connect(self.copy_text)
        self.action_copyText.setShortcut("Ctrl+C")
        self.action_copyText.setEnabled(False)
        self.action_pastText = QAction(QIcon("icons/past.png"), "Past", self)
        self.action_pastText.triggered.connect(self.past_text)
        self.action_pastText.setShortcut("Ctrl+V")
        self.action_pastText.setEnabled(False)
        self.action_cutText = QAction(QIcon("icons/cut.png"), "Cut", self)
        self.action_cutText.triggered.connect(self.cut_text)
        self.action_cutText.setShortcut("Ctrl+X")
        self.action_cutText.setEnabled(False)
        self.action_selectAll = QAction(QIcon("icons/select all.png"), "Select All", self)
        self.action_selectAll.triggered.connect(self.select_all)
        self.action_selectAll.setShortcut("Ctrl+A")
        self.action_delete = QAction(QIcon("icons/delete.png"), "Delete", self)
        self.action_delete.triggered.connect(self.delete_text)
        self.action_delete.setShortcut("Del")
        self.action_delete.setEnabled(False)

        # Help
        self.action_about = QAction(QIcon("icons/about_(info).png"), "About", self)
        self.action_about.triggered.connect(self.show_about)

    def create_menu_bar(self):
        self.menuBar = self.menuBar()

        def create_file_menu():
            self.file_menu = self.menuBar.addMenu("&File")

            self.file_menu.addAction(self.action_newPage)
            self.file_menu.addSeparator()
            self.file_menu.addAction(self.action_openFile)
            self.file_menu.addAction(self.action_saveFile)
            self.file_menu.addAction(self.action_saveFileAs)
            self.file_menu.addSeparator()
            self.action_recentFile = self.file_menu.addMenu("Recent File")
            self.update_recent_files()
            self.file_menu.addSeparator()
            self.file_menu.addAction(self.action_exit)

        def create_edit_menu():
            self.edit_menu = self.menuBar.addMenu("&Edit")

            self.edit_menu.addAction(self.action_random_msg)
            self.edit_menu.addSeparator()
            self.edit_menu.addAction(self.action_undo)
            self.edit_menu.addAction(self.action_redo)
            self.edit_menu.addSeparator()
            self.edit_menu.addAction(self.action_copyText)
            self.edit_menu.addAction(self.action_pastText)
            self.edit_menu.addAction(self.action_cutText)
            self.edit_menu.addAction(self.action_selectAll)
            self.edit_menu.addAction(self.action_delete)

        def create_help_menu():
            self.help_menu = self.menuBar.addMenu("&Help")

            self.help_menu.addAction(self.action_about)

        create_file_menu()
        create_edit_menu()
        create_help_menu()

    def create_tool_bar(self):
        self.toolBar = QToolBar("Tool Bar")
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QSize(20, 20))  # print(self.toolBar.iconSize())
        self.addToolBar(self.toolBar)

        self.toolBar.addAction(self.action_newPage)
        self.toolBar.addAction(self.action_openFile)
        self.toolBar.addAction(self.action_saveFile)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_undo)
        self.toolBar.addAction(self.action_redo)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_copyText)
        self.toolBar.addAction(self.action_pastText)
        self.toolBar.addAction(self.action_cutText)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_exit)

    def create_widgets(self):
        self.te_content = QTextEdit()

    def modify(self):
        pass

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.te_content)

    def setup_connections(self):
        self.te_content.selectionChanged.connect(self.update_copy_cut_delete)
        self.te_content.copyAvailable.connect(self.update_copy_cut_delete)
        QApplication.clipboard().dataChanged.connect(self.update_clipboard)
        self.te_content.undoAvailable.connect(self.update_undo_redo)
        self.te_content.redoAvailable.connect(self.update_undo_redo)

    ############################
    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self,
                                                caption="Open a Text File",
                                                dir=self.save_dir,
                                                filter="Text Files (*.txt)")[0]
        if not file_path:
            return

        with open("".join(file_path), "r") as f:
            text = json.load(f)
            self.te_content.setText(text)

    def charge_file(self, file_name):
        file_path = os.path.join(self.save_dir, file_name)
        with open(file_path, "r") as f:
            text = json.load(f)
            self.te_content.setText(text)

    def save_content(self, directory=None, ask_directory=False):
        content = self.te_content.toPlainText()

        if ask_directory:
            directory = QFileDialog.getExistingDirectory(self, caption="Select the folder where will be saved")
            if not directory:
                return

        if not os.path.exists(directory):
            os.makedirs(directory)

        save_num = 1
        save_path = os.path.join(directory, f"save_{save_num}.txt")
        for file in os.listdir(directory):
            if "save" and str(save_num) in os.path.basename(file):
                save_num += 1

        with open(save_path, "w") as f:
            json.dump(content, f, indent=4)

        return save_path

    def save_file(self):
        self.save_content(directory=self.save_dir)
        self.update_recent_files()

    def save_file_as(self):
        self.save_content(ask_directory=True)
        self.update_recent_files()

    def update_recent_files(self):
        self.action_recentFile.clear()

        for file in os.listdir(self.save_dir):
            action = self.action_recentFile.addAction(file)
            action.triggered.connect(lambda checked, f=file: self.charge_file(f))

    def update_copy_cut_delete(self):
        if self.te_content.textCursor().hasSelection():
            self.action_delete.setEnabled(True)
            self.action_copyText.setEnabled(True)
            self.action_cutText.setEnabled(True)
        else:
            self.action_delete.setEnabled(False)
            self.action_copyText.setEnabled(False)
            self.action_cutText.setEnabled(False)

    def update_clipboard(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()
        if mime_data.hasText():
            self.action_pastText.setEnabled(True)
        else:
            self.action_pastText.setEnabled(False)

    def update_undo_redo(self):
        self.action_undo.setEnabled(self.te_content.document().isUndoAvailable())
        self.action_redo.setEnabled(self.te_content.document().isRedoAvailable())

    def delete_text(self):
        self.actual_text = self.te_content.toPlainText()
        self.te_content.clear()

    def select_all(self):
        self.te_content.selectAll()

    def undo_action(self):
        if self.actual_text:
            self.te_content.insertPlainText(self.actual_text)
            self.actual_text = ""
        else:
            self.te_content.undo()

    def redo_action(self):
        self.te_content.redo()

    def copy_text(self):
        self.te_content.copy()

    def past_text(self):
        self.te_content.paste()

    def cut_text(self):
        self.te_content.cut()

    def new_page(self):
        try:
            if self.timer:
                self.timer.stop()
        except AttributeError:
            return

        self.actual_text = self.te_content.toPlainText()
        self.te_content.clear()

    def close_appli(self):
        QApplication.quit()

    def write_word(self):
        self.num = 0
        all_words = string.ascii_lowercase

        def add_letter():
            if self.num < 100:
                random_number = random.randint(0, len(all_words) - 1)
                text = all_words[random_number]
                self.te_content.insertPlainText(text)
                self.num += 1
            else:
                self.timer.stop()

        self.timer = QTimer()  # start timer
        self.timer.timeout.connect(add_letter)
        self.timer.start(10)  # while timer isn't stop he's going to call add_letter

    def show_about(self):
        QMessageBox.information(self, "About Application", "Test menuBar v1.0\nCreate with PySide6.")


app = QApplication()
win = MainWindow()
win.show()
app.exec()
