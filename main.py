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
    merge_cut_audio_files,
    compress_wav_to_mp3,
    rename_wav_file,
    get_files_in_directory,
    move_directory,
    convert_to_wav_16khz
)
from helpers.input_safety import (
    get_path,
    get_positive_number,
    remove_timestamps,
    get_int,
    select_course_code
)
from helpers.process_audio import transcribe_to_file, move_wav_to_lectures, summarize_lecture
from helpers.recorder import Recorder
from helpers.fancy_prints import print_title, print_yellow, print_green


def main():
    """
    The main function to run this program after setup specified in the READ_ME.md

    :return: None
    """
    print_title()
    course_codes = []
    archived_course_codes = []

    # If the notes folder didn't exist create it and populate it with classes
    note_root_path = "notes"
    if create_folder(note_root_path):
        create_folder(path=f"{note_root_path}/archived_classes")
        course_codes += create_class_folders(prompt="How many classes do you have this semester?\n")

    # If notes folder exists but there are only archived classes
    elif len(get_course_codes(root_directory="notes")) == 0:
        course_codes += create_class_folders(prompt="How many classes do you have this semester?\n")

        # Adds a blank line spacer
        print()
    else:
        course_codes += get_course_codes(root_directory="notes")
        archived_course_codes += get_course_codes(root_directory="notes/archived_classes")

    # Display menu
    choice = menu.main()

    match choice:
        case 1:
            record_now(course_codes=course_codes)
        case 2:
            transcribe_from_recording(course_codes=course_codes)
        case 3:
            summarize_from_transcript(course_codes=course_codes)
        case 4:
            view_file(course_codes=course_codes, archived_course_codes=archived_course_codes)
        case 5:
            edit_classes(course_codes=course_codes, archived_course_codes=archived_course_codes)
        case 6:
            print("Goodbye")


def record_now(course_codes):
    """
    Records lecture live then transcribes the audio and creates a summary sheet.
    Has the option to partly transcribe the lecture while the lecture is happening to speed up the process.

    :param List[str] course_codes: All the user's course codes

    :return: None
    """
    current_class, _ = menu.choose_class(course_codes=course_codes)

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

                print(f"You're recording has been transcribed and summarised in notes/{current_class}")

                # Ends loop when user exits
                return


def transcribe_from_recording(course_codes):
    """
    Transcribes and creates a summary sheet based off a lecture recording

    :param List[str] course_codes: All the user's course codes

    :return: None
    """
    current_class, _ = menu.choose_class(course_codes=course_codes)

    while True:

        # Gets the path of the audio to be processed
        lecture_path = get_path(prompt="\nPath of your audio or video file relative to this program: ")
        try:

            # Converts the audio or video file to .wav at 16khz
            wav_path = convert_to_wav_16khz(file_path=lecture_path)

            # Breaks after successful conversion
            break
        except Exception as e:
            supported_file_extensions = [
                # Audio formats
                '.mp3', '.wav', '.flac', '.ogg', '.aac',
                '.m4a', '.wma', '.aiff', '.opus',

                # Video formats
                '.mp4', '.mkv', '.avi', '.mov',
                '.wmv', '.flv', '.webm'
            ]

            # Tells user to use one of the supported file types
            print_yellow("\nError processing file!")
            print("Please use one of the following file extensions:", end=" ")
            for extension in supported_file_extensions:
                print(extension, end=" ")

            # Adds newline
            print()

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


def summarize_from_transcript(course_codes):
    """
    Creates a summary sheet based on a transcript

    :param List[str] course_codes: List of valid course codes

    :return: None
    """
    transcript_path = get_path(prompt="\nTranscript path relative to this program: ")
    course_code = select_course_code(
        prompt=f"Course code: ",
        valid_course_codes=course_codes
    )
    lecture_num = get_positive_number(prompt="Lecture #: ")

    transcript = txt_file_to_str(transcript_path)
    summarize_lecture(transcript=transcript, course_code=course_code, lecture_num=lecture_num)


