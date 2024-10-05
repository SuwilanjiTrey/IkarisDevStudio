import sys
import os
import shutil
from Screen import mirror
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QTreeView, QFileSystemModel, QInputDialog, 
                             QMessageBox, QLineEdit, QStyle, QLabel, QToolButton, QAction, QMenu, QFileDialog)
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPixmap, QDesktopServices,  QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtCore import Qt, QDir, QUrl, QRegularExpression
from GUI import FileSearcherApp
from color import ColorCoat
from map import run_command_in_cmd
from testingnew import ProjectStructer
from syntax import CommentHighlighter


#main code logic
class CodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('IKARIS - 2024-V2 TM')
        self.setGeometry(100, 100, 1200, 800)

        self.setWindowIcon(QIcon('Android_mini/images/fav_icon.png'))  # Replace with your icon path

        # Main layout
        main_layout = QHBoxLayout()

        # File system view
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.currentPath()))
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setColumnWidth(0, 250)
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.clicked.connect(self.file_clicked)

        # Style the tree view
        self.tree.setStyleSheet("""
            QTreeView {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTreeView::item:hover {
                background-color: #3a3a3a;
            }
            QTreeView::item:selected {
                background-color: #4a4a4a;
            }
        """)


        file_system_layout = QVBoxLayout()
        
        button_layout = QHBoxLayout()
        new_folder_btn = self.create_button('New Folder', 'Android_mini/images/folder.png', self.create_new_folder)
        new_file_btn = self.create_button('New File', 'Android_mini/images/file.png', self.create_new_file)
        create_project = self.create_button('create android app', 'Android_mini/images/run_code.png', self.start_project)
        # In the initUI method, under button_layout, add these lines:
        delete_btn = self.create_button('', 'Android_mini/images/delete.png', self.delete_file)
        rename_btn = self.create_button('rename', 'Android_mini/images/rename.png', self.rename_file)
        

        button_layout.addWidget(new_folder_btn)
        button_layout.addWidget(new_file_btn)
        button_layout.addWidget(create_project)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(rename_btn)

        file_system_layout.addLayout(button_layout)
        file_system_layout.addWidget(self.tree)

        # Editor and Image Viewer
        self.editor = QTextEdit()
        self.editor.setFont(QFont('Courier', 12))
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: none;
            }
        """)

        # Image label for when no file is selected
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(QPixmap('Android_mini/images/ANDROID_MINI.png'))  # Load your image here
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #1e1e1e;
                color: #ffffff;
                border: none;
            }
        """)

        # Initially show the image and hide the editor
        
        self.image_label.setVisible(True)
        self.editor.setVisible(False)

        # Create a comment highlighter and apply it to the editor
        self.highlighter = CommentHighlighter(self.editor.document())

  

      

         # Buttons
        button_layout = QHBoxLayout()
        run_btn = self.create_button('Compile/Deploy', 'Android_mini/images/code.png', self.run_code)
        screen_btn = self.create_button('mirror phone', 'Android_mini/images/run_code.png', self.start_mirroring)
        
        build = self.create_button('build project', 'Android_mini/images/run_code.png', self.build)
        save_btn = self.create_button('Save File', 'Android_mini/images/save.png', self.save_file)
        open_searcher_btn = self.create_button('Open project folder', 'Android_mini/images/search_folder.png', self.open_file_searcher)
        
        button_layout.addWidget(build)
        button_layout.addWidget(run_btn)
        button_layout.addWidget(screen_btn)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(open_searcher_btn)

        

        # Create a QToolButton with a dropdown menu
        self.tool_button = QToolButton(self)
        self.tool_button.setText('Options')
        self.tool_button.setPopupMode(QToolButton.MenuButtonPopup)

        # Create a QMenu to act as the dropdown
        self.menu = QMenu(self)

        # Add actions to the menu
        action1 = QAction('Edit XML', self)
        action2 = QAction('create images', self)
        action3 = QAction('Add images', self)

        # Connect actions to methods
        action1.triggered.connect(lambda: self.option_selected('https://suwilanjitrey.github.io/android-xml-editor/'))
        action2.triggered.connect(lambda: self.option_selected('https://suwilanjitrey.github.io/android-xml-editor/image_editor.html'))
        action3.triggered.connect(lambda: self.add_images())

        # Add actions to the menu
        self.menu.addAction(action1)
        self.menu.addAction(action2)
        self.menu.addAction(action3)

        # Assign the menu to the tool button
        self.tool_button.setMenu(self.menu)

        # Add the button to the layout
        button_layout.addWidget(self.tool_button)







        # Putting it all together
        right_layout = QVBoxLayout()
        right_layout.addLayout(button_layout)
        right_layout.addWidget(self.editor)
        right_layout.addWidget(self.image_label)

        main_layout.addLayout(file_system_layout, 1)
        main_layout.addLayout(right_layout, 3)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.current_file = None
        self.current_folder = None

        self.clear_editor_or_show_image()
        
        # Set the overall application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: #ffffff;
                border: none;
                padding: 5px;
                margin: 2px;
            }
            QToolButton {
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
        """)

    def clear_editor_or_show_image(self):
        if self.current_file is None:
            self.editor.setVisible(False)
            self.image_label.setVisible(True)
        else:
            self.editor.setVisible(True)
            self.image_label.setVisible(False)

    def create_button(self, text, icon_path, connection):
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(connection)
        return button

    
    def file_clicked(self, index):
        path = self.model.filePath(index)
        
        if os.path.isdir(path):
            # Folder is clicked, set current_folder
            self.current_folder = path
            self.current_file = None  # Clear current_file since it's a folder
            #print(f'Selected folder: {self.current_folder}')       <--------------------print debug
        elif os.path.isfile(path):
            # File is clicked, set current_file and handle file preview
            self.current_file = path
            self.current_folder = None  # Clear current_folder since it's a file



            if path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.gif')):
                pixmap = QPixmap(path)
                self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
                self.image_label.setVisible(True)
                self.editor.setVisible(False)

                

            elif path.lower().endswith(('.exe', '.dll', '.cfg', '.ps1')):
                QMessageBox.warning(self, "Cannot Open File", "Executable files cannot be opened in this editor.")
                return  # Skip trying to open the file
            else:
                with open(path, 'r') as file:
                    self.editor.setText(file.read())
                self.editor.setVisible(True)
                self.image_label.setVisible(False)

            #print(f'Selected file: {self.current_file}')               <--------------------print debug


    def option_selected(self, url):
        QDesktopServices.openUrl(QUrl(url))
        #print(f'Selected: {url}')              <--------------------print debug

    def add_images(self):
        # Step 1: Check if a project directory is selected
        if not self.current_folder:
            QMessageBox.warning(self, 'Error', 'No project directory selected. Please select the "res" folder in your project.')
            return

        last_folder = os.path.basename(self.current_folder)
        #print(f'Last folder in current path: {last_folder}')           <--------------------print debug
        
        # Step 2: Ask user where they want to place the images: mipmap or drawable
        reply = QMessageBox.question(self, 'Select Target Directory',
                                    'Where do you want to place the images?\nYes: mipmap\nNo: drawable',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        # Determine the target folder based on user selection
        if reply == QMessageBox.Yes:
            target_dirs = {
                '_hdpi': 'mipmap-hdpi',
                '_mdpi': 'mipmap-mdpi',
                '_xhdpi': 'mipmap-xhdpi',
                '_xxhdpi': 'mipmap-xxhdpi',
                '_xxxhdpi': 'mipmap-xxxhdpi'
            }
            target_type = 'mipmap'
        else:
            target_dirs = {
                '_hdpi': 'drawable-hdpi',
                '_mdpi': 'drawable-mdpi',
                '_xhdpi': 'drawable-xhdpi',
                '_xxhdpi': 'drawable-xxhdpi',
                '_xxxhdpi': 'drawable-xxxhdpi'
            }
            target_type = 'drawable'
        
        # Step 3: Ensure that we are in the correct 'res' folder
        if last_folder == "res":
            res_folder = os.path.join(self.current_folder)

            if not os.path.exists(res_folder):
                QMessageBox.warning(self, 'Error', f'No "{target_type}" folder found in the selected project directory. Please select the "res" folder.')
                return

            # Step 4: Prompt the user to select multiple images
            image_paths, _ = QFileDialog.getOpenFileNames(self, 'Select Images', '', 'Image Files (*.png *.jpg *.jpeg *.webp)')

            if not image_paths:
                QMessageBox.warning(self, 'No Selection', 'No images were selected.')
                return

            # Step 5: Move the selected images to their corresponding mipmap or drawable directories
            for image_path in image_paths:
                file_name = os.path.basename(image_path)
                lower = file_name.lower()
                file_base, file_ext = os.path.splitext(lower)

                # Identify the density tag and corresponding directory
                for tag, target_folder in target_dirs.items():
                    if tag in file_base:
                        target_dir = os.path.join(res_folder, target_folder)
                        if not os.path.exists(target_dir):
                            os.makedirs(target_dir)  # Create target directory if it doesn't exist

                        # Copy the file to the target directory
                        new_file_name = file_base.replace(tag, '') + file_ext  # Remove the density tag
                        target_path = os.path.join(target_dir, new_file_name)
                        shutil.copy(image_path, target_path)

                        print(f"Image '{image_path}' placed in '{target_path}'")
                        break
                else:
                    print(f"Image '{image_path}' does not have a valid density tag.")

            QMessageBox.information(self, 'Success', f'Images have been successfully added to the {target_type} directories.')



    def delete_file(self):
        if self.current_file:
            # Deleting a file
            reply = QMessageBox.question(self, 'Confirm Delete',
                                        f'Are you sure you want to delete the file "{self.current_file}"?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    os.remove(self.current_file)
                    QMessageBox.information(self, 'Deleted', f'File deleted: {self.current_file}')
                    self.editor.clear()  # Clear the text editor
                    self.current_file = None
                except OSError as e:
                    QMessageBox.warning(self, 'Error', f'Failed to delete file: {str(e)}')

        elif self.current_folder:
            # Deleting a folder
            reply = QMessageBox.question(self, 'Confirm Delete',
                                        f'Are you sure you want to delete the folder "{self.current_folder}" and all its contents?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    shutil.rmtree(self.current_folder)
                    QMessageBox.information(self, 'Deleted', f'Folder deleted: {self.current_folder}')
                    self.current_folder = None
                except OSError as e:
                    QMessageBox.warning(self, 'Error', f'Failed to delete folder: {str(e)}')
        else:
            QMessageBox.warning(self, 'Error', 'No file or folder is currently selected.')

    def rename_file(self):
        if self.current_file or self.current_folder:
            new_name, ok = QInputDialog.getText(self, 'Rename', 'Enter new name:')
            if ok and new_name:
                if self.current_file:
                    # Renaming a file
                    new_path = os.path.join(os.path.dirname(self.current_file), new_name)
                    try:
                        os.rename(self.current_file, new_path)
                        QMessageBox.information(self, 'Renamed', f'File renamed to: {new_path}')
                        self.current_file = new_path  # Update the current file path
                        # Update the editor with the renamed file's content
                        with open(new_path, 'r') as file:
                            self.editor.setText(file.read())
                    except OSError as e:
                        QMessageBox.warning(self, 'Error', f'Failed to rename file: {str(e)}')

                elif self.current_folder:
                    # Renaming a folder
                    new_path = os.path.join(os.path.dirname(self.current_folder), new_name)
                    try:
                        os.rename(self.current_folder, new_path)
                        QMessageBox.information(self, 'Renamed', f'Folder renamed to: {new_path}')
                        self.current_folder = new_path  # Update the current folder path
                    except OSError as e:
                        QMessageBox.warning(self, 'Error', f'Failed to rename folder: {str(e)}')
        else:
            QMessageBox.warning(self, 'Error', 'No file or folder is currently selected.')




        

    def create_new_folder(self):
        index = self.tree.currentIndex()
        if index.isValid():
            dir_path = self.model.filePath(index)
            if os.path.isfile(dir_path):
                dir_path = os.path.dirname(dir_path)
            folder_name, ok = QInputDialog.getText(self, 'New Folder', 'Enter folder name:')
            if ok and folder_name:
                os.mkdir(os.path.join(dir_path, folder_name))

    def create_new_file(self):
        index = self.tree.currentIndex()
        if index.isValid():
            dir_path = self.model.filePath(index)
            if os.path.isfile(dir_path):
                dir_path = os.path.dirname(dir_path)
            file_name, ok = QInputDialog.getText(self, 'New File', 'Enter file name:')
            if ok and file_name:
                open(os.path.join(dir_path, file_name), 'w').close()

    def build(self):
        

        file_path = os.path.abspath(self.current_file)
        base_directory = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        file_extension = file_name.split('.')[-1]
        
        print(base_directory)
   


        commands = [
        "gradle build"
        
    ]


        print(commands)
        if commands:
            
            try:
                run_command_in_cmd(commands, base_directory=base_directory,new_window=True) 
                
            except subprocess.TimeoutExpired:
                QMessageBox.warning(self, 'Timeout', 'Code execution timed out after 10 seconds.')
        else:
            QMessageBox.warning(self, 'Error', f'Unsupported file type: .{file_extension}')
        

    def run_code(self):
        if not self.current_file:
            QMessageBox.warning(self, 'Error', 'No file selected, please select any .kt file...')
            return

        file_path = os.path.abspath(self.current_file)
        base_directory = os.path.dirname(file_path)
        #root = os.path.join(base_directory, "cd ..","cd ..","cd ..")
        file_name = os.path.basename(file_path)
        file_extension = file_name.split('.')[-1]
        
        #print(root)

        #commands = {
        #    'py': f"python \"{file_name}\"",
        #    'java': f"javac \"{file_name}\" && java \"{os.path.splitext(file_name)[0]}\"",
        #    'kt': f"kotlinc \"{file_name}\" -include-runtime -d \"{os.path.splitext(file_name)[0]}.jar\" && java -jar \"{os.path.splitext(file_name)[0]}.jar\""
        #      'kt': "gradle assembleDebug" 
        #}


        commands = [
        "gradle assembleDebug",
        f"adb install {os.path.join(base_directory, 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')}"
    ]

        print(commands)
        if commands:
            
            try:
                run_command_in_cmd(commands, base_directory=base_directory,new_window=True) 
                
            except subprocess.TimeoutExpired:
                QMessageBox.warning(self, 'Timeout', 'Code execution timed out after 10 seconds.')
        else:
            QMessageBox.warning(self, 'Error', f'Unsupported file type: .{file_extension}')
        


    def start_project(self):
        self.project = ProjectStructer()
        self.project.directory_selected.connect(self.update_directory)
        print("File searcher opened and signal connected")  # Debug print
        self.project.show()
        print("project created")


    def start_mirroring(self):
        result = mirror()
        if result.startswith("Error") or result.startswith("Timeout"):
            QMessageBox.warning(self, 'Error', result)
        else:
            QMessageBox.information(self, 'Success', result)
        print(result)



    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w') as file:
                file.write(self.editor.toPlainText())
            QMessageBox.information(self, 'Saved', f'File saved: {self.current_file}')
        else:
            QMessageBox.warning(self, 'Error', 'No file is currently open.')


    def open_file_searcher(self):
        self.file_searcher = FileSearcherApp()
        self.file_searcher.directory_selected.connect(self.update_directory)
        print("File searcher opened and signal connected")  # Debug print
        self.file_searcher.show()

    def update_directory(self, new_directory):
        print(f"Updating directory to: {new_directory}")  # Debug print
        if os.path.isdir(new_directory):
            self.tree.setRootIndex(self.model.index(new_directory))
            print("Directory updated successfully")  # Debug print
            QMessageBox.information(self, 'Directory Updated', f'Current directory changed to: {new_directory}')
        else:
            print(f"Invalid directory: {new_directory}")  # Debug print
            QMessageBox.warning(self, 'Error', f'Invalid directory: {new_directory}')





if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = CodeEditor()
    editor.show()
    sys.exit(app.exec_())