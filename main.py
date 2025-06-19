import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from scipy import signal
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

        self.setup_waveform_tab()
        #self.setup_fourier_tab()
        #self.setup_export_tab()
    def setup_waveform_tab(self):
        self.control_frame = ttk.Frame(self.waveform_frame)
        self.control_frame.grid(row=0, column=0, columnspan=6, sticky='w')

        ttk.Label(self.control_frame, text="Frequency").grid(row=1, column=1, sticky='w')
        self.freq_var = tk.DoubleVar()
        self.freq_entry = ttk.Entry(self.control_frame, textvariable=self.freq_var)
        self.freq_entry.grid(row=2, column=1)

        ttk.Label(self.control_frame, text="Amplitude").grid(row=1, column=2, sticky='w')
        self.amp_var = tk.DoubleVar()
        self.amp_entry = ttk.Entry(self.control_frame, textvariable=self.amp_var)
        self.amp_entry.grid(row=2, column=2)

        ttk.Label(self.control_frame, text="Phase").grid(row=1, column=3, sticky='w')
        self.phase_var = tk.DoubleVar()
        self.phase_entry = ttk.Entry(self.control_frame, textvariable=self.phase_var)
        self.phase_entry.grid(row=2, column=3)

        ttk.Label(self.control_frame, text="Waveform Type").grid(row=1, column=0, sticky='w')
        self.waveform_type_combobox = ttk.Combobox(self.control_frame, values=["Sine", "Square", "Sawtooth", "Triangle"], state="readonly")
        self.waveform_type_combobox.grid(row=2, column=0)
        self.waveform_type_combobox.current(0)
        self.waveform_type_combobox.bind("<<ComboboxSelected>>", self.generate_waveform)


    #def setup_fourier_tab(self):
    
    #def setup_export_tab(self):


    
    def generate_waveform(self, event = None):
        wave_type = self.waveform_type_combobox.get()
        

if __name__ == "__main__":
    root = tk.Tk()
    app = Display(root)
    root.mainloop() 