import os
import librosa
import soundfile as sf
import numpy as np

def split_audio_into_chunks(audio_file, chunk_duration_ms=20, overlap_factor=0.5):
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)
    
    # Calculate the duration of each chunk in samples
    chunk_duration_samples = int((chunk_duration_ms / 1000) * sr)
    
    # Calculate the overlap in samples
    overlap_samples = int(chunk_duration_samples * overlap_factor)
    
    # List to store the audio chunks
    chunks = []
    
    start_sample = 0
    chunk_index = 1
    
    # Split the audio into chunks with overlap
    while start_sample < len(y):
        end_sample = start_sample + chunk_duration_samples
        chunk = y[start_sample:end_sample]
        
        chunks.append(chunk)
        
        # Update the index and start sample for the next chunk
        chunk_index += 1
        start_sample = start_sample + chunk_duration_samples - overlap_samples
    
    print(f"Chunks for {audio_file} have been created.")
    
    return chunks, sr  # Return the chunks and the sample rate


def process_dataset(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".wav"):
            file_path = os.path.join(input_dir, filename)
            chunks, sr = split_audio_into_chunks(file_path)  # Get chunks and sample rate

            parent_dir = os.path.basename(os.path.dirname(file_path))
            audio_name = os.path.basename(file_path).split('.')[0]
            specific_output_dir = os.path.join(output_dir, parent_dir, audio_name)
            if not os.path.exists(specific_output_dir):
                os.makedirs(specific_output_dir)

            # Save each chunk to the output directory
            for i, chunk in enumerate(chunks):
                output_file = os.path.join(specific_output_dir, f"{audio_name}_{i+1}.wav")
                sf.write(output_file, chunk, sr)
                print(f"Processed and saved file: {output_file}")


if __name__ == "__main__":
    input_folder = './final_dataset/Control'
    output_folder = './final_dataset_chunks'
    process_dataset(input_folder, output_folder)
