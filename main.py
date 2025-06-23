import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from scipy import signal
from tab_waveform import Waveform
import json

class Display:
    def __init__(self, root):
        self.root = root
        self.root.title("Waveform Generator")

        style = ttk.Style(self.root)
        style.theme_use("winnative")

        self.setup_controls()

    def setup_controls(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.waveform_frame = ttk.Frame(notebook)
        self.fourier_frame = ttk.Frame(notebook)
        self.export_frame = ttk.Frame(notebook)

        notebook.add(self.waveform_frame, text='Waveform Generator')
        notebook.add(self.fourier_frame, text='Fourier Series')
        notebook.add(self.export_frame, text='Export Options')

        Waveform(self.waveform_frame)
        #self.setup_fourier_tab()
        #self.setup_export_tab()


if __name__ == "__main__":
    root = tk.Tk()
    app = Display(root)
    root.mainloop() 