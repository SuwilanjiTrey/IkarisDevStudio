import tkinter as tk
from map import map_directory_structure,find_file, read_file #,find_file_regex
#remove the comment if you wish to add the regex logic 
#testing code


def get_input():
    root_dir = input("Enter the root directory of your project:     ")
    structure = map_directory_structure(root_dir)


    #DEBUGGING
    #for file, path in structure.items():
    #    print(f"{file}: {path}")

    find_files_searched = input("what file would you like to find?    ")
    found = find_file(structure,find_files_searched) #if you wish to implement the logic of regex, replace "find_files_searched" with "regex"


    if found:
        for path in found:
            print(f"File found: {path}")
    else:
        print("file not found....")

    read = input("would you like to display the contents of this file?  (yes/no)")
    if read.lower() == "yes":
        if found:
            for index, path in enumerate(found):
                print(f"{index + 1}.{path}")

            if len(found) > 1:
                file_choice = int(input(f"enter the number of the file you want to read:     "))

            else:
                file_choice = 0


            file_content = read_file(found[file_choice])
            print(f"\nContents of {found[file_choice]}: \n")
            print(file_content)
        else:
            print("No matching files found")

if __name__ == "__main__":
    get_input()

