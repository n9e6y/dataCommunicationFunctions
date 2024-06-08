import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def ami(bits):
    signal = []
    last_voltage = 1  # start with positive voltage
    for bit in bits:
        if bit == '1':
            signal.append(last_voltage)
            last_voltage *= -1  # toggle voltage on each '1'
        else:
            signal.append(0)  # represent '0' with zero voltage
    return signal

def rz(bits):
    signal = []
    for bit in bits:
        if bit == '1':
            signal.extend([1, 0])  # high for first half, low for second half
        else:
            signal.extend([0, 0])  # low for both halves for '0'
    return signal

def nrz(bits):
    signal = [1 if bit == '1' else -1 for bit in bits]
    return signal

def manchester(bits):
    signal = []
    for bit in bits:
        if bit == '1':
            signal.extend([-1, 1])  # high to low for '1'
        else:
            signal.extend([1, -1])  # low to high for '0'
    return signal

def hdb3(bits):
    signal = []
    last_nonzero = 1
    zero_count = 0
    for bit in bits:
        if bit == '1':
            if zero_count == 4:
                signal[-4] = last_nonzero
                signal.append(0)
                zero_count = 0
            else:
                signal.append(last_nonzero)
                last_nonzero *= -1
            zero_count = 0
        else:
            zero_count += 1
            if zero_count == 4:
                if last_nonzero == -1:
                    signal.extend([0, 0, 0, 1])
                else:
                    signal.extend([0, 0, 0, -1])
                zero_count = 0
            else:
                signal.append(0)
    return signal

def ask(bits, amp1=1, amp0=0.5, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration, samples_per_bit)
    signal = np.concatenate([amp1 * np.ones(samples_per_bit) if bit == '1' else amp0 * np.ones(samples_per_bit) for bit in bits])
    return signal, t

def fsk(bits, f1=5, f0=2, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration, samples_per_bit)
    signal = np.concatenate([np.sin(2 * np.pi * f1 * t) if bit == '1' else np.sin(2 * np.pi * f0 * t) for bit in bits])
    return signal, t

def qam(bits, amp1=1, amp0=0.5, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration, samples_per_bit)
    carrier = np.sin(2 * np.pi * 5 * t)  # 5 Hz carrier frequency
    signal = np.concatenate([(amp1 * carrier) if bit == '1' else (amp0 * carrier) for bit in bits])
    return signal, t

def psk(bits, f=5, bit_duration=1, samples_per_bit=100):
    t = np.linspace(0, bit_duration, samples_per_bit)
    signal = np.concatenate([np.sin(2 * np.pi * f * t + (0 if bit == '0' else np.pi)) for bit in bits])
    return signal, t


def plot_signal(bits, coding_name):
    n = len(bits)
    samples_per_bit = 100
    
    signal_function = globals()[coding_name.lower()]
    try:
        signal, t = signal_function(bits, samples_per_bit=samples_per_bit)
        time = np.linspace(0, n, len(signal))
        fig, ax = plt.subplots()
        ax.plot(time, signal)
    except TypeError:
        signal = signal_function(bits)
        time = np.arange(len(signal))
        fig, ax = plt.subplots()
        ax.step(time, signal, where='post')
        bit_positions = np.arange(0, len(bits) * 2, 2)
        ax.set_xticks(bit_positions)
        ax.set_xticklabels(range(len(bits))) 

    ax.set_title(f"{coding_name} Signal")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    ax.set_ylim([-1.5, 1.5])  
    ax.grid(True)
    
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
coding_name_var.set("ami")  # default  svalue
options = ["ami", "rz", "nrz", "manchester", "hdb3", "ask", "fsk", "qam", "psk"]
OptionMenu(root, coding_name_var, *options).pack()

Button(root, text="Plot Signal", command=plot_button_click).pack()

root.mainloop()
