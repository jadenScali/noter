from helpers.transcribe import transcribe_audio
from helpers.file_handler import write_to_file, create_folder, create_class_folders, get_course_codes
import helpers.menu as menu
import time


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
            print("2")
        case 3:
            print("3")
        case 4:
            print("4")
        case 5:
            print("5")
        case 6:
            print("quit")

    # start_time = time.time()
    #
    # transcript_raw = transcribe_audio(wav_file="rick_proper.wav")
    #
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    #
    # print("Transcription Result:", transcript_raw)
    # print(f"Time taken: {elapsed_time:.2f} seconds")
    #
    # write_to_file(filename="test.txt", content=transcript_raw)


main()

