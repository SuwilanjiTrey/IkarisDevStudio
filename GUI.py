from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QListWidget, QTextEdit, QFileDialog, 
                             QTreeWidget, QTreeWidgetItem, QMessageBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSignal
import os, sys
from map import map_directory_structure, find_file, read_file

class FileSearcherApp(QWidget):
    directory_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Android_mini/images/File Searcher')
        self.setGeometry(100, 100, 1000, 600)

        self.setWindowIcon(QIcon('Android_mini/images/folder.png'))  # Replace with your icon path
        layout = QHBoxLayout()

        # Directory Tree Widget
        self.dir_tree = QTreeWidget(self)
        self.dir_tree.setHeaderLabel("Directory Structure")
        self.dir_tree.itemClicked.connect(self.display_selected_file)
        self.dir_tree.setStyleSheet("""
            QTreeWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTreeWidget::item:hover {
                background-color: #3a3a3a;
            }
            QTreeWidget::item:selected {
                background-color: #4a4a4a;
            }
        """)
        layout.addWidget(self.dir_tree)

        # Buttons
        tree_button_layout = QVBoxLayout()
        expand_button = self.create_button('Expand All', 'Android_mini/images/expand.png', self.expand_all)
        collapse_button = self.create_button('Collapse All', 'Android_mini/images/collapse.png', self.collapse_all)
        use_dir_button = self.create_button('Use Directory', 'Android_mini/images/use_file.png', self.use_directory)
        tree_button_layout.addWidget(expand_button)
        tree_button_layout.addWidget(collapse_button)
        tree_button_layout.addWidget(use_dir_button)
        layout.addLayout(tree_button_layout)

        # Right-side Layout
        right_layout = QVBoxLayout()

        # Root directory input
        dir_layout = QHBoxLayout()
        self.dir_input = QLineEdit(self)
        dir_button = self.create_button('Browse', 'Android_mini/images/search_folder.png', self.browse_directory)
        dir_layout.addWidget(QLabel('Root Directory:'))
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(dir_button)
        right_layout.addLayout(dir_layout)

        # Search input
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit(self)
        search_button = self.create_button('Search', 'Android_mini/images/search.png', self.search_file)
        search_layout.addWidget(QLabel('Search File:'))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        right_layout.addLayout(search_layout)

        # List widget to display found files
        self.result_list = QListWidget(self)
        self.result_list.itemSelectionChanged.connect(self.display_file_contents)
        self.result_list.setStyleSheet("""
            QListWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QListWidget::item:hover {
                background-color: #3a3a3a;
            }
            QListWidget::item:selected {
                background-color: #4a4a4a;
            }
        """)
        right_layout.addWidget(self.result_list)

        # Text edit to display file contents
        self.file_content_display = QTextEdit(self)
        self.file_content_display.setReadOnly(True)
        self.file_content_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: none;
            }
        """)
        right_layout.addWidget(self.file_content_display)

        layout.addLayout(right_layout)
        self.setLayout(layout)

        # Set the overall application style
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: #ffffff;
                border: none;
                padding: 5px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QPushButton:pressed {
                background-color: #5a5a5a;
            }
            QLineEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3a3a3a;
                padding: 2px;
            }
            QLabel {
                color: #ffffff;
            }
        """)



    def create_button(self, text, icon_path, connection):
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(connection)
        return button

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.dir_input.setText(directory)
            self.structure = map_directory_structure(directory)
            self.populate_tree(self.structure)
            print(f"Directory browsed: {directory}")  # Debug print

    

    def populate_tree(self, structure):
        self.dir_tree.clear()
        root_item = QTreeWidgetItem([self.dir_input.text()])
        root_item.setIcon(0, QIcon("Android_mini/images/folder.png"))
        self.dir_tree.addTopLevelItem(root_item)
        self.add_tree_items(root_item, structure)
        root_item.setExpanded(True)

    def add_tree_items(self, parent_item, structure):
        for item_name, item_value in structure.items():
            if isinstance(item_value, dict):  # Directory
                dir_item = QTreeWidgetItem(parent_item, [item_name])
                dir_item.setIcon(0, QIcon("fAndroid_mini/images/folder.png"))
                self.add_tree_items(dir_item, item_value)  # Recursively add sub-items
            else:  # File
                file_item = QTreeWidgetItem(parent_item, [item_name])
                file_item.setIcon(0, QIcon("Android_mini/images/file.png"))
                if isinstance(item_value, list):
                    file_item.setToolTip(0, "\n".join(item_value))  # Join list into a single string
                else:
                    file_item.setToolTip(0, item_value)

    def search_file(self):
        search_term = self.search_input.text()

        if not self.structure or not search_term:
            return

        found_files = find_file(self.structure, search_term)

        self.result_list.clear()
        if found_files:
            for path in found_files:
                self.result_list.addItem(path)
        else:
            self.result_list.addItem('No matching files found.')

    def display_file_contents(self):
        selected_item = self.result_list.currentItem()
        if selected_item:
            file_path = selected_item.text()
            if file_path != 'No matching files found.':
                content = read_file(file_path)
                self.file_content_display.setPlainText(content)

    def display_selected_file(self, item):
        # Only display file contents if the selected item is a file
        if item.childCount() == 0:  # No children means it's a file
            file_path = item.toolTip(0)
            if file_path:
                content = read_file(file_path)
                self.file_content_display.setPlainText(content)

    def expand_all(self):
        self.dir_tree.expandAll()

    def collapse_all(self):
        self.dir_tree.collapseAll()

    def use_directory(self):
        current_dir = self.dir_input.text()
        if current_dir and os.path.isdir(current_dir):
            print(f"Using directory: {current_dir}")  # Debug print
            self.directory_selected.emit(current_dir)
        else:
            print("No valid directory selected")  # Debug print
            QMessageBox.warning(self, 'Error', 'Please select a valid directory first.')
        

    def get_full_path(self, item):
        path = item.text(0)
        parent = item.parent()
        while parent:
            path = parent.text(0) + '/' + path
            parent = parent.parent()
        return path

#if __name__ == '__main__':
    