"""Modules for creating visualization plots"""
import matplotlib.pyplot as plt
import matplotlib.cm
from imageio import imwrite
import numpy as np

def save_activation_plot(activation: np.ndarray, file: str) -> None:
    """
    Plot activations and save the plot to file.

    Args:
        activation (np.ndarray): The raw activation matrix
        file (str): The file name to be saved as
    
    """
    # Draw the low pitches in the bottom
    salience = np.flip(activation, axis=1)
    inferno = matplotlib.cm.get_cmap('inferno')
    image = inferno(salience.transpose())
    imwrite(file, (255 * image).astype(np.uint8))

def save_audio_plot(audio: np.ndarray, file: str) -> None:
    """
    Plot audio and save the plot to file.

    Args:
        audio (np.ndarray): The input audio
        file (str): The file name to be saved as 
    
    """
    plt.figure()
    plt.plot(audio,'b')
    plt.savefig(file)

def save_frequency_plot(frequency: np.ndarray, file: str) -> None:
    """
    Plot frequency and save the plot to file.

    Args:
        frequency (np.ndarray): The input audio
        file (str): The file name to be saved as 
    
    """
    plt.figure()
    plt.plot(frequency,'g')
    plt.savefig(file)
