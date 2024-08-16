import os
import subprocess
import platform
import helpers.menu as menu
from helpers.file_handler import (
    create_folder,
    create_class_folders,
    get_course_codes,
    txt_file_to_str,
    get_lecture_num,
    get_cut_path,
    merge_cut_audio_files, compress_wav_to_mp3, rename_wav_file, get_files_in_directory
)
from helpers.input_safety import get_path, get_filename, get_positive_number, remove_timestamps, get_int
from helpers.process_audio import transcribe_to_file, move_wav_to_lectures, summarize_lecture
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
            record_now(course_codes=course_codes)
        case 2:
            transcribe_from_recording(course_codes=course_codes)
        case 3:
            summarize_from_transcript()
        case 4:
            view_file(course_codes=course_codes)
        case 5:
            print("5")
        case 6:
            print("Goodbye")


def record_now(course_codes):
    """
    Records lecture live then transcribes the audio and creates a summary sheet.
    Has the option to partly transcribe the lecture while the lecture is happening to speed up the process.

    :param List[str] course_codes: All the user's course codes

    :return: None
    """
    current_class = menu.choose_class(course_codes=course_codes)

    # Sets up mic to record audio to correct path
    i = 0
    lecture_num = get_lecture_num(current_class)
    mic = Recorder(file_path=get_cut_path(current_class=current_class, lecture_num=lecture_num, n=i))
    mic.start_recording()

    while True:
        # Gets users choice from recording menu
        user_input = menu.manage_live_recording()
        match user_input:

            # Cut recording and transcribe
            case "c":

                # Stop recording finalize .wav
                mic.stop_recording()

                # Start new recording
                i += 1
                wav_path = get_cut_path(current_class=current_class, lecture_num=lecture_num, n=i)
                mic = Recorder(file_path=wav_path)
                mic.start_recording()

                # Transcribe audio up to this point
                transcribe_to_file(
                    course_code=current_class,
                    lecture_num=lecture_num,
                    finalize_transcription=False,
                    cut_path_n=i-1,
                )

            case "s":
                # Stop recording finalize .wav
                mic.stop_recording()

                # Transcribe the remaining audio
                transcribe_to_file(
                    course_code=current_class,
                    lecture_num=lecture_num,
                    finalize_transcription=True,
                    cut_path_n=i
                )

                # Merge all cut .wav files into one .wav file
                merged_wav_path = merge_cut_audio_files(course_code=current_class, lecture_num=lecture_num)

                # Compress .wav file to an .mp3 file
                compress_wav_to_mp3(wav_file_path=merged_wav_path)

                # Create a summary sheet
                transcript_path = f"notes/{current_class}/transcripts/{lecture_num}.txt"
                transcript_clean_no_header = remove_timestamps(
                    transcript=txt_file_to_str(file_path=transcript_path)
                )
                summarize_lecture(
                    transcript=transcript_clean_no_header,
                    course_code=current_class,
                    lecture_num=lecture_num
                )

                # Ends loop when user exits
                return


def transcribe_from_recording(course_codes):
    """
    Transcribes and creates a summary sheet based off a lecture recording

    :param List[str] course_codes: All the user's course codes

    :return: None
    """
    current_class = menu.choose_class(course_codes=course_codes)

    # Gets the path of the audio to be processed
    wav_path = get_path(prompt="Path of your .wav file relative to this program: ")

    # Moves the .wav file to lectures
    lecture_num = get_lecture_num(current_class)
    new_path = move_wav_to_lectures(original_path=wav_path, course_code=current_class, current_lecture_num=lecture_num)

    # Transcribes the file
    transcribe_to_file(
        course_code=current_class,
        lecture_num=lecture_num,
        finalize_transcription=True
    )

    # Compresses lecture file
    print("Compressing")
    clean_wav_path = rename_wav_file(original_path=new_path, new_name=f"{lecture_num}")
    compress_wav_to_mp3(wav_file_path=clean_wav_path)

    # Creates a summary sheet
    transcript_path = f"notes/{current_class}/transcripts/{lecture_num}.txt"
    transcript_clean_no_header = remove_timestamps(transcript=txt_file_to_str(file_path=transcript_path))
    summarize_lecture(
        transcript=transcript_clean_no_header,
        course_code=current_class,
        lecture_num=lecture_num
    )


def summarize_from_transcript():
    """
    Creates a summary sheet based on a transcript

    :return: None
    """
    transcript_path = get_path(prompt="Transcript path relative to this program: ")
    course_code = get_filename(prompt="Course code: ")
    lecture_num = get_positive_number(prompt="Lecture #: ")

    transcript = txt_file_to_str(transcript_path)
    summarize_lecture(transcript=transcript, course_code=course_code, lecture_num=lecture_num)


def view_file(course_codes):
    """
    View any summary, transcript, or lecture file

    :param List[str] course_codes: All the user's course codes

    :return: None
    """
    # Get user choices about the media they want to view
    current_class = menu.choose_class(course_codes=course_codes)
    media_type = menu.select_media_type()

    # Get the filenames from the class and category the user wants to view
    files_in_folder = get_files_in_directory(f"notes/{current_class}/{media_type}")

    if len(files_in_folder) == 0:
        print("There are no files here")
        return

    print(f"Select from {media_type}")
    for i, file_name in enumerate(files_in_folder):
        print(f"{i+1}. {file_name}")

    file_num_picked = get_int(lowest_valid=1, highest_valid=len(files_in_folder), prompt="")

    # Open the file picked by the user on any os
    file_path = f"notes/{current_class}/{media_type}/{files_in_folder[file_num_picked-1]}"
    system = platform.system()

    if system == "Windows":
        os.startfile(file_path)
    elif system == "Darwin":
        subprocess.run(["open", file_path], check=True)
    elif system == "Linux":
        subprocess.run(["xdg-open", file_path], check=True)
    else:
        print(f"Unsupported operating system: {system}")


main()

