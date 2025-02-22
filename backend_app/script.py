import librosa
import numpy as np
from pedalboard import Pedalboard, NoiseGate, Compressor, LowShelfFilter, Gain
import tensorflow as tf
import noisereduce as nr

# Pedalboard effect pipeline
def get_pedalboard():
    return Pedalboard([
        NoiseGate(threshold_db=-30, ratio=1.5, release_ms=250),
        Compressor(threshold_db=-16, ratio=4),
        LowShelfFilter(cutoff_frequency_hz=400, gain_db=10, q=1),
        Gain(gain_db=2)
    ])


# Noise reduction and applying effects using Pedalboard
def process_audio_file(y, sr):

    # Select a noise profile from the first 0.5 seconds
    noise_sample = y[:int(sr * 0.5)]  # First 0.5 seconds as noise profile
    reduced_noise = nr.reduce_noise(y=y, sr=sr, y_noise=noise_sample, prop_decrease=0.9)

    # Apply pedalboard effects
    board = get_pedalboard()
    effected = board(reduced_noise, sr)

    return effected, sr


def normalize_amplitude_audio(audio_signal):
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

def adjust_audio_length(audio_signal, target_length, sr):
    """
    Adjust the length of an audio signal to the target length.
    :param audio_signal: numpy array, the raw audio signal
    :param target_length: float, the target length in seconds
    :param sr: int, sample rate of the audio
    :return: numpy array, the adjusted audio signal
    """
    current_length = len(audio_signal) / sr
    if current_length < target_length:
        # If audio is too short, pad with zeros
        target_samples = int(target_length * sr)
        padded_signal = np.pad(audio_signal, (0, target_samples - len(audio_signal)), mode='constant')
        return padded_signal
    else:
        # If audio is too long, truncate it
        target_samples = int(target_length * sr)
        truncated_signal = audio_signal[:target_samples]
        return truncated_signal

def normalise_audio(audio_signal, sr, target_sample_rate=44100, median_length=63.29469387755102):
    """
    Process an audio signal: normalize, stretch, and adjust its duration.

    :param audio_signal: numpy array, raw audio signal
    :param sr: int, sample rate of the audio signal
    :param target_sample_rate: int, target sampling rate for processing (default is 44100 Hz)
    :param median_length: float, median duration of the audio files in seconds
    :return: Processed audio signal (stretched and normalized)
    """
    try:
        # Ensure the sample rate matches the target sample rate
        if sr != target_sample_rate:
            audio_signal = librosa.resample(audio_signal, orig_sr=sr, target_sr=target_sample_rate)
            sr = target_sample_rate

        # Normalize the audio signal
        normalized_signal = normalize_amplitude_audio(audio_signal)
        
        # Adjust the length to the robust median duration (padding or truncating)
        adjusted_signal = adjust_audio_length(normalized_signal, median_length, sr)

        
        return adjusted_signal, sr

    except Exception as e:
        print(f"Error processing audio: {e}")
        return None

# Function to split audio into chunks
def split_audio_into_chunks(y, sr, chunk_duration_ms=20, overlap_factor=0.5):

    # Calculate the duration of each chunk in samples
    chunk_duration_samples = int((chunk_duration_ms / 1000) * sr)

    # Calculate the overlap in samples
    overlap_samples = int(chunk_duration_samples * overlap_factor)

    # List to store the audio chunks
    chunks = []
    start_sample = 0

    while start_sample < len(y):
        end_sample = start_sample + chunk_duration_samples
        chunk = y[start_sample:end_sample]
        chunks.append(chunk)
        start_sample = start_sample + chunk_duration_samples - overlap_samples

    return chunks, sr


# Generate MFCC features from audio chunks
def generate_mfcc_images(chunks, sr, target_chunk_length=882, n_mfcc=13, n_fft=128):
    mfcc_features = []
    for chunk in chunks :
        # Pad or truncate the chunk to match the target length
        if len(chunk) < target_chunk_length:
            chunk = np.pad(chunk, (0, target_chunk_length - len(chunk)), mode='constant')
        else:
            chunk = chunk[:target_chunk_length]

        # Extract MFCC features
        mfcc = librosa.feature.mfcc(y=chunk, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft)
        mfcc_features.append(mfcc)

    # Concatenate all MFCCs along the time axis
    if mfcc_features:
        concatenated_mfcc = np.concatenate(mfcc_features, axis=1)  # Concatenate along the time axis
    else:
        raise ValueError("No chunks available for MFCC extraction.")

    return concatenated_mfcc

# Run MFCC data on TFLite model for inference
def run_inference_on_tflite_model(mfcc_data, tflite_model_path='./best_model.tflite'):
    # Load the TFLite model
    interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
    interpreter.allocate_tensors()

    # Get input and output tensor details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Prepare MFCC data for inference
    input_data = np.expand_dims(mfcc_data, axis=0).astype(np.float32)  # Add batch dimension

    # Run inference
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Get the result
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # The output is the model's prediction (e.g., class probabilities)
    return output_data


# Main pipeline function to process all audio files
def process_audio_pipeline(file_path):
    try:
        # Load audio file (y = audio signal, sr = sample rate)
        y, sr = librosa.load(file_path, sr=None)

        # Step 1: Process the audio file (e.g., noise reduction and applying effects)
        effected_audio, sr = process_audio_file(y, sr)
        
        # Step 2: Remove silence from the audio (using WebRTC VAD)
        trimmed_audio, _ = librosa.effects.trim(effected_audio)

        # Step 3: Normalize the audio and adjust its duration
        normalised_audio, sr = normalise_audio(trimmed_audio, sr)

        # Step 4: Split the audio into chunks for feature extraction
        chunks, sr = split_audio_into_chunks(normalised_audio, sr)

        # Step 5: Generate MFCC (Mel Frequency Cepstral Coefficients) features from audio chunks
        mfcc_data = generate_mfcc_images(chunks, sr)

        # Step 6: Run the MFCC data through the TFLite model for inference (classification or regression)
        predictions = run_inference_on_tflite_model(mfcc_data.T)
        print(f"Inference for {file_path} completed, predictions: {predictions}")

        return(predictions)

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
