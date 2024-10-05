#test
import subprocess
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QTreeView, QFileSystemModel, QInputDialog, 
                             QMessageBox, QLineEdit, QStyle)
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QDir
from map import run_command_in_cmd

class ScreenMirror(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # ... (other UI initialization code) ...

        self.mirror_button = QPushButton('Mirror Screen', self)
        self.mirror_button.clicked.connect(self.mirror_screen)
        # Add this button to your layout

    def mirror_screen(self):
        scrcpy_path = self.find_scrcpy()
        if not scrcpy_path:
            QMessageBox.warning(self, 'Error', 'scrcpy not found. Please make sure it\'s installed and in your PATH.')
            return

        try:
            subprocess.Popen([scrcpy_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            QMessageBox.information(self, 'Success', 'Screen mirroring started. Check the new command window.')
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, 'Error', f'Failed to start scrcpy: {str(e)}')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'An unexpected error occurred: {str(e)}')

    def find_scrcpy(self):
        # First, check if scrcpy is in PATH
        scrcpy_path = shutil.which('scrcpy')
        if scrcpy_path:
            return scrcpy_path

        # If not in PATH, check the default location you mentioned
        default_path = os.path.join(os.getcwd(), 'scrcpy-win64-v2.3.1', 'scrcpy.exe')
        if os.path.exists(default_path):
            return default_path

        # If still not found, ask the user for the location
        scrcpy_path, ok = QInputDialog.getText(self, 'scrcpy not found', 
                                               'Enter the full path to scrcpy.exe:')
        if ok and os.path.exists(scrcpy_path):
            return scrcpy_path

        return None



def mirror():
    # Get the directory where the script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to scrcpy.exe
    scrcpy_path = os.path.join(current_dir, "scrcpy-win64-v2.3.1", "scrcpy.exe")
    
    # Check if the file exists
    if not os.path.exists(scrcpy_path):
        return f"Error: scrcpy.exe not found at {scrcpy_path}"
    
    # Construct the command
    command = [f"{scrcpy_path}"]
    print(f"Executing command: {command}")
    
    try:
        # Run the command
        result = run_command_in_cmd(command, new_window=True)
        return f"Screen mirroring started successfully. Result: {result}"
    except subprocess.TimeoutExpired:
        return "Timeout: Code execution timed out after 10 seconds."
    except Exception as e:
        return f"Error: {str(e)}"

"""
if __name__ == '__main__':
    app = QApplication([])
    mirror = ScreenMirror()
    mirror.show()
    app.exec_()
"""