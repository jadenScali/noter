import os
import subprocess
import time
from datetime import datetime
from helpers.file_handler import write_to_file, get_lecture_num, move_and_rename_file
from helpers.input_safety import remove_timestamps, snake_to_title
from helpers.openai_handler import summary_sheet_gpt


def transcribe_audio(wav_path, model_name="medium.en", timed=True):
    """
    Transcribes an audio file (.wav) using a specified model and returns the processed string.

    :param str wav_path: Path to the WAV file
    :param str model_name: Name of the model to use
    :param str timed: Weather or not to display the time it took to transcribe a file

    :return: Transcribed string of the audio file

    :raises: Exception if any error occurs during transcribing
    """

    if timed:
        start_time = time.time()

    model = f"modules/whisper.cpp/models/ggml-{model_name}.bin"

    # Check if the whisper model exists
    if not os.path.exists(model):
        raise FileNotFoundError(
            f"Model file not found: {model} \n\nDownload a model with this command:\n\n> bash ./models/download-ggml-model.sh {model_name}\n\n")

    # Check if the wav file exists
    if not os.path.exists(wav_path):
        raise FileNotFoundError(f"WAV file not found: {wav_path}")

    full_command = f"modules/whisper.cpp/main -m {model} -f {wav_path} -np"

    # Execute the command
    process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Get the output and error (if any)
    output, error = process.communicate()

    if error:
        raise Exception(f"Error processing audio: {error.decode('utf-8')}")

    # Process and return the output string
    decoded_str = output.decode('utf-8').strip()
    processed_str = decoded_str.replace('[BLANK_AUDIO]', '').strip()

    if timed:
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Prints the time in seconds if under a minute and in minutes if over
        if elapsed_time >= 60:
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            print(f"\nTranscribed in {minutes} minutes and {seconds:.2f} seconds")
        else:
            print(f"\nTranscribed in {elapsed_time:.2f} seconds")

    return processed_str


def transcribe_and_summarize(wav_path, course_code):
    """

    :param wav_path:
    :param course_code:
    :return:
    """
    # Transcribing... animation
    print("Transcribing...")
    transcript_raw = transcribe_audio(wav_path=wav_path)

    current_lecture_num = get_lecture_num(course_code=course_code)

    # Get the current date and time
    current_date = datetime.now()

    # Format the date as dd/mm/yyyy
    formatted_date = current_date.strftime("%d/%m/%Y")

    # Adds a header to the transcript and a blank line at the end of the file
    transcript_header = f"Course: {course_code}\nLecture {current_lecture_num}\nDate: {formatted_date}\n\n"
    transcript_timestamped = transcript_header + transcript_raw + '\n'

    # Writes transcript with timestamps to a timestamped .txt file
    transcript_file_name = f"{current_lecture_num}.txt"
    timestamped_path = f"notes/{course_code}/timestamped/{transcript_file_name}"
    write_to_file(file_path=timestamped_path, content=transcript_timestamped)
    print(f"Created {transcript_file_name} in {timestamped_path}")

    # Appends timestamped transcript to the main timestamped transcript for the class including past lectures
    timestamped_main_path = f"notes/{course_code}/timestamped/main.txt"
    write_to_file(file_path=timestamped_main_path, content=transcript_timestamped)
    print(f"Appended to main.txt in {timestamped_main_path}")

    # Converts raw transcript to one without timestamps
    clean_transcript = remove_timestamps(transcript=transcript_timestamped)

    # Writes transcript to .txt file
    transcript_path = f"notes/{course_code}/transcripts/{transcript_file_name}"
    write_to_file(file_path=transcript_path, content=clean_transcript)
    print(f"Created {transcript_file_name} in {transcript_path}")

    # Appends transcript to the main transcript for the class including past lectures
    transcript_path_main_path = f"notes/{course_code}/transcripts/main.txt"
    write_to_file(file_path=transcript_path_main_path, content=clean_transcript)
    print(f"Appended to main.txt in {transcript_path_main_path}")

    # Moving .wav file to lectures folder
    new_directory = f"notes/{course_code}/lectures"
    new_wav_name = f"{current_lecture_num}.wav"
    move_and_rename_file(original_path=wav_path, new_directory=new_directory, new_filename=new_wav_name)
    print(f"Moved {wav_path} to {new_directory} as {new_wav_name}")

    # Creates summary sheet
    transcript_clean_no_header = remove_timestamps(transcript=transcript_raw)
    summarize_lecture(transcript=transcript_clean_no_header, course_code=course_code, lecture_num=current_lecture_num)

    print("\nTranscription successful!")


def summarize_lecture(transcript, course_code, lecture_num):
    """
    Summarizes the lecture from a transcript and creates a .md summary sheet

    :param str transcript: Lecture transcript
    :param str course_code: Code of the lecture class
    :param number lecture_num: The nth lecture

    :return: Creates the summary sheet file
    """
    # Creates a summary sheet and its title based on the transcript
    print("Summarizing...")
    summary_sheet, sheet_title = summary_sheet_gpt(transcript=transcript)

    # Get the current date and time
    current_date = datetime.now()

    # Format the date as dd/mm/yyyy
    formatted_date = current_date.strftime("%d/%m/%Y")

    # Add header to summary_sheet in Markdown
    sheet_header = (
        f"## {snake_to_title(sheet_title)}\n\n"
        f"### Lecture: {course_code}-{lecture_num}\n"
        f"### Date: {formatted_date}\n\n"
        f"---\n\n"
    )
    summary_sheet = sheet_header + summary_sheet + "\n\n"

    # Writes summary_sheet to a .md (Markdown) file
    summary_file_name = f"{lecture_num}-{sheet_title.lower()}.md"
    summary_path = f"notes/{course_code}/summaries/{summary_file_name}"
    write_to_file(file_path=summary_path, content=summary_sheet)
    print(f"Created {summary_file_name} in {summary_path}")

    # Appends summary_sheet to the main summary_sheet for the class including past lectures
    summary_main_path = f"notes/{course_code}/summaries/main.md"
    write_to_file(file_path=summary_main_path, content=summary_sheet)
    print(f"Appended to main.md in {summary_main_path}")
