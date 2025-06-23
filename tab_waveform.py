import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from scipy import signal
import json

class Waveform:
    def __init__(self, waveform_frame):
        self.control_frame = ttk.Frame(waveform_frame)
        self.control_frame.grid(row=0, column=0, sticky='nw')

        # Timing controls
        ttk.Label(self.control_frame, text="Steps").grid(row=0, column=3, sticky='w')
        self.steps_var = tk.DoubleVar()
        self.steps_entry = ttk.Entry(self.control_frame, textvariable=self.steps_var, width=8)
        self.steps_entry.grid(row=0, column=4)
        self.steps_var.set(1000)

        ttk.Label(self.control_frame, text="dt").grid(row=0, column=5, sticky='w')
        self.dt_var = tk.DoubleVar()
        self.dt_entry = ttk.Entry(self.control_frame, textvariable=self.dt_var, width=8)
        self.dt_entry.grid(row=0, column=6)
        self.dt_var.set(0.01)

        ttk.Label(self.control_frame, text="Time").grid(row=0, column=7, sticky='w')
        self.time_var = tk.DoubleVar()
        self.time_entry = ttk.Entry(self.control_frame, textvariable=self.time_var, width=8)
        self.time_entry.grid(row=0, column=8)
        self.time_var.set(1)

        ttk.Label(self.control_frame, text="Hz").grid(row=0, column=9, sticky='w')
        self.hz_var = tk.DoubleVar()
        self.hz_entry = ttk.Entry(self.control_frame, textvariable=self.hz_var, width=8)
        self.hz_entry.grid(row=0, column=10)
        self.hz_var.set(100)

        self.dt_var.trace_add("write", lambda *args: self.update_from_dt())
        self.steps_var.trace_add("write", lambda *args: self.update_from_steps())
        self.time_var.trace_add("write", lambda *args: self.update_from_total_time())
        self.hz_var.trace_add("write", lambda *args: self.update_from_hz())

        # Top Row: Waveform type selection and Add button
        ttk.Label(self.control_frame, text="Waveform Type").grid(row=1, column=0, sticky='w')
        self.waveform_type_combobox = ttk.Combobox(
            self.control_frame,
            values=[
                "Sine", "Square", "Sawtooth", "Triangle",
                "Gaussian Pulse", "Sin Pulse", "Square Pulse"
            ],
            state="readonly"
        )
        self.waveform_type_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.waveform_type_combobox.current(0)

        self.add_button = ttk.Button(self.control_frame, text="Add", command=self.add_waveform_row)
        self.add_button.grid(row=1, column=2, padx=5)

        # Container for added waveform rows
        self.waveform_rows_frame = ttk.Frame(self.control_frame)
        self.waveform_rows_frame.grid(row=2, column=0, columnspan=11, sticky='nw')

        self.row_count = 0
        self.rows = []

    def add_waveform_row(self):
        waveform_type = self.waveform_type_combobox.get()
        row_frame = ttk.Frame(self.waveform_rows_frame)
        row_frame.grid(row=self.row_count, column=0, sticky='w', pady=2)

        ttk.Label(row_frame, text=waveform_type).grid(row=0, column=0, padx=5)

        entry_labels = []
        if waveform_type in ["Sine", "Square", "Sawtooth", "Triangle"]:
            entry_labels = ["Frequency", "Amplitude", "Phase", "Y Offset", "Frequency Change"]
        elif waveform_type == "Gaussian Pulse":
            entry_labels = ["Width", "Amplitude", "X Offset", "Y Offset", "Frequency Change"]
        elif waveform_type == "Sin Pulse":
            entry_labels = ["Frequency", "Amplitude", "T Start", "N Half Oscillations", "Y Offset", "Frequency Change"]
        elif waveform_type == "Square Pulse":
            entry_labels = ["T Start", "Amplitude", "On Width", "Off Width", "N Oscillations", "Frequency Change"]

        entry_vars = []
        for i, label in enumerate(entry_labels):
            ttk.Label(row_frame, text=label).grid(row=0, column=1 + 2 * i, padx=2)
            var = tk.DoubleVar()
            entry = ttk.Entry(row_frame, textvariable=var, width=8)
            entry.grid(row=0, column=2 + 2 * i, padx=2)
            entry_vars.append((label, var))

        delete_button = ttk.Button(row_frame, text="Delete", command=lambda: self.delete_row(row_frame))
        delete_button.grid(row=0, column=2 + 2 * len(entry_labels), padx=5)

        self.rows.append((waveform_type, entry_vars, row_frame))
        self.row_count += 1

    def delete_row(self, row_frame):
        row_frame.destroy()
        self.row_count -= 1

    def update_from_dt(self):
        try:
            dt = self.dt_var.get()
            steps = int(self.time_var.get() / dt)
            sampling_rate = 1 / dt
            self.steps_var.set(steps)
            self.hz_var.set(sampling_rate)
        except:
            pass

    def update_from_steps(self):
        try:
            dt = self.dt_var.get()
            steps = int(self.steps_var.get())
            total_time = steps * dt
            sampling_rate = 1 / dt
            self.time_var.set(total_time)
            self.hz_var.set(sampling_rate)
        except:
            pass

    def update_from_total_time(self):
        try:
            dt = self.dt_var.get()
            total_time = self.time_var.get()
            steps = int(total_time / dt)
            self.steps_var.set(steps)
        except:
            pass

    def update_from_hz(self):
        try:
            rate = self.hz_var.get()
            dt = 1 / rate
            self.dt_var.set(dt)
        except:
            pass
