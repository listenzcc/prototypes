"""
File: main.py
Author: Chuncheng Zhang
Date: 2025-04-23
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    1. Generate 10s length 100 Hz simplex noise time series and plot the result.
    2. Operate the psd analysis on the time series.
    3. Operate the wavelet analysis on the time series.
    4. Operate the upper analysis on the first 2s of the time series.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-04-23 ------------------------
# Requirements and constants

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram, welch
import pywt

# %% ---- 2025-04-23 ------------------------
# Function and class


def generate_simplex_noise(duration=10, sampling_rate=100):
    """Generate simplex noise time series."""
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    noise = np.random.normal(0, 1, t.shape)
    return t, noise


def plot_time_series(t, signal, title="Time Series"):
    """Plot the time series."""
    plt.figure(figsize=(10, 4))
    plt.plot(t, signal)
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()


def psd_analysis(signal, sampling_rate=100):
    """Perform power spectral density (PSD) analysis."""
    f, Pxx = welch(signal, fs=sampling_rate)
    plt.figure(figsize=(10, 4))
    plt.semilogy(f, Pxx)
    plt.title("Power Spectral Density (PSD) Analysis")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power Spectral Density")
    plt.grid()
    plt.show()


def wavelet_analysis(signal, wavelet='cmor', wavelet_default='cmor'):
    """Perform wavelet analysis."""
    coefficients, frequencies = pywt.cwt(
        signal, scales=np.arange(1, 128), wavelet=wavelet)
    plt.figure(figsize=(10, 4))
    plt.imshow(np.abs(coefficients), extent=[0, len(
        signal), frequencies[-1], frequencies[0]], aspect='auto', cmap='jet')
    plt.title("Wavelet Analysis")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.colorbar(label="Magnitude")
    plt.show()

    print(coefficients.shape, signal.shape)
    plt.figure(figsize=(10, 4))
    plt.imshow(np.abs(coefficients)[:, :200], extent=[0, len(
        signal[:200]), frequencies[-1], frequencies[0]], aspect='auto', cmap='jet')
    plt.title("Wavelet Analysis (Cropped)")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.colorbar(label="Magnitude")
    plt.show()


# %% ---- 2025-04-23 ------------------------
# Play ground

# Generate 10s length 100 Hz simplex noise time series
duration = 10
sampling_rate = 100
t, noise = generate_simplex_noise(duration, sampling_rate)

# Plot the time series
plot_time_series(t, noise, title="10s Simplex Noise Time Series")


# Perform PSD analysis
psd_analysis(noise, sampling_rate)

# Perform wavelet analysis
wavelet_analysis(noise)

# Analyze the first 2 seconds of the time series
first_2s_signal = noise[:2 * sampling_rate]
plot_time_series(t[:2 * sampling_rate], first_2s_signal,
                 title="First 2s Simplex Noise Time Series")
psd_analysis(first_2s_signal, sampling_rate)
wavelet_analysis(first_2s_signal)

# %% ---- 2025-04-23 ------------------------
# Pending


# %% ---- 2025-04-23 ------------------------
# Pending
