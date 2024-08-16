from helpers.file_handler import create_folder, create_class_folders, get_course_codes, txt_file_to_str, get_lecture_num
import helpers.menu as menu
from helpers.input_safety import get_path, get_filename, get_positive_number
from helpers.process_audio import transcribe_and_summarize, summarize_lecture
from helpers.recorder import Recorder

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
            current_class = menu.choose_class(course_codes=course_codes)

            # Sets up mic to record audio to correct path
            mic = Recorder(file_path=f"notes/{current_class}/lectures/{get_lecture_num(course_code=current_class)}.wav")
            mic.start_recording()

        case 2:
            current_class = menu.choose_class(course_codes=course_codes)

            # Gets the path of the audio to be processed
            wav_path = get_path(prompt="Path of your .wav file relative to this program: ")

            transcribe_and_summarize(wav_path=wav_path, course_code=current_class)
        case 3:
            transcript_path = get_path(prompt="Transcript path relative to this program: ")
            course_code = get_filename(prompt="Course code: ")
            lecture_num = get_positive_number(prompt="Lecture #: ")

            transcript = txt_file_to_str(transcript_path)
            summarize_lecture(transcript=transcript, course_code=course_code, lecture_num=lecture_num)
        case 4:
            print("4")
        case 5:
            print("5")
        case 6:
            print("Goodbye")


main()

