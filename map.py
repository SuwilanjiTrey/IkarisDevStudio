import os
import re
import subprocess
#NEW file


def map_directory_structure(root_dir):
    file_structure = {} #create an array thats initially empty

    #for loop to traverse through the directory
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file in file_structure:
                file_structure[file].append(os.path.join(root, file)) #if there exists a file with the same name in different directories, put them in in index
            else:
                file_structure[file] = [os.path.join(root, file)] #this creates a dictionary with each key as the file
    
    
    return file_structure


def map_project_structure(root_dir):
    file_structure = {} #create an array thats initially empty

    #for loop to traverse through the directory
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file in file_structure:
                file_structure[file].append(os.path.join(root, file)) #if there exists a file with the same name in different directories, put them in in index
            else:
                file_structure[file] = [os.path.join(root, file)] #this creates a dictionary with each key as the file
    
    
    return file_structure

def find_file(file_structure, partial_name):
    #this function searches if the file is in the structure
    matching_files =[]
    for file_name in file_structure:
        if partial_name.lower() in file_name.lower(): #make it case insensitive
            matching_files.extend(file_structure[file_name])
    return matching_files if matching_files else None
    pass




def find_file_regex(file_structure, regex_pattern):
    # Compile the regular expression
    pattern = re.compile(regex_pattern, re.IGNORECASE)  # Case-insensitive
    matching_files = []
    
    for file_name in file_structure:
        if pattern.search(file_name):
            matching_files.extend(file_structure[file_name])
    return matching_files if matching_files else None
    pass

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except Exception as e:
        return f"An error occured while reading the file: {str(e)}"
    

def run_command_in_cmd(command, base_directory=None, new_window=False):
    if base_directory is None:
        base_directory = os.path.join(os.path.expanduser('~'), 'Desktop')
    
    if base_directory:
            os.chdir(base_directory)
        
            if new_window:
                cmd = ['start', 'cmd', '/K']
            else:
                cmd = ['cmd', '/C']
            
            # Join multiple commands with '&' for sequential execution
            full_command = ' & '.join(command)
            cmd.append(full_command)
            
            try:
                process = subprocess.Popen(cmd, shell=True)
                process.communicate(timeout=600)  # 10 minutes timeout
            except subprocess.TimeoutExpired:
                process.kill()
                raise
        
