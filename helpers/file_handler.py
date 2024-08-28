import os
import shutil
import re
from pydub import AudioSegment
from helpers.fancy_prints import print_green
from helpers.input_safety import get_int, get_filename
from datetime import timedelta
from natsort import natsorted
from moviepy.editor import VideoFileClip


def write_to_file(file_path, content):
    """
    Appends the given text to a file with the specified file_path.
    If the file does not exist, it will be created.

    :param str file_path: The name of the file to write to (including the .txt extension) with its location (ie a path)
    :param str content: The text to write into the file

    :return: None
    """
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(content)


def create_class_folders(prompt):
    """
    Creates the folders and subfolders for each class only if they do not already exist.
    Each class will get a transcripts, summaries and timestamped folder.

    :param str prompt: The message shown to the user before taking input

    :return: List[str] class names user entered
    """
    class_count = get_int(lowest_valid=1, prompt=prompt)
    course_codes = []

    # Adds a blank line
    print()

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
    If it already exists but is empty it will return True.

    :param str path: The path of the folder

    :return bool: Weather or not a folder was created
    """
    if not os.path.exists(path):
        os.mkdir(path)
        return True
    elif os.path.exists(path) and len(os.listdir(path)) == 0:
        return True

    return False


def get_course_codes(root_directory, ignore_directories=None):
    """
    Returns a list of folder names in the root directory.

    :param List[str] ignore_directories: A list of folders to ignore
    :param str root_directory: The directory to search

    :return List[str]: List of folder names aka course_codes
    """
    if ignore_directories is None:
        ignore_directories = [f"{root_directory}/archived_classes"]

    folder_names = []

    # Iterate through the entries in the notes folder
    for entry in os.listdir(root_directory):

        # Create the full path for each entry
        full_path = os.path.join(root_directory, entry)

        # Check if the entry is a directory
        if os.path.isdir(full_path) and full_path not in ignore_directories:
            folder_names.append(entry)

    return folder_names


def get_lecture_num(course_code):
    """
    Goes into the timestamped folder for course_code and finds the next lecture number.

    :param str course_code: Directory name in /notes

    :return str: Next lecture number
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


def get_cut_path(current_class, lecture_num, n):
    """
    Generates the path of the cut .wav file

    :param lecture_num:
    :param str current_class: Class code
    :param int n: The nth cut .wav file

    :return str: The path of the cut .wav file
    """
    return f"notes/{current_class}/lectures/{lecture_num}-_-CUT_{n}-_-.wav"


def move_and_rename_file(original_path, new_directory, new_filename):
    """
    Moves a file and renames it.

    :param str original_path: The original file path
    :param str new_directory: The new directory
    :param str new_filename: The new filename

    :return str: New path of the file
    """

    # Ensure the new directory exists
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)

    # Create the new file path with the new filename
    new_path = os.path.join(new_directory, new_filename)

    # Move and rename the file
    shutil.move(original_path, new_path)

    return new_path


