import os
import librosa
import soundfile as sf
import numpy as np
from audios_median_length import calculate_median_length

def normalize_audio(audio_signal):
    """
    Normalize the amplitude of an audio signal to the range [-1, 1].    
    :param audio_signal: numpy array, raw audio signal
    :return: numpy array, audio signal normalized to the range [-1, 1]
    """
    if audio_signal.size == 0:  # Check for empty signal
        raise ValueError("Empty audio signal encountered.")
        
    max_amplitude = np.max(np.abs(audio_signal))
    if max_amplitude > 1:
        normalized_signal = audio_signal / max_amplitude
    else:
        normalized_signal = audio_signal
    return normalized_signal

def process_dataset(input_dir, output_dir, target_sample_rate=44100):
    """
    Normalize all audio files in a dataset by adjusting their amplitude and length.
    
    :param input_dir: str, path to the directory containing the original audio files
    :param output_dir: str, path to the directory where processed audio files will be saved
    :param target_sample_rate: int, target sampling rate for all audio files (default is 44100 Hz)
    """
    os.makedirs(output_dir, exist_ok=True)

    # Calculate the median duration
    median_length = calculate_median_length()
    
    if np.isnan(median_length):
        print("Cannot proceed, no valid audio files with duration found.")
        return

    print(f"Median duration: {median_length:.2f} seconds")

    # Process each audio file
    for filename in os.listdir(input_dir):
        if filename.endswith(".wav"):
            file_path = os.path.join(input_dir, filename)
            
            try:
                # Load the audio file
                audio_signal, sr = librosa.load(file_path, sr=target_sample_rate)
                
                # Skip empty or silent audio files
                if audio_signal.size == 0 or np.max(np.abs(audio_signal)) == 0:
                    print(f"Warning: {filename} is empty or silent, skipping.")
                    continue

                # Normalize the audio signal
                normalized_signal = normalize_audio(audio_signal)

                # Adjust the length to the median duration
                current_length = len(audio_signal) / sr
                stretch_factor = median_length / current_length
                stretched_signal = librosa.effects.time_stretch(normalized_signal, rate=stretch_factor)

                # Save the processed audio file
                parent_dir = os.path.basename(os.path.dirname(file_path))  # Fix: Use file_path
                audio_name = os.path.basename(file_path).split('.')[0]
                specific_output_dir = os.path.join(output_dir, parent_dir)
                if not os.path.exists(specific_output_dir):
                    os.makedirs(specific_output_dir)
                
                output_file = os.path.join(specific_output_dir, f"{audio_name}.wav")  # Fix: Use output_file
                sf.write(output_file, stretched_signal, sr)  # Fix: Use output_file
                print(f"Processed and saved file: {output_file}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__": 
    input_directory = "./patient_dataset_without_silence/Control"
    output_directory = "./final_dataset"

    process_dataset(input_directory, output_directory)
