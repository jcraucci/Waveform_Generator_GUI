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

        general_frame = ttk.Frame(notebook)
        self.waveform_frame = ttk.Frame(notebook)
        export_frame = ttk.Frame(notebook)

        notebook.add(general_frame, text='')
        notebook.add(self.waveform_frame, text='')
        notebook.add(export_frame, text='')

if __name__ == "__main__":
    root = tk.Tk()
    app = Display(root)
    root.mainloop() 