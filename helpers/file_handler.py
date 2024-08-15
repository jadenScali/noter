import os
import shutil
from helpers.input_safety import get_int, get_filename


def write_to_file(file_path, content):
    """
    Appends the given text to a file with the specified file_path.
    If the file does not exist, it will be created.

    :param str file_path: The name of the file to write to (including the .txt extension) with its location (ie a path)
    :param str content: The text to write into the file

    :return: None
    """
    with open(file_path, 'a') as file:
        file.write(content)


def create_class_folders():
    """
    Creates the folders and subfolders for each class only if they do not already exist.
    Each class will get a transcripts, summaries and timestamped folder.

    :return: List[str] class names user entered
    """
    class_count = get_int(lowest_valid=1, highest_valid=100, prompt="How many classes do you have this semester?\n")
    course_codes = []

    # Saves the class names to course_codes and create appropriate files
    for i in range(class_count):
        course_codes.append(get_filename(f"Course code of class #{i + 1}: "))

        create_folder(f"notes/{course_codes[i]}")
        create_folder(f"notes/{course_codes[i]}/transcripts")
        create_folder(f"notes/{course_codes[i]}/summaries")
        create_folder(f"notes/{course_codes[i]}/timestamped")
        create_folder(f"notes/{course_codes[i]}/lectures")

    return course_codes


def create_folder(path):
    """
    Creates a folder only if it does not already exist.
    If it already exists but is empty it will return True

    :param str path: The path of the folder

    :return: Weather or not a folder was created
    """
    if not os.path.exists(path):
        os.mkdir(path)
        return True
    elif os.path.exists(path) and len(os.listdir(path)) == 0:
        return True

    return False


def get_course_codes():
    """
    Returns a list of folder names in the notes folder.

    :return: List[str] of folder names aka course_codes
    """

    folder_names = []
    notes_path = "notes"

    # Iterate through the entries in the notes folder
    for entry in os.listdir(notes_path):

        # Create the full path for each entry
        full_path = os.path.join(notes_path, entry)

        # Check if the entry is a directory
        if os.path.isdir(full_path):
            folder_names.append(entry)

    return folder_names


def get_lecture_num(course_code):
    """
    Goes into the timestamped folder for course_code and finds the next lecture number

    :param str course_code: Directory name in /notes

    :return: Next lecture number as a str
    """
    # Get a list of files in the timestamped directory
    timestamped_folder = f"notes/{course_code}/timestamped"

    files = [f for f in os.listdir(timestamped_folder) if
             os.path.isfile(os.path.join(timestamped_folder, f)) and f[0].isdigit()]

    # Create a list of numeric prefixes from the files
    nums = []
    for f in files:
        # Extract the numeric prefix
        prefix = ''
        for char in f:
            if char.isdigit():
                prefix += char
            else:

                # Stop at the first non-digit character
                break

        # If there's a numeric prefix, convert to integer and add to the list
        if prefix:
            nums.append(int(prefix))

    # Return the highest number + 1, or 0 if the list is empty
    if nums:
        return max(nums) + 1
    else:
        return 0


def move_and_rename_file(original_path, new_directory, new_filename):
    """
    Moves a file and renames it

    :param str original_path: The original file path
    :param str new_directory: The new directory
    :param str new_filename: The new filename

    :return:
    """
    # Ensure the new directory exists
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)

    # Create the new file path with the new filename
    new_path = os.path.join(new_directory, new_filename)

    # Move and rename the file
    shutil.move(original_path, new_path)

    return new_path

