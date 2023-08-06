import os


def clear_terminal():
    """
    Clears Terminal"""
    if os.name=='nt': #Windows
        os.system('cls')

    else:
        os.system('clear')

def terminal_pathfind():
    """ Lets terminal users find and/or create directories
    entirely inside the commandline. Returns path as a string"""
    selected_directory = False # Remains false while no existing directory has been selected

    while not selected_directory:
        current_dir_contents = ' | '.join(map(str, os.listdir()))
        clear_terminal()

        # Prints the current files and folders in directory
        print("Current directory is {} \n\nThe directory contains: \n{}".format(os.getcwd(), current_dir_contents))

        choice = input("\nNote: you can use .. to go up a directory and mkdir to create a directory \nPlease select a directory: ")

        if choice.lower() == "mkdir":  # Create a directory Dialouge
            directory_name = str(input("What would you like to call the directory?: "))
            try:
                os.mkdir(directory_name)
            except expression as identifier:
                print("Invalid selection made \nError: {}".format(identifier))

        elif choice.lower() == "here":  # If they've selected the right folder
            chosen_directory = os.getcwd()
            return chosen_directory

        elif not choice.lower() == "here":  # If user wants to navigate to a different folder
            try:
                os.chdir(choice)
                selection = validate_menu_options(maximum = 2, minimum = 1,
                message="Current Path: {} \nWould you like to use the current path? (1)Yes (2)No :".format(os.getcwd()) )

                if selection == 1:
                    chosen_directory = os.getcwd()
                    return chosen_directory
                    selected_directory = True
                else:
                    continue
            except NotADirectoryError:
                print("Invalid selection made, choice is not a directory")


def select_directory(gui=False, use_cwd=False):
    """Allows user to select a directory and returns the path as a string
    gui: allows you to specify whether or not you want a tkinter dialogue
        box for picking the directory or a cli based directory selection
    use_cwd: returns the current working directory as a string
    """
    if use_cwd == True:
        return str(os.getcwd())

    if gui == False: #Terminal/cmd based path selector
        return terminal_pathfind()

    if gui == True: # GUI based file selector
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        file_path = str(filedialog.askdirectory(
                title="Specify Directory",
                mustexist=False))
        return file_path

def save_to_json(data, file_path = str(os.getcwd()), file_name = "config.json"):
    """Takes two parameters:
    data: JSON formatted data (Dictionary and/or class instance with vars(<instance>))
    file_path: A string representation of the path to output config.json to
    """
    import json
    # TODO: Check for right extension in file_name
    with open(os.path.join(file_path, file_name), 'w') as write_file:
        json.dump(data, write_file)

def center_text(message = "Hello World!"):
    """Takes a message and returns it centered in terminal
    message: The message to center
    """
    import shutil
    columns = shutil.get_terminal_size().columns
    return(message.center(columns))

def validate_int_selection(self, maximum = 1, minimum=0, message = "Please select one of the above options: "):
        """
        Takes three parameters:
        maximum: The maximumimum value
        minimum: The minimum value
        Message: What to prompt user with when function is called
        """
        valid_answer = False

        while valid_answer == False:
            try: # Catches if answer is not int or float
                selection = eval(input(message))
            except:
                print("Invalid input please try again")

            if selection > maximum: # More than maximum
                print("Invalid input the selection made was larger than {}".format(maximum))

            elif selection < minimum:#Less than minimum
                print("Invalid input the selection made was smaller than {}".format(minimum))

            else: # If answer is valid and in range
                return selection
