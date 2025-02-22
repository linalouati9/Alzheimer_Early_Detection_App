import webrtcvad
import wave
import numpy as np
from pydub import AudioSegment
import os


class SpeechProcessor:
    def __init__(self, aggressiveness=3):
        """
        Initialize the SpeechProcessor with a given aggressiveness level.
        :param aggressiveness: Level of aggressiveness (0 to 3).
        """
        self.vad = webrtcvad.Vad(aggressiveness)

    @staticmethod
    def read_wave(file):
        """
        Read a WAV file and return its frames and sample rate.
        :param file: Path to the WAV file.
        :return: Tuple (audio data, sample_rate).
        """
        with wave.open(file, 'rb') as wf:
            if wf.getsampwidth() != 2:
                raise ValueError("Only 16-bit WAV PCM files are supported.")
            if wf.getnchannels() != 1:
                raise ValueError("Only mono audio is supported.")
            sample_rate = wf.getframerate()
            frames = wf.readframes(wf.getnframes())
            return frames, sample_rate

    @staticmethod
    def frame_generator(frame_duration_ms, audio, sample_rate):
        """
        Generate audio frames of a specified duration.
        :param frame_duration_ms: Duration of each frame in milliseconds.
        :param audio: Audio data.
        :param sample_rate: Sample rate of the audio.
        :return: Generator yielding audio frames.
        """
        frame_size = int(sample_rate * frame_duration_ms / 1000) * 2  # 2 bytes per sample
        for i in range(0, len(audio) - frame_size + 1, frame_size):
            yield audio[i:i + frame_size]

    def remove_silence(self, input_dir, output_dir):
        """
        Remove silence from all audio files in the specified directory and save the result in a structured directory.
        :param input_dir: Directory containing WAV audio files.
        :param output_dir: Base directory where processed audio files will be saved.
        """
        for file_name in os.listdir(input_dir):
            if file_name.endswith(".wav"):
                file_path = os.path.join(input_dir, file_name)
                print(f"Processing {file_name}...")

                # Read and process the audio file
                audio, sample_rate = self.read_wave(file_path)
                
                # Resample if necessary
                if sample_rate not in [8000, 16000, 32000, 48000]:
                    print(f"Resampling {file_name} from {sample_rate} Hz to 16000 Hz...")
                    audio_segment = AudioSegment.from_wav(file_path)
                    audio_segment = audio_segment.set_frame_rate(16000).set_channels(1)
                    sample_rate = 16000
                    audio = audio_segment.raw_data
                
                frames = list(self.frame_generator(30, audio, sample_rate))  # 30 ms per frame
                
                # Detect speech frames
                speech_frames = [
                    frame for frame in frames if self.vad.is_speech(frame, sample_rate)
                ]

                # Combine speech frames into a single audio segment
                speech_audio = b"".join(speech_frames)

                # Save the resulting audio
                parent_dir = os.path.basename(os.path.dirname(file_path))
                audio_name = os.path.splitext(file_name)[0]
                specific_output_dir = os.path.join(output_dir, parent_dir)
                os.makedirs(specific_output_dir, exist_ok=True)
                
                output_path = os.path.join(specific_output_dir, f"{audio_name}.wav")
                with wave.open(output_path, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)  # 16-bit audio
                    wf.setframerate(sample_rate)
                    wf.writeframes(speech_audio)
                
                print(f"Saved processed audio to {output_path}")


if __name__ == "__main__":
    # input_directory = "./patient_dataset/Dementia"
    input_directory = "./patient_dataset/Control"
    output_directory = "./patient_dataset_without_silence"
    
    processor = SpeechProcessor(aggressiveness=3)
    processor.remove_silence(input_directory, output_directory)
