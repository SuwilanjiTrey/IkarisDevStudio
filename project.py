from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QListWidget, QTextEdit, QFileDialog, 
                             QTreeWidget, QTreeWidgetItem, QMessageBox, QInputDialog)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSignal, QDir
import os, sys, shutil
from map import map_project_structure, find_file, read_file

class ProjectStructer(QWidget):
    directory_selected = pyqtSignal(str)
 
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('create structure')
        self.setGeometry(100, 100, 1000, 600)

        self.setWindowIcon(QIcon('Android_mini/images/ANDROID_MINI.png'))  # Replace with your icon path
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
        use_dir_button = self.create_button('Use Directory', 'Android_mini/images/use_file.png', self.copy_path)
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
        # Get the directory of the current script
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construct the path to your desired starting directory
        start_directory = os.path.join(current_script_dir, "project_structure")
        
        # Create the directory if it doesn't exist
        if not os.path.exists(start_directory):
            os.makedirs(start_directory)
        
        # Open the file dialog
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", start_directory)
        
        if directory:
            self.dir_input.setText(directory)
            self.structure = map_project_structure(directory)
            self.populate_tree(self.structure)
            print(f"Directory browsed: {directory}")  # Debug print

        

    

    def populate_tree(self, structure):
        self.dir_tree.clear()
        root_item = QTreeWidgetItem([self.dir_input.text()])
        root_item.setIcon(0, QIcon("folder.png"))
        self.dir_tree.addTopLevelItem(root_item)
        self.add_tree_items(root_item, structure)
        root_item.setExpanded(True)

    def add_tree_items(self, parent_item, structure):
        for item_name, item_value in structure.items():
            if isinstance(item_value, dict):  # Directory
                dir_item = QTreeWidgetItem(parent_item, [item_name])
                dir_item.setIcon(0, QIcon("folder.png"))
                self.add_tree_items(dir_item, item_value)  # Recursively add sub-items
            else:  # File
                file_item = QTreeWidgetItem(parent_item, [item_name])
                file_item.setIcon(0, QIcon("file.png"))
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
           # self.copy_path()
            print(f"Using directory: {current_dir}")  # Debug print
        else:
            print("No valid directory selected")  # Debug print
            QMessageBox.warning(self, 'Error', 'Please select a valid directory first.')
        return current_dir

    def copy_path(self):
        source_dir = self.use_directory()  # Source directory is selected by the user
        if source_dir:
            # Get the name for the new project folder
            file_name, ok = QInputDialog.getText(self, 'New Project', 'Enter project name:')
            if ok and file_name:
                # Convert project name to lowercase for consistency
                project_name = file_name.lower()

                # Construct the path to your desired starting directory
                current_script_dir = os.path.dirname(os.path.abspath(__file__))
                start_directory = os.path.join(current_script_dir, "My_Projects", project_name)

                try:
                    # Create the directory if it doesn't exist
                    if not os.path.exists(start_directory):
                        os.makedirs(start_directory)

                    # Copy all contents from the source directory to the new directory
                    shutil.copytree(source_dir, start_directory, dirs_exist_ok=True)

                    # Perform renaming of "myapplication" to the new project name
                    self.replace_project_name(start_directory, "myapplication", project_name)

                    # Emit the signal with the new directory path
                    self.directory_selected.emit(start_directory)

                    QMessageBox.information(self, 'Success', f'Project copied and renamed to: {start_directory}')
                    print(f"Directory copied to: {start_directory}")  # Debug print
                except Exception as e:
                    QMessageBox.warning(self, 'Error', f'Failed to copy directory: {str(e)}')
                    print(f"Error copying directory: {str(e)}")  # Debug print
            else:
                print("Project creation cancelled")  # Debug print



    #new helper function
    def replace_project_name(self, directory, old_name, new_name):
        # Recursively go through all files and directories
        for root, dirs, files in os.walk(directory, topdown=False):
            # Rename files if they contain 'myapplication' in the name
            for file_name in files:
                if old_name in file_name:
                    old_file_path = os.path.join(root, file_name)
                    new_file_name = file_name.replace(old_name, new_name)
                    new_file_path = os.path.join(root, new_file_name)
                    os.rename(old_file_path, new_file_path)

            # Rename directories if they contain 'myapplication' in the name
            for dir_name in dirs:
                if old_name in dir_name:
                    old_dir_path = os.path.join(root, dir_name)
                    new_dir_name = dir_name.replace(old_name, new_name)
                    new_dir_path = os.path.join(root, new_dir_name)
                    os.rename(old_dir_path, new_dir_path)

            # Replace occurrences of 'myapplication' inside files
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()

                # Replace 'myapplication' in the file content
                if old_name in content:
                    new_content = content.replace(old_name, new_name)
                    with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
                        file.write(new_content)

        

    def get_full_path(self, item):
        path = item.text(0)
        parent = item.parent()
        while parent:
            path = parent.text(0) + '/' + path
            parent = parent.parent()
        return path

#if __name__ == '__main__':
    