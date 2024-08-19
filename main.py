import tkinter as tk
from gui.signal_plotter import SignalPlotter

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalPlotter(root)
    root.mainloop()