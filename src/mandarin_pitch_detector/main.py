"""A pitch detector developer for Mandarin Chinese."""

import crepe
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import matplotlib.cm
from imageio import imwrite
import pandas as pd
import numpy as np
from mandarin_pitch_detector.visualization import (
    save_activation_plot,
    save_audio_plot,
    save_frequency_plot)

def get_groups_from_ndarray(time: np.ndarray, frequency: np.ndarray, confidence: np.ndarray, threshold_confidence: float, min_duration: float) -> list:

    chunks = []

    start_idx = None

    for i in range(len(confidence)):
        if confidence[i] > threshold_confidence:
            if start_idx is None:
                start_idx = i  # Start of new high-confidence segment
        else:
            if start_idx is not None:
                # End of high-confidence segment
                end_idx = i
                t_chunk = time[start_idx:end_idx]
                if t_chunk[-1] - t_chunk[0] > min_duration:
                    chunks.append((
                        t_chunk,
                        frequency[start_idx:end_idx],
                        confidence[start_idx:end_idx]
                    ))
                start_idx = None  # Reset

    # Handle case where sequence continues till the end
    if start_idx is not None:
        t_chunk = time[start_idx:]
        if t_chunk[-1] - t_chunk[0] > min_duration:
            chunks.append((
                t_chunk,
                frequency[start_idx:],
                confidence[start_idx:]
            ))


    print(f"Number of valid chunks: {len(chunks)}")
    for i, (t, f, c) in enumerate(chunks):
        print(f"\nChunk {i+1}:")
        print("Time:", t)
        print("Frequency:", f)
        print("Confidence:", c)

    return chunks

def save_to_csv(time: np.ndarray, frequency: np.ndarray, confidence: np.ndarray, file: str):
    """
    Save time, frequency, and confidence arrays to a CSV file.

    Parameters:
    - time (np.ndarray): 1D array of time values
    - frequency (np.ndarray): 1D array of frequency values
    - confidence (np.ndarray): 1D array of confidence values
    - given_file_path_name (str): Path to save the CSV file
    """
    # Check that all arrays have the same length
    if not (len(time) == len(frequency) == len(confidence)):
        raise ValueError("All input arrays must have the same length")

    data = np.column_stack((time, frequency, confidence))
    header = "time,frequency,confidence"
    np.savetxt(file, data, delimiter=",", header=header, comments='', fmt='%.10f')
    print(f"Saved to file {file}")

def read_from_csv(file: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Reads a CSV file with columns time, frequency, and confidence,
    and returns them as three separate NumPy arrays.

    Parameters:
    - given_file_path_name (str): Path to the CSV file

    Returns:
    - time (np.ndarray)
    - frequency (np.ndarray)
    - confidence (np.ndarray)
    """
    # Load data, skipping the header
    data = np.loadtxt(file, delimiter=",", skiprows=1)

    # Split columns into separate arrays
    time = data[:, 0]
    frequency = data[:, 1]
    confidence = data[:, 2]

    return time, frequency, confidence


if __name__ == "__main__":
    sr, audio = wavfile.read('data/mandarinTones.wav')
    time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)
    save_audio_plot(audio, "data/audio.png")
    save_to_csv(time, frequency, confidence, 'data/time_freq_confidence.csv')
    save_activation_plot(activation, "data/activation.png")
    save_frequency_plot(frequency, "data/frequency.png")
    

    time, frequency, confidence = read_from_csv('data/time_freq_confidence.csv')
    chunks = get_groups_from_ndarray(time, frequency, confidence, threshold_confidence=0.8, min_duration=0.15)
