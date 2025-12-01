"""Modules containing pitch detection functions"""
import numpy as np
import logging
import io
import base64
import parselmouth
import matplotlib.pyplot as plt
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

def praat_pitch_detector(audio_path: str) -> dict:
    print(audio_path)
    sound = parselmouth.Sound(audio_path)
    print("Done")
    pitch = sound.to_pitch()
    
    # Extract pitch values
    pitch_values = pitch.selected_array['frequency']
    pitch_values = pitch_values[pitch_values != 0] # Remove unvoiced segments

    if len(pitch_values) < 5:
        print('Not enough voiced data')
        raise ValueError('Not enough voiced data')

    # Normalize pitch (semitones relative to mean)
    mean_pitch = np.mean(pitch_values)
    semitones = 12 * np.log2(pitch_values / mean_pitch)
    
    # Fit linear regression to get slope
    x = np.arange(len(semitones))
    slope, intercept = np.polyfit(x, semitones, 1)
    
    # Check for dipping (concavity) - simplified
    # If the middle part is significantly lower than start and end
    mid_idx = len(semitones) // 2
    start_val = np.mean(semitones[:len(semitones)//4])
    end_val = np.mean(semitones[3*len(semitones)//4:])
    mid_val = np.mean(semitones[mid_idx-len(semitones)//8 : mid_idx+len(semitones)//8])
    
    is_dipping = (start_val > mid_val + 0.5) and (end_val > mid_val + 0.5)

    tone = "Unknown"
    
    if is_dipping:
        tone = "Tone 3 (Dipping)"
    elif slope > 0.05: # Thresholds need tuning
        tone = "Tone 2 (Rising)"
    elif slope < -0.05:
        tone = "Tone 4 (Falling)"
    else:
        tone = "Tone 1 (Level)"

    # Generate plot
    plt.figure(figsize=(10, 4))
    plt.plot(semitones, label='Pitch Contour (Semitones)')
    plt.plot(x, slope * x + intercept, 'r--', label=f'Linear Fit (slope={slope:.2f})')
    plt.title(f'Pitch Analysis: {tone}')
    plt.xlabel('Time Frame')
    plt.ylabel('Semitones (relative to mean)')
    plt.legend()
    plt.grid(True)
    
    # Save plot to base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return {
        'tone': tone,
        'slope': slope,
        'is_dipping': bool(is_dipping),
        'pitch_contour': semitones.tolist(),
        'plot_image': plot_base64
    }
