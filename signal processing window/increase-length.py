"""
File: increase-length.py
Author: Chuncheng Zhang
Date: 2025-04-24
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    What will happen if the length of the time series is increased to 100s?

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-04-24 ------------------------
# Requirements and constants
import noise
import numpy as np
import matplotlib.pyplot as plt


# %% ---- 2025-04-24 ------------------------
# Function and class


def generate_simplex_noise(num_points, octave):
    """
    Generate simplex noise for the given number of points with a specified octave.

    Args:
        num_points (int): Number of points to generate noise for.
        octave (int): The octave to scale the noise.

    Returns:
        np.ndarray: Array of simplex noise values.
    """
    seed = int(np.random.randint(0, 100))
    return np.array([noise.pnoise1(i / num_points * octave, base=seed) for i in range(num_points)])


def compute_and_plot_fft(time_series, sampling_rate=1.0):
    """
    Compute and plot the FFT of a time series.

    Args:
        time_series (np.ndarray): The input time series data.
        sampling_rate (float): Sampling rate of the time series.

    Returns:
        None
    """
    fft_result = np.fft.fft(time_series)
    frequencies = np.fft.fftfreq(len(time_series), d=1/sampling_rate)
    frequencies = (frequencies + 1) % 1

    # Create a 2x2 grid for plotting
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    # Plot the time series
    axs[0, 0].plot(time_series, color='blue')  # Added color
    axs[0, 0].set_title("Time Series")
    axs[0, 0].set_xlabel("Index")
    axs[0, 0].set_ylabel("Amplitude")

    # Plot the real part of FFT
    axs[0, 1].plot(frequencies, np.real(fft_result),
                   color='green')  # Added color
    axs[0, 1].set_title("FFT Real Part")
    axs[0, 1].set_xlabel("Frequency (Hz)")
    axs[0, 1].set_ylabel("Amplitude")

    # Plot the imaginary part of FFT
    axs[1, 0].plot(frequencies, np.imag(fft_result),
                   color='red')  # Added color
    axs[1, 0].set_title("FFT Imaginary Part")
    axs[1, 0].set_xlabel("Frequency (Hz)")
    axs[1, 0].set_ylabel("Amplitude")

    # Plot the absolute value of FFT
    axs[1, 1].plot(frequencies, np.abs(fft_result),
                   color='purple')  # Added color
    axs[1, 1].set_title("FFT Absolute Value")
    axs[1, 1].set_xlabel("Frequency (Hz)")
    axs[1, 1].set_ylabel("Amplitude")

    return fig


# %% ---- 2025-04-24 ------------------------
# Play ground
print(plt.style.available)
plt.style.use('ggplot')

# Generate and plot simplex noise with octave
num_points = 100
octave = 20  # Example octave value
time_series = generate_simplex_noise(num_points, octave)
octave = 10
time_series_2 = generate_simplex_noise(num_points, octave)

sampling_rate = 1.0  # Example sampling rate
compute_and_plot_fft(time_series, sampling_rate)
plt.suptitle("Raw Time Series")
plt.tight_layout()
plt.show()

time_series_repeat = np.concatenate((time_series, time_series))
compute_and_plot_fft(time_series_repeat, sampling_rate)
plt.suptitle("Repeated Time Series")
plt.tight_layout()
plt.show()

time_series_concat = np.concatenate((time_series, time_series_2))
compute_and_plot_fft(time_series_concat, sampling_rate)
plt.suptitle("Concated Time Series")
plt.tight_layout()
plt.show()

# %% ---- 2025-04-24 ------------------------
# Pending


# %% ---- 2025-04-24 ------------------------
# Pending
