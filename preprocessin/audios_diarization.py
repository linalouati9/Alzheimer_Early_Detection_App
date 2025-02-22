from pyannote.audio import Pipeline
from pydub import AudioSegment
import os

class SpeakerDiarization:
    def __init__(self, pretrained_model="pyannote/speaker-diarization@2.1", auth_token=None, cache_dir=".cache/huggingface"):
        self.pipeline = Pipeline.from_pretrained(pretrained_model, 
                                                 use_auth_token=auth_token, 
                                                 cache_dir=cache_dir)

    def process_audio(self, audio_path, output_dir, num_speakers=2):
        """
        Process a single audio file for speaker diarization and extract dominant speaker's audio.

        :param audio_path: Path to the audio file.
        :param output_dir: Directory to save the output audio file.
        :param num_speakers: Number of speakers to identify.
        """
        # Run the diarization pipeline
        diarization = self.pipeline(audio_path, num_speakers=num_speakers)

        # Calculate speaker durations and identify dominant speaker
        durations = {}
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            durations[speaker] = durations.get(speaker, 0) + (turn.end - turn.start)

        dominant_speaker = max(durations, key=durations.get)
        print(f"Dominant speaker: {dominant_speaker} in {audio_path}")

        # Extract dominant speaker's segments
        audio = AudioSegment.from_wav(audio_path)
        dominant_audio = AudioSegment.silent(duration=0)

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            if speaker == dominant_speaker:
                start = int(turn.start * 1000)  # convert to milliseconds
                end = int(turn.end * 1000)
                dominant_audio += audio[start:end]

        # Save the dominant speaker's audio
        parent_dir = os.path.basename(os.path.dirname(audio_path))
        audio_name = os.path.basename(audio_path).split('.')[0]
        specific_output_dir = os.path.join(output_dir, parent_dir)
        if not os.path.exists(specific_output_dir):
            os.makedirs(specific_output_dir)
        
        output_file = os.path.join(specific_output_dir, f"{audio_name}.wav")
        dominant_audio.export(output_file, format="wav")
        print(f"Saved dominant speaker audio to {output_file}")

    def process_directory(self, input_dir, output_dir, num_speakers=2):
        """
        Process all audio files in a directory for speaker diarization.

        :param input_dir: Directory containing audio files.
        :param output_dir: Directory to save output audio files.
        :param num_speakers: Number of speakers to identify.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for file_name in os.listdir(input_dir):
            if file_name.endswith(".wav"):
                audio_path = os.path.join(input_dir, file_name)
                self.process_audio(audio_path, output_dir, num_speakers=num_speakers)


if __name__ == "__main__":
    auth_token = "YOUR_TOKEN_HERE"
    input_directory = "./dataset/Control/"
    output_directory = "./patient_dataset/"

    diarization_tool = SpeakerDiarization(auth_token=auth_token)
    diarization_tool.process_directory(input_directory, output_directory, num_speakers=2)
