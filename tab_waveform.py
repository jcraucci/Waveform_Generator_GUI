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

        ttk.Label(self.control_frame, text="Envelope Type").grid(row=1, column=3, padx=5, sticky='w')

        self.envelope_type_var = tk.StringVar()
        self.envelope_type_combobox = ttk.Combobox(
            self.control_frame,
            textvariable=self.envelope_type_var,
            values=["None", "Gaussian", "Square", "Sin"],
            state="readonly",
            width=10
        )
        self.envelope_type_combobox.grid(row=1, column=4, padx=5)
        self.envelope_type_combobox.current(0)

        # Create but don't place the widgets yet
        self.envelope_width_label = ttk.Label(self.control_frame, text="Width")
        self.envelope_width_var = tk.DoubleVar()
        self.envelope_width_entry = ttk.Entry(self.control_frame, textvariable=self.envelope_width_var, width=8)

        self.envelope_shift_label = ttk.Label(self.control_frame, text="Shift")
        self.envelope_shift_var = tk.DoubleVar()
        self.envelope_shift_entry = ttk.Entry(self.control_frame, textvariable=self.envelope_shift_var, width=8)

        def update_envelope_fields(event=None):
            # Remove all widgets first
            self.envelope_width_label.grid_forget()
            self.envelope_width_entry.grid_forget()
            self.envelope_shift_label.grid_forget()
            self.envelope_shift_entry.grid_forget()

            envelope_type = self.envelope_type_var.get()
            if envelope_type != "None":
                # Place the labels and entries to the right of the combobox (col 4)
                self.envelope_width_label.grid(row=1, column=5, padx=2)
                self.envelope_width_entry.grid(row=1, column=6, padx=2)
                self.envelope_shift_label.grid(row=1, column=7, padx=2)
                self.envelope_shift_entry.grid(row=1, column=8, padx=2)

        self.envelope_type_combobox.bind("<<ComboboxSelected>>", update_envelope_fields)
        update_envelope_fields()  # initialize

        


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

            if label == "Frequency Change":
                var = tk.StringVar()
                combo = ttk.Combobox(row_frame, textvariable=var,
                                    values=["None", "Chirp", "Linear", "Quadratic"],
                                    state="readonly", width=10)
                combo.grid(row=0, column=2 + 2 * i, padx=2)
                combo.current(0)

                # Dynamically shown fields
                t0_label = ttk.Label(row_frame, text="T0")
                t0_entry_var = tk.DoubleVar()
                t0_entry = ttk.Entry(row_frame, textvariable=t0_entry_var, width=8)

                linear_label = ttk.Label(row_frame, text="Linear Factor")
                linear_entry_var = tk.DoubleVar()
                linear_entry = ttk.Entry(row_frame, textvariable=linear_entry_var, width=8)

                quad_label = ttk.Label(row_frame, text="Quadratic Factor")
                quad_entry_var = tk.DoubleVar()
                quad_entry = ttk.Entry(row_frame, textvariable=quad_entry_var, width=8)

                def update_freq_fields(event=None):
                    # Clear all
                    t0_label.grid_forget()
                    t0_entry.grid_forget()
                    linear_label.grid_forget()
                    linear_entry.grid_forget()
                    quad_label.grid_forget()
                    quad_entry.grid_forget()

                    base_col = combo.grid_info()['column'] + 1

                    mode = var.get()
                    if mode == "Chirp":
                        t0_label.grid(row=0, column=base_col, padx=2)
                        t0_entry.grid(row=0, column=base_col + 1, padx=2)
                    elif mode == "Linear":
                        linear_label.grid(row=0, column=base_col, padx=2)
                        linear_entry.grid(row=0, column=base_col + 1, padx=2)
                    elif mode == "Quadratic":
                        linear_label.grid(row=0, column=base_col, padx=2)
                        linear_entry.grid(row=0, column=base_col + 1, padx=2)
                        quad_label.grid(row=0, column=base_col + 2, padx=2)
                        quad_entry.grid(row=0, column=base_col + 3, padx=2)

                combo.bind("<<ComboboxSelected>>", update_freq_fields)
                update_freq_fields()  # Call once to match initial selection

                entry_vars.append((label, var))
                # Store the dynamic entries as needed:
                entry_vars.append(("T0", t0_entry_var))
                entry_vars.append(("Linear Factor", linear_entry_var))
                entry_vars.append(("Quadratic Factor", quad_entry_var))


            else:
                var = tk.DoubleVar()
                entry = ttk.Entry(row_frame, textvariable=var, width=8)
                entry.grid(row=0, column=2 + 2 * i, padx=2)
                entry_vars.append((label, var))

        delete_button = ttk.Button(row_frame, text="Delete", command=lambda: self.delete_row(row_frame))

        def place_delete_button():
            # Reposition the delete button based on the current rightmost column
            widgets = row_frame.grid_slaves(row=0)
            if not widgets:
                return
            max_col = max([w.grid_info()['column'] for w in widgets])
            delete_button.grid(row=0, column=max_col + 1, padx=5)

        combo.bind("<<ComboboxSelected>>", lambda e: [update_freq_fields(), place_delete_button()])
        update_freq_fields()
        place_delete_button()

        self.rows.append((waveform_type, entry_vars, row_frame))
        self.row_count += 1

    def delete_row(self, row_frame):
        row_frame.destroy()
        self.rows = [row for row in self.rows if row[2] != row_frame]
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
