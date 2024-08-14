from helpers.transcribe import transcribe_audio
from helpers.file_handler import write_to_file
import time


def main():
    """
    The main function to run this program after setup specified in the READ_ME.md

    :return: None
    """
    start_time = time.time()

    transcript_raw = transcribe_audio(wav_file="rick_proper.wav")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Transcription Result:", transcript_raw)
    print(f"Time taken: {elapsed_time:.2f} seconds")

    write_to_file(filename="test.txt", content=transcript_raw)


main()

