import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from encoding_schemes import binary_schemes, modulation_schemes
from utils.plotting import plot_signal


class SignalPlotter:
    def __init__(self, master):
        self.master = master
        self.master.title("Signal Plotter")

        self.canvas = None

        tk.Label(self.master, text="Enter the bit sequence:").pack()
        self.bit_sequence = tk.StringVar()
        tk.Entry(self.master, textvariable=self.bit_sequence).pack()

        tk.Label(self.master, text="Select the coding/modulation function:").pack()
        self.coding_name_var = tk.StringVar(self.master)
        self.coding_name_var.set("ami")  # default value
        options = ["ami", "rz", "nrz", "manchester", "hdb3", "ask", "fsk", "qam", "psk"]
        tk.OptionMenu(self.master, self.coding_name_var, *options).pack()

        tk.Button(self.master, text="Plot Signal", command=self.plot_button_click).pack()

    def plot_button_click(self):
        bits = self.bit_sequence.get()
        coding_name = self.coding_name_var.get()

        if not all(bit in '01' for bit in bits):
            messagebox.showerror("Invalid Input", "Please enter a sequence of 0s and 1s only.")
            return

        scheme_module = binary_schemes if coding_name in ["ami", "rz", "nrz", "manchester",
                                                          "hdb3"] else modulation_schemes
        if not hasattr(scheme_module, coding_name):
            messagebox.showerror("Invalid Function", "Please enter a valid modulation function name.")
            return

        signal_function = getattr(scheme_module, coding_name)
        signal, t = signal_function(bits)

        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()

        fig = plot_signal(bits, coding_name, signal, t)
        self.canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()