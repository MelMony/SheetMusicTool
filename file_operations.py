import os
import shutil

def move_files_to_directories(files, target_directories):
    """Utility function to move files (parts) into new directory locations (part folders).

    Args:
        files (str): A list of file paths representing the files to be moved
        target_directories (list[str]): A list of file paths representing the locations to output files
    """
    try: 
        # Check files exist
        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError

        for file, target_directory in zip(files, target_directories):
            # If folders dont yet exist make them
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)

            # Move files to folders - will replace any existing files of the same name
            shutil.move(file, os.path.join(target_directory, os.path.basename(file)))
            print(f"Moved {file} to {target_directory}.")
    
    except FileNotFoundError:
        print(f"File not found: {file}")


def convert_txt_file_to_string(file):
    """Utility function to convert the contents of a .txt file into a string format.

    Args:
        file (str): A file path representing a .txt file to be converted

    Returns:
        str: A string representing the contents of the supplied .txt file.
    """
    return ' '.join([str(elem) for elem in open(file, "r")])


def convert_string_to_array(text):
    """Utility function to convert a string into an array of strings using the newline character as the delimiter.

    Args:
        text (str): A string of text to be converted. Should contain newline characters to indicate split positions.

    Returns:
        list[str]: An array of strings representing the converted text. 
    """
    return text.split('\n')