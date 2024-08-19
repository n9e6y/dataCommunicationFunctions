import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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


def ask(bits, amp1=1, amp0=0.5, bit_duration=1, samples_per_bit=100):
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


def qam(bits, amp1=1, amp0=0.5, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration * len(bits), samples_per_bit * len(bits))
    carrier = np.sin(2 * np.pi * 10 * t)  # 10 Hz carrier frequency
    signal = np.array([amp1 if bit == '1' else amp0 for bit in bits])
    return np.repeat(signal, samples_per_bit) * carrier, t


def psk(bits, f=10, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration * len(bits), samples_per_bit * len(bits))
    signal = np.zeros(len(t))
    for i, bit in enumerate(bits):
        t_bit = t[i * samples_per_bit:(i + 1) * samples_per_bit] - i * bit_duration
        signal[i * samples_per_bit:(i + 1) * samples_per_bit] = np.sin(
            2 * np.pi * f * t_bit + (0 if bit == '0' else np.pi))
    return signal, t


def plot_signal(bits, coding_name):
    signal_function = globals()[coding_name.lower()]
    signal, t = signal_function(bits)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t, signal)
    ax.set_title(f"{coding_name.upper()} Signal")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    ax.set_ylim([-1.5, 1.5])
    ax.grid(True)

    # Add bit labels
    for i, bit in enumerate(bits):
        ax.text(i + 0.5, -1.7, bit, ha='center', va='center')

    ax.set_xticks(range(len(bits) + 1))
    ax.set_xticklabels(range(len(bits) + 1))

    return fig


def plot_button_click():
    global canvas
    bits = bit_sequence.get()
    coding_name = coding_name_var.get()

    if not all(bit in '01' for bit in bits):
        messagebox.showerror("Invalid Input", "Please enter a sequence of 0s and 1s only.")
        return

    if coding_name.lower() not in globals():
        messagebox.showerror("Invalid Function", "Please enter a valid modulation function name.")
        return

    if canvas:
        canvas.get_tk_widget().pack_forget()

    fig = plot_signal(bits, coding_name)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()


root = Tk()
root.title("Signal Plotter")

canvas = None

Label(root, text="Enter the bit sequence:").pack()
bit_sequence = StringVar()
Entry(root, textvariable=bit_sequence).pack()

Label(root, text="Select the coding/modulation function:").pack()
coding_name_var = StringVar(root)
coding_name_var.set("ami")  # default value
options = ["ami", "rz", "nrz", "manchester", "hdb3", "ask", "fsk", "qam", "psk"]
OptionMenu(root, coding_name_var, *options).pack()

Button(root, text="Plot Signal", command=plot_button_click).pack()

root.mainloop()