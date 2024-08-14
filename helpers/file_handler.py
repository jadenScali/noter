import os
from helpers.input_safety import get_int, get_filename


def write_to_file(filename, content):
    """
    Appends the given text to a file with the specified filename.
    If the file does not exist, it will be created.

    :param str filename: The name of the file to write to (including the .txt extension)
    :param str content: The text to write into the file

    :return: None
    """
    with open(filename, 'a') as file:
        file.write(content)
    print(f"Transcription written to {filename}")


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