def txt_file_to_str(file_path):
    """
    Converts the content of a .txt file to a string.

    :param str file_path: Path to the .txt file

    :return str: The content of the file or None if file doesn't exist
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return None


def merge_cut_audio_files(course_code, lecture_num):
    """
    Merges all files matching the pattern {lecture_num}-_-CUT_{n}-_-.wav into a single {lecture_num}.wav file.

    :param str course_code: Code of the lecture class
    :param Union[int, float] lecture_num: The nth lecture

    :return str: The audio file path or None if no files exist
    """

    # Define the regex pattern to match {i}-_-CUT_{n}-_-.wav files
    pattern = re.compile(rf'^{lecture_num}-_-CUT_(\d+)-_-.wav$')

    # Dictionary to hold cut .wav files
    files_to_merge = []

    # Iterate over files in the directory
    directory = f"notes/{course_code}/lectures"
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            cut_number = int(match.group(1))
            files_to_merge.append((cut_number, filename))

    # Check if there are files to merge
    if files_to_merge:

        # Sort the files by the cut number (n)
        files_to_merge.sort(key=lambda x: x[0])

        # Load and concatenate audio files
        combined = AudioSegment.empty()
        for _, filename in files_to_merge:
            file_path = os.path.join(directory, filename)
            audio = AudioSegment.from_wav(file_path)
            combined += audio

        # Export the combined audio to a single file
        output_path = os.path.join(directory, f"{lecture_num}.wav")
        combined.export(output_path, format="wav")
        print(f"Merged files into {output_path}")

        # Delete the original cut files
        for _, filename in files_to_merge:
            file_path = os.path.join(directory, filename)
            os.remove(file_path)

        return output_path
    else:
        print(f"No files found for base file number {lecture_num}")
        return None


def add_time_to_timestamps(timestamped_transcript, time_to_add):
    """
    Adds a constant amount of time to all timestamps in the format [hh:mm:ss.sss --> hh:mm:ss.sss] within a str.

    :param str timestamped_transcript: The input string containing the timestamps and dialogue
    :param float time_to_add: The amount of time in seconds to add to each timestamp

    :return str: The modified string with updated timestamps
    """

    # Regular expression pattern to match timestamps [hh:mm:ss.sss --> hh:mm:ss.sss]
    pattern = r'\[(\d{2}):(\d{2}):(\d{2}\.\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}\.\d{3})\]'

    def add_time(match):
        """
        Adds time to the matched timestamp and returns the new timestamp.

        :param re.Match match: The matched timestamp

        :return str: Updated timestamp
        """

        # Parse start time
        start_hour, start_minute, start_second = int(match.group(1)), int(match.group(2)), float(match.group(3))
        start_time = timedelta(hours=start_hour, minutes=start_minute, seconds=start_second)

        # Parse end time
        end_hour, end_minute, end_second = int(match.group(4)), int(match.group(5)), float(match.group(6))
        end_time = timedelta(hours=end_hour, minutes=end_minute, seconds=end_second)

        # Add time to both start and end times
        new_start_time = start_time + timedelta(seconds=time_to_add)
        new_end_time = end_time + timedelta(seconds=time_to_add)

        # Format the new times back to [hh:mm:ss.sss]
        new_start_str = f"{str(int(new_start_time.total_seconds() // 3600)).zfill(2)}:" \
                        f"{str(int((new_start_time.total_seconds() % 3600) // 60)).zfill(2)}:" \
                        f"{'{:06.3f}'.format(new_start_time.total_seconds() % 60)}"

        new_end_str = f"{str(int(new_end_time.total_seconds() // 3600)).zfill(2)}:" \
                      f"{str(int((new_end_time.total_seconds() % 3600) // 60)).zfill(2)}:" \
                      f"{'{:06.3f}'.format(new_end_time.total_seconds() % 60)}"

        return f"[{new_start_str} --> {new_end_str}]"

    # Replace the timestamps in the text
    modified_text = re.sub(pattern, add_time, timestamped_transcript)

    return modified_text


def get_transcript_end_time(transcript_raw):
    """
    Extracts the latest end time from a timestamped transcript.

    :param str transcript_raw: The input string containing the timestamps and dialogue

    :return float: The latest end time in timedelta
    """
    pattern = r'\[(\d{2}):(\d{2}):(\d{2}\.\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}\.\d{3})\]'

    latest_end_time = timedelta()

    for match in re.finditer(pattern, transcript_raw):

        # Parse end time
        end_hour, end_minute, end_second = int(match.group(4)), int(match.group(5)), float(match.group(6))
        end_time = timedelta(hours=end_hour, minutes=end_minute, seconds=end_second)

        # Update the latest end time if this one is later
        if end_time > latest_end_time:
            latest_end_time = end_time

    return latest_end_time.total_seconds()


def rename_wav_file(original_path, new_name):
    """
    Renames a .wav file to a new name while keeping the same directory.

    :param str original_path: The full path to the original .wav file
    :param str new_name: The new name for the .wav file (without the extension)

    :return str: The new str path to the renamed .wav file
    """

    # Ensure the file is a .wav file
    if not original_path.lower().endswith(".wav"):
        raise ValueError("The provided file is not a .wav file.")

    # Get the directory of the original file
    directory = os.path.dirname(original_path)

    # Create the new file path with the new name
    new_path = os.path.join(directory, f"{new_name}.wav")

    # Rename the file
    os.rename(original_path, new_path)

    return new_path


def compress_wav_to_mp3(wav_file_path, bit_rate="128k"):
    """
    Compresses a .wav file by converting it to a .mp3 file, prints the percentage of compression,
    and then deletes the original .wav file.

    :param str wav_file_path: Path to the .wav file
    :param str bit_rate: Bit-rate for the .mp3 file (default is 192k)

    :return str: Path to the compressed .mp3 file
    """
    print_green("\nCompressing...")

    # Ensure the file is a .wav file
    print("Checking .wav")
    if not wav_file_path.lower().endswith(".wav"):
        raise ValueError("The provided file is not a .wav file.")

    # Get the size of the original .wav file
    original_size = os.path.getsize(wav_file_path)

    # Load the .wav file
    audio = AudioSegment.from_wav(wav_file_path)

    # Define the output .mp3 file path
    mp3_file_path = wav_file_path.replace(".wav", ".mp3")

    # Export the audio as an .mp3 file
    audio.export(mp3_file_path, format="mp3", bitrate=bit_rate)
    print("Converted to .mp3")

    # Get the size of the compressed .mp3 file
    compressed_size = os.path.getsize(mp3_file_path)

    # Calculate the percentage of compression
    compression_percentage = ((original_size - compressed_size) / original_size) * 100

    # Print the percentage of compression
    print(f"Compression saved {compression_percentage:.2f}% space")

    # Delete the original .wav file
    os.remove(wav_file_path)

    print_green("\nCompression successful!")

    return mp3_file_path


def convert_to_wav_16khz(file_path):
    """
    Converts any audio or video file to a .wav file at a 16 kHz sample rate.
    Deletes the original file after conversion if it's an audio file, but keeps the original file if it's a video.
    Supports: .mp3, .wav, .flac, .ogg, .acc, .m4a, .wma, .aiff, .opus, .mp4, .mkv, .avi, .mov, .wmv, .flv and .webm

    :param str file_path: Path to the input audio or video file (e.g., .mp3, .mp4, .flac)

    :return str: Path to the converted .wav file
    """
    if not os.path.exists(file_path):
        raise ValueError("The provided file path does not exist.")

    # Determine the file extension
    file_ext = os.path.splitext(file_path)[1].lower()

    is_video = False

    if file_ext in ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm']:
        is_video = True

        # Extract audio from video file using moviepy
        with VideoFileClip(file_path) as video:
            audio = video.audio

            # Save the extracted audio as a temporary file
            temp_audio_path = "temp_audio.mp3"
            audio.write_audiofile(temp_audio_path)
            file_path = temp_audio_path

    # Load the audio file (either from video or directly)
    audio = AudioSegment.from_file(file_path)

    # Set the output file path to be the same as input but with .wav extension
    output_file_path = os.path.splitext(file_path)[0] + ".wav"

    # Export the audio as a .wav file with a 16 kHz sample rate
    audio.set_frame_rate(16000).export(output_file_path, format="wav")

    # Remove the original audio file if it wasn't a video or a .wav
    if not is_video and file_ext != '.wav':
        os.remove(file_path)
    else:
        # Remove the temporary audio file if created
        if os.path.exists("temp_audio.mp3"):
            os.remove("temp_audio.mp3")

    print("Converted to .wav")
    return output_file_path


def get_files_in_directory(directory_path):
    """
    Returns a list of filenames within the given directory.

    :param str directory_path: The path to the directory

    :return list[str]: A list of filenames in the directory
    """

    # Check if the provided path is a valid directory
    if not os.path.isdir(directory_path):
        raise ValueError(f"The provided path '{directory_path}' is not a valid directory.")

    # Get the list of filenames in the directory
    filenames = os.listdir(directory_path)

    # Sort the filenames naturally ie numbers in increasing order and then alphabetically
    filenames = natsorted(filenames)

    return filenames


def move_directory(original_path, new_path):
    """
    Moves a directory to a new location.

    :param str original_path: The original directory path
    :param str new_path: The new str directory path

    :return str: New path to folder
    """

    # Ensure the parent directory exists, create it if it doesn't
    parent_directory = os.path.dirname(new_path)
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)

    # If the new directory already exists, add a suffix to the filename
    suffix = 1
    base_path = new_path

    while os.path.exists(new_path):
        suffix += 1
        new_path = f"{base_path}_{suffix}"

    # Move the directory
    shutil.move(original_path, new_path)

    return new_path

