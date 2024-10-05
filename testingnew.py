import os
import sys
import shutil
from PyQt5.QtWidgets import QInputDialog, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QGridLayout, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal, QStandardPaths, QSize, Qt


 


class ProjectStructer(QWidget):
    directory_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.selected_app_type = None  # Store the selected app type
        self.project_templates = {
            "No Activity": "project_structure/NoActivity",
            "Basic Activity": "project_structure/Basic_views_activity",
            "Empty Activity": "project_structure/EmptyActivity",
            "Empty Views Activity": "project_structure/EmptyViewsActivity",
            "Navigation Drawer": "project_structure/NavigationDrawerViewsActivity",
            "Bottom Navigation": "project_structure/Bottom_navigation_views_activity",
            "Responsive Activity": "project_structure/ResponsiveViewsActivity",
            "Game Activity(C++)": "project_structure/GameActivity(C++)",
            "Native C++": "project_structure/NativeC++"

            # Map more application types to their respective folders
        }
        self.app_type_descriptions = {
            "No Activity": "Creates a basic Android project without any initial activity. Suitable for projects where you want to start from scratch or have full control over the initial setup.",
            "Basic Activity": "Generates a project with a basic activity and a simple app bar. Ideal for straightforward applications that don't require complex navigation.",
            "Empty Activity": "Creates a project with a single, empty activity. Perfect for simple applications or as a starting point for custom layouts.",
            "Empty Views Activity": "Similar to Empty Activity, but uses the newer ViewBinding feature for more efficient view access. Good for modern Android development practices.",
            "Navigation Drawer": "Sets up a project with a side menu (drawer) for navigation. Useful for apps with multiple sections or complex navigation structures.",
            "Bottom Navigation": "Creates an app with a bottom navigation bar. Great for apps with 3-5 main sections that users switch between frequently.",
            "Responsive Activity": "Generates a project designed to adapt to different screen sizes and orientations. Ideal for apps that need to work well on both phones and tablets.",
            "Game Activity(C++)": "Sets up a project with native C++ support, optimized for game development. Use this for high-performance games or apps requiring low-level access.",
            "Native C++": "Creates a project with native C++ support. Suitable for apps that require high performance or need to integrate with C++ libraries."
        }        
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Create Project Structure')
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowIcon(QIcon('Android_mini/images/ANDROID_MINI.png'))

        layout = QHBoxLayout()

        # Grid layout for application type buttons
        button_grid_layout = QGridLayout()
        self.add_application_type_buttons(button_grid_layout)
        layout.addLayout(button_grid_layout)

        # Create Project button in the center
        self.create_project_button = self.create_button('Create Project', 'Android_mini/images/create_project.png', self.create_project)
        layout.addWidget(self.create_project_button)

        # Right-side layout (Directory input and project info)
        right_layout = QVBoxLayout()

        # Directory input for selecting project folder
        dir_layout = QHBoxLayout()
        self.dir_input = QLineEdit(self)
        dir_button = self.create_button('', 'Android_mini/images/search_folder.png', self.browse_directory)
        dir_layout.addWidget(QLabel('Create project in:'))
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(dir_button)
        right_layout.addLayout(dir_layout)

        # Application type info display
        self.app_info_display = QTextEdit(self)
        self.app_info_display.setReadOnly(True)
        right_layout.addWidget(self.app_info_display)

        # Additional IDE information display
        self.additional_info_display = QTextEdit(self)
        self.additional_info_display.setReadOnly(True)
        right_layout.addWidget(self.additional_info_display)

        layout.addLayout(right_layout)
        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget { background-color: #2b2b2b; color: #ffffff; }
            QPushButton { background-color: #3a3a3a; color: #ffffff; border: none; padding: 5px; margin: 2px; }
            QPushButton:hover { background-color: #4a4a4a; }
            QPushButton:pressed { background-color: #5a5a5a; }
            QLineEdit { background-color: #1e1e1e; color: #ffffff; border: 1px solid #3a3a3a; padding: 2px; }
            QTextEdit { background-color: #1e1e1e; color: #ffffff; border: none; }
            QLabel { color: #ffffff; }
        """)



    def add_application_type_buttons(self, layout):
        app_types = list(self.project_templates.keys())
        app_icons = {
            "No Activity": "Android_mini/images/no_activity.png",
            "Basic Activity": "Android_mini/images/basic_activity.png",
            "Empty Activity": "Android_mini/images/empty_activity.png",
            "Navigation Drawer": "Android_mini/images/drawer_activity.png",
            "Bottom Navigation": "Android_mini/images/bottom_navigation.png",
            "Game Activity(C++)": "Android_mini/images/game_activity.png",
            "Empty Views Activity": "Android_mini/images/empty_views_activity.png",
            "Responsive Activity": "Android_mini/images/responsive_views.png",
            "Native C++": "Android_mini/images/native_C.png"
        }
        
        
        for i, app_type in enumerate(app_types):
            button = QPushButton(app_type)
            
            # Set the icon for the button if an icon exists for the app type
            icon_path = app_icons.get(app_type, None)
            if icon_path:
                button.setIcon(QIcon(icon_path))
                button.setIconSize(QSize(64, 64))  # Set the icon size

            # Align the icon on top and text at the bottom
            button.setStyleSheet("""
                QPushButton {
                    text-align: center;  /* Align text in the center */
                    padding: 10px;       /* Add padding around the button */
                    font-size: 12px;     /* Adjust the font size */
                }
                QPushButton:hover {
                    background-color: #4a4a4a;  /* Add hover effect */
                }
                QPushButton:pressed {
                    background-color: #5a5a5a;  /* Add pressed effect */
                }
                QPushButton:icon {
                    display: block;
                }
                """)
    
    # Connect the button click to the handler
            button.clicked.connect(lambda: self.handle_button_click())
            
            # Add the button to the grid layout
            layout.addWidget(button, i // 3, i % 3)

    def handle_button_click(self):
        sender = self.sender()
        self.selected_app_type = sender.text()
        self.display_app_type_info(self.selected_app_type)


    def display_app_type_info(self, app_type):
        description = self.app_type_descriptions.get(app_type, "No description available.")
        template_info = f"Template: {self.project_templates.get(app_type, 'Unknown')}"
        
        info_text = f"Application Type: {app_type}\n\n"
        info_text += f"Description:\n{description}\n\n"
        #info_text += f"Technical Details:\n{template_info}\n\n"
        info_text += "This template provides a starting point for your Android application. "
        info_text += "You can customize and expand upon this structure to build your specific app features."

        self.app_info_display.setPlainText(info_text)




    def browse_directory(self):
        desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", desktop_path)
        if directory:
            self.dir_input.setText(directory)


    def use_directory(self):
        current_dir = self.dir_input.text()
        if current_dir and os.path.isdir(current_dir):
            print(f"Using directory: {current_dir}")  # Debug print
        else:
            print("No valid directory selected")  # Debug print
            QMessageBox.warning(self, 'Error', 'Please select a valid directory first.')
        return current_dir

    def create_button(self, text, icon_path, connection):
        button = QPushButton(text)
        if icon_path:
            button.setIcon(QIcon(icon_path))
        button.clicked.connect(connection)
        return button

    def create_project(self):
        if not self.selected_app_type:
            QMessageBox.warning(self, 'Error', 'Please select an application type.')
            return

        target_directory = self.dir_input.text().strip()
        if not target_directory:
            QMessageBox.warning(self, 'Error', 'Please select a target directory.')
            return

        project_name, ok = QInputDialog.getText(self, 'Project Name', 'Enter the project name:')
        if not ok or not project_name:
            return

        # Now get the template folder associated with the selected application type
        template_folder = self.project_templates.get(self.selected_app_type)
        newname = project_name.lower()
        if not template_folder:
            QMessageBox.warning(self, 'Error', 'Invalid application type selected.')
            return

        try:
            # Use the copy_path method to copy and rename the project
            self.copy_path(template_folder, target_directory, newname)
            QMessageBox.information(self, 'Success', f'Project {project_name} created successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to create project: {e}')

    def copy_path(self, template_folder, target_directory, project_name):
        # Construct the target directory (i.e., where the new project will be created)
        start_directory = os.path.join(target_directory, project_name)

        try:
            if not os.path.exists(start_directory):
                os.makedirs(start_directory)

            # Copy all contents from the template folder to the target directory
            shutil.copytree(template_folder, start_directory, dirs_exist_ok=True)

            # Rename placeholders (such as 'myapplication') in the copied files
            self.replace_project_name(start_directory, "myapplication", project_name)

            # Emit signal with the new directory path
            self.directory_selected.emit(start_directory)

            print(f"Project copied and renamed to: {start_directory}")  # Debug print
        except Exception as e:
            print(f"Error copying project: {str(e)}")  # Debug print
            raise e

    def replace_project_name(self, directory, old_name, new_name):
        # Traverse all files in the directory and replace the old project name
        for root, dirs, files in os.walk(directory, topdown=False):
            for file_name in files:
                if old_name in file_name:
                    old_file_path = os.path.join(root, file_name)
                    new_file_name = file_name.replace(old_name, new_name)
                    new_file_path = os.path.join(root, new_file_name)
                    os.rename(old_file_path, new_file_path)

            for dir_name in dirs:
                if old_name in dir_name:
                    old_dir_path = os.path.join(root, dir_name)
                    new_dir_name = dir_name.replace(old_name, new_name)
                    new_dir_path = os.path.join(root, new_dir_name)
                    os.rename(old_dir_path, new_dir_path)

            # Replace occurrences of 'myapplication' inside the file contents
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()

                if old_name in content:
                    new_content = content.replace(old_name, new_name)
                    with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
                        file.write(new_content)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = ProjectStructer()
    editor.show()
    sys.exit(app.exec_())