def view_file(course_codes, archived_course_codes):
    """
    View any summary, transcript, or lecture file

    :param List[str] archived_course_codes: Courses that have been archived
    :param List[str] course_codes: All the user's course codes

    :return: None
    """

    # Get user choices about the media they want to view
    current_class, is_archive = menu.choose_class(course_codes=course_codes, archived_codes=archived_course_codes)
    media_type = menu.select_media_type()

    # Get the filenames from the class and category the user wants to view
    if is_archive:
        files_in_folder = get_files_in_directory(f"notes/archived_classes/{current_class}/{media_type}")
    else:
        files_in_folder = get_files_in_directory(f"notes/{current_class}/{media_type}")

    if len(files_in_folder) == 0:
        print("There are no files here")
        return

    # Gets the user to select the file from their specified media type
    print(f"\nSelect from {media_type}")
    for i, file_name in enumerate(files_in_folder):
        print(f"{i+1}. {file_name}")

    file_num_picked = get_int(lowest_valid=1, highest_valid=len(files_in_folder), prompt="")

    # Open the file picked by the user on any os
    if is_archive:
        file_path = f"notes/archived_classes/{current_class}/{media_type}/{files_in_folder[file_num_picked-1]}"
    else:
        file_path = f"notes/{current_class}/{media_type}/{files_in_folder[file_num_picked - 1]}"

    system = platform.system()

    if system == "Windows":
        os.startfile(file_path)
    elif system == "Darwin":
        subprocess.run(["open", file_path], check=True)
    elif system == "Linux":
        subprocess.run(["xdg-open", file_path], check=True)
    else:
        print(f"Unsupported operating system: {system}")


def edit_classes(course_codes, archived_course_codes):
    """
    Archive or add courses.

    :param List[str] archived_course_codes: Course codes in the archive
    :param List[str] course_codes: Course codes that are currently not archived

    :return: None
    """
    edit_type = menu.edit_class_options()

    match edit_type:
        case "archive":
            print("\nHow many classes would you like to archive?")
            classes_to_archive = get_int(lowest_valid=1, highest_valid=len(course_codes), prompt="")

            # Adds blank line
            print()

            # For every class to archive archives a different course code
            for i in range(classes_to_archive):
                class_to_archive = select_course_code(
                    prompt=f"Course code of class to archive #{i+1}: ",
                    valid_course_codes=course_codes
                )

                # Moves class folder to archived classes
                move_directory(
                    original_path=f"notes/{class_to_archive}",
                    new_path=f"notes/archived_classes/{class_to_archive}"
                )

            print_green("Archive successful!")

        case "add_classes":
            create_class_folders(prompt="\nHow many classes would you like to add?\n")
            print_green("\nClasses added successfully!")

        case "new_semester":

            # Archive every class
            for course in course_codes:

                # Moves class folder to archived classes
                move_directory(
                    original_path=f"notes/{course}",
                    new_path=f"notes/archived_classes/{course}"
                )

            print("All classes archived")

            create_class_folders(prompt="\nHow many classes would you like to add?\n")
            print("Classes added successfully!")

        case "restore_from_archive":
            print("\nHow many classes would you like to restore?")
            classes_to_restore = get_int(lowest_valid=1, highest_valid=len(archived_course_codes), prompt="")

            # Adds blank line
            print()

            # For every class to archive archives a different course code
            for i in range(classes_to_restore):
                class_to_restore = select_course_code(
                    prompt=f"Course code of class to restore #{i + 1}: ",
                    valid_course_codes=archived_course_codes
                )

                # Moves class folder to archived classes
                move_directory(
                    original_path=f"notes/archived_classes/{class_to_restore}",
                    new_path=f"notes/{class_to_restore}"
                )

            print_green("Restore successful!")


main()

