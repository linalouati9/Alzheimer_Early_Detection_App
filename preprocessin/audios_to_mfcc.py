import os
import librosa
import numpy as np

# Generate MFCC features from audio files
def generate_mfcc_images(input_dir, target_chunk_length=882, n_mfcc=13, n_fft=128): # 882 samples (which corresponds to 20ms at a sample rate of 44.1 kHz)
    data = []
    for folder in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, folder)

        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith('.wav'):
                    file_path = os.path.join(folder_path, file)
                    
                    # Load audio file
                    chunk, sr = librosa.load(file_path, sr=None)
                    
                    # Pad or truncate the chunk to match the target length
                    if len(chunk) < target_chunk_length:
                        chunk = np.pad(chunk, (0, target_chunk_length - len(chunk)), mode='constant')
                    else:
                        chunk = chunk[:target_chunk_length]

                    print(f"Processing {file_path}: {len(chunk)} samples after padding/truncating")

                    # Extract MFCC features
                    mfcc = librosa.feature.mfcc(y=chunk, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft)
                    data.append(mfcc)
    
    return np.array(data)

if __name__ == "__main__":
    # Generate features for the Dementia dataset
    X_dementia = generate_mfcc_images("./final_dataset_chunks/Dementia")
    y_dementia = np.ones(len(X_dementia))

    # Generate features for the Control dataset
    X_control = generate_mfcc_images("./final_dataset_chunks/Control")
    y_control = np.zeros(len(X_control))

    # Combine the datasets
    X = np.concatenate((X_dementia, X_control), axis=0)
    y = np.concatenate((y_dementia, y_control), axis=0)

    # Save the datasets
    np.savez("X.npz", X)
    np.savez("y.npz", y)
