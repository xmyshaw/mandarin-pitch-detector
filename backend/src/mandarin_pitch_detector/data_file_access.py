"""Modules for reading and writing CSV file."""
import numpy as np

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
