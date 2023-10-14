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
        text (str): A string of text to be converted. Must contain newline characters to indicate split positions.

    Returns:
        list[str]: An array of strings representing the converted text. 
    """
    return text.split('\n')


def convert_string_to_part_pages(text):
    """Utility function to convert a string into a dictionary of part names and associated inclusive page ranges.

    Args:
        text (str): A string of text to be converted. 
        Must contain newline character indicating each new part, a comma between the part name and page range, and a hyphen between the page numbers.
        Example: Alto Sax 1, 12-14

    Returns:
        dict[str, (int, int)]: A dictionary of part name keys and associated inclusive page range values.
    """
    if '\n' not in text:
        raise ValueError('Text must contain a newline between each part.')
    
    result = {}
    
    for part in text.split('\n'):
        if ',' not in part:
            raise ValueError('Text must contain a comma between the part name and page range')
        part_pages = part.split(',', 1)
        
        if '-' not in part_pages[1]:
            raise ValueError('Text must contain a hyphen between the page range numbers.')
        page_numbers = part_pages[1].split('-', 1)
        
        result[part_pages[0].strip()] = (int(page_numbers[0].strip()), int(page_numbers[1].strip()))
    
    return result