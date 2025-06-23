import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from scipy import signal
import json

class Waveform():
    def __init__(self, waveform_frame):
        self.control_frame = ttk.Frame(waveform_frame)
        self.control_frame.grid(row=0, column=0, columnspan=6, sticky='w')
        
        ttk.Label(self.control_frame, text="Steps").grid(row=0, column=0, sticky='w')
        self.steps_var = tk.DoubleVar()
        self.steps_entry = ttk.Entry(self.control_frame, textvariable=self.steps_var)
        self.steps_entry.grid(row=1, column=0)
        self.steps_var.set(1000)

        ttk.Label(self.control_frame, text="dt").grid(row=0, column=1, sticky='w')
        self.dt_var = tk.DoubleVar()
        self.dt_entry = ttk.Entry(self.control_frame, textvariable=self.dt_var)
        self.dt_entry.grid(row=1, column=1)
        self.dt_var.set(0.01)

        ttk.Label(self.control_frame, text="Time").grid(row=0, column=2, sticky='w')
        self.time_var = tk.DoubleVar()
        self.time_entry = ttk.Entry(self.control_frame, textvariable=self.time_var)
        self.time_entry.grid(row=1, column=2)
        self.time_var.set(1)

        ttk.Label(self.control_frame, text="Hz").grid(row=0, column=3, sticky='w')
        self.hz_var = tk.DoubleVar()
        self.hz_entry = ttk.Entry(self.control_frame, textvariable=self.hz_var)
        self.hz_entry.grid(row=1, column=3)
        self.hz_var.set(100)

        ttk.Label(self.control_frame, text="Waveform Type").grid(row=2, column=0, sticky='w')
        self.waveform_type_combobox = ttk.Combobox(self.control_frame, values=["Sine", "Square", "Sawtooth", "Triangle"], state="readonly")
        self.waveform_type_combobox.grid(row=3, column=0)
        self.waveform_type_combobox.current(0)

        ttk.Label(self.control_frame, text="Frequency").grid(row=2, column=1, sticky='w')
        self.freq_var = tk.DoubleVar()
        self.freq_entry = ttk.Entry(self.control_frame, textvariable=self.freq_var)
        self.freq_entry.grid(row=3, column=1)
        self.freq_var.set(1)

        ttk.Label(self.control_frame, text="Amplitude").grid(row=2, column=2, sticky='w')
        self.amp_var = tk.DoubleVar()
        self.amp_entry = ttk.Entry(self.control_frame, textvariable=self.amp_var)
        self.amp_entry.grid(row=3, column=2)
        self.amp_var.set(1)

        ttk.Label(self.control_frame, text="Phase").grid(row=2, column=3, sticky='w')
        self.phase_var = tk.DoubleVar()
        self.phase_entry = ttk.Entry(self.control_frame, textvariable=self.phase_var)
        self.phase_entry.grid(row=3, column=3)
        self.phase_var.set(0)

        ttk.Label(self.control_frame, text="Offset").grid(row=2, column=4, sticky='w')
        self.offset_var = tk.DoubleVar()
        self.offset_entry = ttk.Entry(self.control_frame, textvariable=self.phase_var)
        self.offset_entry.grid(row=3, column=4)
        self.offset_var.set(0)

        self.width_var = tk.DoubleVar()
        self.position_var = tk.DoubleVar()
        self.on_width_var = tk.DoubleVar()
        self.t_start_var = tk.DoubleVar()
        self.off_width_var = tk.DoubleVar()
        self.n_osc_var = tk.IntVar()

        pulse_labels = ["Width", "Position", "On Width", "T Start", "Off Width", "N Oscillations"]
        pulse_vars = [self.width_var, self.position_var, self.on_width_var, self.t_start_var, self.off_width_var, self.n_osc_var]
        self.pulse_entries = []

        for i, (label, var) in enumerate(zip(pulse_labels, pulse_vars)):
            ttk.Label(self.control_frame, text=label).grid(row=5 + i // 3, column=(i % 3) * 2, sticky='w')
            entry = ttk.Entry(self.control_frame, textvariable=var, state='disabled')
            entry.grid(row=5 + i // 3, column=(i % 3) * 2 + 1)
            self.pulse_entries.append(entry)

        self.pulse_var = tk.BooleanVar()
        ttk.Checkbutton(self.control_frame, text="Pulse", variable=self.pulse_var, command=self.on_pulse_toggle).grid(row=4, column=0, sticky='w')

        self.freq_change_var = tk.BooleanVar()
        ttk.Checkbutton(self.control_frame, text="Frequency Change", variable=self.freq_change_var, command=self.on_freq_change_toggle).grid(row=3, column=5, sticky='w')



        self.dt_var.trace_add("write", lambda *args: self.update_from_dt())
        self.steps_var.trace_add("write", lambda *args: self.update_from_steps())
        self.time_var.trace_add("write", lambda *args: self.update_from_total_time())
        self.hz_var.trace_add("write", lambda *args: self.update_from_hz())


    #def setup_fourier_tab(self):
    
    #def setup_export_tab(self):

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

    def on_pulse_toggle(self):
        if self.pulse_var.get():
            self.waveform_type_combobox['values'] = ["Gaussian Envelope", "Square Envelope", "Square Train"]
            self.waveform_type_combobox.current(0)

            #self.freq_entry.config(state='disabled')
            #self.amp_entry.config(state='disabled')
            #self.phase_entry.config(state='disabled')
            #self.offset_entry.config(state='disabled')

            for entry in self.pulse_entries:
                entry.config(state='normal')
        else:
            self.waveform_type_combobox['values'] = ["Sine", "Square", "Sawtooth", "Triangle"]
            self.waveform_type_combobox.current(0)

            self.freq_entry.config(state='normal')
            self.amp_entry.config(state='normal')
            self.phase_entry.config(state='normal')
            self.offset_entry.config(state='normal')

            for entry in self.pulse_entries:
                entry.config(state='disabled')
    
    def on_freq_change_toggle(self):
        return