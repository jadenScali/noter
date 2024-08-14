import os


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


def create_class_folders(class_names):
    """
    Creates the folders and subfolders for each class only if they do not already exist.
    Each class will get a transcripts, summaries and timestamped folder.

    :param List[str] class_names: Names of the classes aka names of the folders

    :return: None
    """
    note_root_path = "notes"
    create_folder(note_root_path)

    for name in class_names:
        create_folder(f"notes/{name}")
        create_folder(f"notes/{name}/transcripts")
        create_folder(f"notes/{name}/summaries")
        create_folder(f"notes/{name}/timestamped")


def create_folder(path):
    """
    Creates a folder only if it does not already exist.

    :param str path: The path of the folder

    :return: None
    """

    if not os.path.exists(path):
        os.mkdir(path)

