import sounddevice as sd
import wave
import threading
from pydub import AudioSegment
from helpers.fancy_prints import print_red


def get_supported_sample_rate():
    """
    Returns the supported sample rate for the user's default microphone.

    :return int: Supported sample rate
    """
    device_info = sd.query_devices(kind='input')

    return int(sd.query_devices(device_info['index'], 'input')['default_samplerate'])


class Recorder:
    """
    A class to handle audio recording from the microphone to a .wav file at a samplerate Whisper can read.
    """
    def __init__(self, file_path, channels=1):
        """
        Initializes the Recorder with the given file_path, channels, and sample rate.

        :param str file_path: The name of the output .wav file
        :param int channels: The channels, defaults to 1 as that's what Whisper supports

        :return: None
        """
        self.file_path = file_path
        self.channels = channels
        self.samplerate = get_supported_sample_rate()
        self.block_size = self.get_optimal_block_size(self.samplerate)
        self.is_recording = False
        self._stream = None


    def get_optimal_block_size(self, samplerate):
        """
        Returns an optimal block size for the given sample rate.

        :param int samplerate: The sample rate of the audio

        :return int: Optimal block size
        """
        block_sizes = [256, 512, 1024, 2048]
        for size in block_sizes:
            try:
                with sd.InputStream(samplerate=samplerate, channels=self.channels, blocksize=size):
                    return size
            except Exception as e:
                print(f"Block size {size} failed: {e}")

        # Fallback to a default value
        return 1024


    def _callback(self, indata, frames, time, status):
        """
        Internal callback function to handle real-time audio data.

        This function is called automatically by the sounddevice.InputStream
        to process and save the incoming audio data to the .wav file.

        Note: Frames and time are side effects of InputStream callback and not used

        :param numpy.ndarray indata: Raw audio data captured from the mic as a chunk
        :param sounddevice.CallbackFlags status: Status flags indicating the state of the stream (e.g., errors)

        :return: None
        """
        if status:
            print(status)
        self._wav_file.writeframes(indata.copy())


    def start_recording(self):
        """
        Starts the audio recording and saves the data to the specified .wav file.

        :return: None
        """
        self.is_recording = True
        self._wav_file = wave.open(self.file_path, 'wb')
        self._wav_file.setnchannels(self.channels)
        self._wav_file.setsampwidth(2)
        self._wav_file.setframerate(self.samplerate)

        self._stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            callback=self._callback,
            blocksize=self.block_size,
            dtype = 'int16'
        )


        # Start the recording in a separate thread
        def record():
            with self._stream:
                while self.is_recording:
                    sd.sleep(1000)


        self._recording_thread = threading.Thread(target=record)
        self._recording_thread.start()
        print_red(f"\nRecording live...")


    def convert_to_16khz(self):
        """
        Converts the recorded .wav file to a 16 kHz sample rate.

        :return: None
        """
        audio = AudioSegment.from_wav(self.file_path)

        # Resample to 16 kHz
        if audio.frame_rate != 16000:
            audio = audio.set_frame_rate(16000)

        # Save the resampled audio back to the file
        audio.export(self.file_path, format="wav")


    def stop_recording(self):
        """
        Stops recording audio and finalizes the .wav file.

        :return: None
        """
        self.is_recording = False

        # Wait for the recording thread to finish
        self._recording_thread.join()
        self._wav_file.close()
        self.convert_to_16khz()
        print_red("Recording stopped")

