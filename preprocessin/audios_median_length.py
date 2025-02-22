import os
import numpy as np
import librosa

def calculate_median_length(input_dir="./dataset", target_sample_rate=44100):
    """
    Calculate the median duration of audio files in a dataset.
    Recursively processes all subdirectories.
    Skips empty or silent files.
    
    :param input_dir: str, path to the directory containing the audio files
    :param target_sample_rate: int, target sampling rate for all audio files (default is 44100 Hz)
    :return: float, median duration in seconds
    """
    lengths = []
    
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith(".wav"):
                file_path = os.path.join(root, filename)
                try:
                    # Load the audio file
                    audio_signal, sr = librosa.load(file_path, sr=target_sample_rate)
                    
                    # Skip empty or silent audio files
                    if audio_signal.size == 0 or np.max(np.abs(audio_signal)) == 0:
                        print(f"Warning: {filename} is empty or silent, skipping.")
                        continue
                    
                    # Append the duration of the file (length in seconds)
                    lengths.append(len(audio_signal) / sr)
                except Exception as e:
                    print(f"Error loading {filename} in {root}: {e}")
    
    # Compute the median duration
    if lengths:
        return np.median(lengths)
    else:
        print("No valid audio files found.")
        return float('nan')
