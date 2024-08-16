import sounddevice as sd
import wave
import threading


class Recorder:
    """
    A class to handle audio recording from the microphone to a .wav file at a samplerate Whisper can read.
    """
    def __init__(self, file_path, channels=1, samplerate=16000):
        """
        Initializes the Recorder with the given file_path, channels, and sample rate.

        :param str file_path: The name of the output .wav file
        :param int, optional channels: The channels, defaults to 1 as that's what Whisper supports
        :param int, optional samplerate: The samplerate of the audio, defaults to 16000 as that's what Whisper supports

        :return: None
        """
        self.file_path = file_path
        self.channels = channels
        self.samplerate = samplerate
        self.is_recording = False
        self._stream = None


    def _callback(self, indata, status):
        """
        Internal callback function to handle real-time audio data.

        This function is called automatically by the sounddevice.InputStream
        to process and save the incoming audio data to the .wav file.

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
            callback=self._callback
        )


        # Start the recording in a separate thread
        def record():
            with self._stream:
                while self.is_recording:
                    sd.sleep(1000)


        self._recording_thread = threading.Thread(target=record)
        self._recording_thread.start()
        print(f"Recording live... Saving to {self.file_path}")


    def stop_recording(self):
        """
        Stops recording audio and finalizes the .wav file.

        :return: None
        """
        self.is_recording = False

        # Wait for the recording thread to finish
        self._recording_thread.join()
        self._wav_file.close()
        print("Recording stopped")

