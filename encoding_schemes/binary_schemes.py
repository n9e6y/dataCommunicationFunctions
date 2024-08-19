import numpy as np

def ami(bits, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration * len(bits), samples_per_bit * len(bits))
    signal = np.zeros(len(t))
    last_voltage = 1
    for i, bit in enumerate(bits):
        if bit == '1':
            signal[i * samples_per_bit:(i + 1) * samples_per_bit] = last_voltage
            last_voltage *= -1
    return signal, t


def rz(bits, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration * len(bits), samples_per_bit * len(bits))
    signal = np.zeros(len(t))
    for i, bit in enumerate(bits):
        if bit == '1':
            signal[i * samples_per_bit:i * samples_per_bit + samples_per_bit // 2] = 1
    return signal, t


def nrz(bits, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration * len(bits), samples_per_bit * len(bits))
    signal = np.array([1 if bit == '1' else -1 for bit in bits])
    return np.repeat(signal, samples_per_bit), t


def manchester(bits, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration * len(bits), samples_per_bit * len(bits))
    signal = np.zeros(len(t))
    for i, bit in enumerate(bits):
        if bit == '1':
            signal[i * samples_per_bit:i * samples_per_bit + samples_per_bit // 2] = -1
            signal[i * samples_per_bit + samples_per_bit // 2:(i + 1) * samples_per_bit] = 1
        else:
            signal[i * samples_per_bit:i * samples_per_bit + samples_per_bit // 2] = 1
            signal[i * samples_per_bit + samples_per_bit // 2:(i + 1) * samples_per_bit] = -1
    return signal, t


def hdb3(bits, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration * len(bits), samples_per_bit * len(bits))
    signal = np.zeros(len(t))
    last_nonzero = 1
    zero_count = 0
    for i, bit in enumerate(bits):
        if bit == '1':
            if zero_count == 4:
                signal[(i - 4) * samples_per_bit:(i - 3) * samples_per_bit] = last_nonzero
                zero_count = 0
            else:
                signal[i * samples_per_bit:(i + 1) * samples_per_bit] = last_nonzero
                last_nonzero *= -1
            zero_count = 0
        else:
            zero_count += 1
            if zero_count == 4:
                if last_nonzero == -1:
                    signal[i * samples_per_bit:(i + 1) * samples_per_bit] = 1
                else:
                    signal[i * samples_per_bit:(i + 1) * samples_per_bit] = -1
                last_nonzero *= -1
                zero_count = 0
    return signal, t