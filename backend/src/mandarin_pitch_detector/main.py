"""A pitch detector developer for Mandarin Chinese."""

import crepe
from scipy.io import wavfile
from mandarin_pitch_detector.visualization import (
    save_activation_plot,
    save_audio_plot,
    save_frequency_plot)
from mandarin_pitch_detector.data_file_access import (
    read_from_csv,
    save_to_csv
)
from mandarin_pitch_detector.pitch_detector import get_groups, process_chunks


def rule_based_pitch_detector():
    sr, audio = wavfile.read('data/mandarinTones.wav')
    time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)
    save_audio_plot(audio, "data/audio.png")
    save_to_csv(time, frequency, confidence, 'data/time_freq_confidence.csv')
    save_activation_plot(activation, "data/activation.png")
    save_frequency_plot(frequency, "data/frequency.png")

    time, frequency, confidence = read_from_csv('data/time_freq_confidence.csv')
    chunks = get_groups(time, frequency, confidence, threshold_confidence=0.8, min_duration=0.15)
    process_chunks(chunks)

