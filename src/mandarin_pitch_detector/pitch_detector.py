"""Modules containing pitch detection functions"""
import numpy as np
import logging
from mandarin_pitch_detector.pitch_model import linear_regression

logger = logging.getLogger(__name__)

def get_groups(time: np.ndarray, frequency: np.ndarray, confidence: np.ndarray, threshold_confidence: float, min_duration: float) -> list | None:
    """
    Plot activations and save the plot to file.

    Parameters:
    - time (np.ndarray): The timestamps on which the pitch was estimated
    - frequency (np.ndarray): The predicted pitch values in Hz
    - confidence (np.ndarray): The confidence of voice activity, between 0 and 1
    - threshold_confidence (float): Threshold of confidence for identifying groups
    - min_duration (float): Minimum duration in ms for identifying groups
    - file (str): The file name to be saved as
    
    Returns:
    - list | None: List of tuples representing groups identified for pitch detection,
                    else None
    """

    chunks = []

    start_idx = None

    for i, _ in enumerate(confidence):
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
    if len(chunks) > 0:
        return chunks
    logger.warning("No voice detected!")
    return None

def process_chunks(chunks: list) -> None:
    for i, (t, f, c) in enumerate(chunks):
        coef, intercept, score = linear_regression(t, f)
        print(f"Chunk {i}: Coefficiency {coef}, intercept {intercept}, score {score}")
