from helpers.process_audio import transcribe_audio
from helpers.file_handler import create_folder, create_class_folders, get_course_codes
import helpers.menu as menu
from helpers.input_safety import get_path
from helpers.process_audio import transcribe_and_summarize


def main():
    """
    The main function to run this program after setup specified in the READ_ME.md

    :return: None
    """

    course_codes = []

    # If the notes folder didn't exist create it and populate it with classes
    note_root_path = "notes"
    if create_folder(note_root_path):
        course_codes += create_class_folders()
    else:
        course_codes += get_course_codes()

    # Display menu
    choice = menu.main()

    match choice:
        case 1:
            print("Record now")
        case 2:
            current_class = menu.choose_class(course_codes=course_codes)

            # Gets the path of the audio to be processed
            wav_path = get_path(prompt="Please enter the path of your .wav file relative to this program: ")

            transcribe_and_summarize(wav_path=wav_path, course_code=current_class)
        case 3:
            print("3")
        case 4:
            print("4")
        case 5:
            print("5")
        case 6:
            print("quit")


main()

