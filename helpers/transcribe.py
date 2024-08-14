import os
import subprocess


def transcribe_audio(wav_file, model_name="medium.en"):
    """
    Transcribes an audio file (.wav) using a specified model and returns the processed string.

    :param str wav_file: Path to the WAV file
    :param str model_name: Name of the model to use

    :return: Transcribed string of the audio file

    :raises: Exception if any error occurs during transcribing
    """

    model = f"modules/whisper.cpp/models/ggml-{model_name}.bin"

    # Check if the whisper model exists
    if not os.path.exists(model):
        raise FileNotFoundError(
            f"Model file not found: {model} \n\nDownload a model with this command:\n\n> bash ./models/download-ggml-model.sh {model_name}\n\n")

    # Check if the wav file exists
    if not os.path.exists(wav_file):
        raise FileNotFoundError(f"WAV file not found: {wav_file}")

    full_command = f"modules/whisper.cpp/main -m {model} -f {wav_file} -np"

    # Execute the command
    process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Get the output and error (if any)
    output, error = process.communicate()

    if error:
        raise Exception(f"Error processing audio: {error.decode('utf-8')}")

    # Process and return the output string
    decoded_str = output.decode('utf-8').strip()
    processed_str = decoded_str.replace('[BLANK_AUDIO]', '').strip()

    return processed_str

