# Content of encoding_schemes/modulation_schemes.py
import numpy as np


def ask(bits, amp1=1, amp0=0, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration * len(bits), samples_per_bit * len(bits))
    carrier = np.sin(2 * np.pi * 10 * t)  # 10 Hz carrier frequency
    signal = np.array([amp1 if bit == '1' else amp0 for bit in bits])
    return np.repeat(signal, samples_per_bit) * carrier, t


def fsk(bits, f1=10, f0=5, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration * len(bits), samples_per_bit * len(bits))
    signal = np.zeros(len(t))
    for i, bit in enumerate(bits):
        t_bit = t[i * samples_per_bit:(i + 1) * samples_per_bit] - i * bit_duration
        signal[i * samples_per_bit:(i + 1) * samples_per_bit] = np.sin(2 * np.pi * (f1 if bit == '1' else f0) * t_bit)
    return signal, t


def qam(bits, amp1=1, amp2=0.5, f=10, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration * len(bits), samples_per_bit * len(bits))
    i_signal = np.array([amp1 if bit == '1' else -amp1 for bit in bits[::2]])
    q_signal = np.array([amp2 if bit == '1' else -amp2 for bit in bits[1::2]])

    i_carrier = np.cos(2 * np.pi * f * t)
    q_carrier = np.sin(2 * np.pi * f * t)

    i_modulated = np.repeat(i_signal, 2 * samples_per_bit) * i_carrier
    q_modulated = np.repeat(q_signal, 2 * samples_per_bit) * q_carrier

    return i_modulated + q_modulated, t


def psk(bits, f=10, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration * len(bits), samples_per_bit * len(bits))
    signal = np.zeros(len(t))
    for i, bit in enumerate(bits):
        t_bit = t[i * samples_per_bit:(i + 1) * samples_per_bit] - i * bit_duration
        signal[i * samples_per_bit:(i + 1) * samples_per_bit] = np.sin(
            2 * np.pi * f * t_bit + (0 if bit == '0' else np.pi))
    return signal, t