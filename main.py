"""
Author: Reagan Giuliano
Date Created: 12/25/25
A custom time-tracking application with start/stop functionality,
resume capability, and CSV logging
"""

import tkinter as tk
from tkinter import messagebox
import datetime
import csv
import os

# Configuration
LOG_FILE = "time_log.csv"


class TimeTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Work Timer")
        self.master.geometry("400x500")

        # Variables to track state
        self.start_time = None
        self.elapsed_time = datetime.timedelta()
        self.running = False
        self.last_entry = {"project": "", "internal": "", "comments": ""}

        # UI Setup
        self.label_timer = tk.Label(root, text="00:00:00", font=("Helvetica", 32))
        self.label_timer.pack(pady=20)

        self.btn_start = tk.Button(root, text="Start New Task", command=self.start_new, width=20, bg="#d4edda")
        self.btn_start.pack(pady=5)

        self.btn_resume = tk.Button(root, text="Resume Last Task", command=self.resume_last, width=20, bg="#cce5ff")
        self.btn_resume.pack(pady=5)

        self.btn_stop = tk.Button(root, text="Stop & Save", command=self.stop_timer, width=20, bg="#f8d7da",
                                  state="disabled")
        self.btn_stop.pack(pady=5)

        # Input Fields (Hidden until Stop is pressed)
        self.input_frame = tk.Frame(root)

        tk.Label(self.input_frame, text="Project:").pack()
        self.ent_project = tk.Entry(self.input_frame, width=40)
        self.ent_project.pack()

        tk.Label(self.input_frame, text="Internal Details:").pack()
        self.ent_internal = tk.Text(self.input_frame, height=3, width=40)
        self.ent_internal.pack()

        tk.Label(self.input_frame, text="Comments for Invoice:").pack()
        self.ent_comments = tk.Text(self.input_frame, height=3, width=40)
        self.ent_comments.pack()

        self.btn_save = tk.Button(self.input_frame, text="Confirm & Save to Log", command=self.save_data, bg="#28a745",
                                  fg="white")
        self.btn_save.pack(pady=10)

    def update_clock(self):
        if self.running:
            now = datetime.datetime.now()
            self.elapsed_time = now - self.start_time
            # Format time to HH:MM:SS
            display_time = str(self.elapsed_time).split(".")[0]
            if len(display_time) == 7: display_time = "0" + display_time  # padding
            self.label_timer.config(text=display_time)
            self.master.after(1000, self.update_clock)

    def start_new(self):
        self.clear_inputs()
        self.begin_timing()

    def resume_last(self):
        # Pre-fill with last known data
        self.ent_project.delete(0, tk.END)
        self.ent_project.insert(0, self.last_entry["project"])
        self.ent_internal.delete("1.0", tk.END)
        self.ent_internal.insert("1.0", self.last_entry["internal"])
        self.ent_comments.delete("1.0", tk.END)
        self.ent_comments.insert("1.0", self.last_entry["comments"])
        self.begin_timing()

    def begin_timing(self):
        self.start_time = datetime.datetime.now()
        self.running = True
        self.btn_start.config(state="disabled")
        self.btn_resume.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.input_frame.pack_forget()
        self.update_clock()

    def stop_timer(self):
        self.running = False
        self.btn_stop.config(state="disabled")
        self.input_frame.pack(pady=10)

    def clear_inputs(self):
        self.ent_project.delete(0, tk.END)
        self.ent_internal.delete("1.0", tk.END)
        self.ent_comments.delete("1.0", tk.END)

    def save_data(self):
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        project = self.ent_project.get()
        internal = self.ent_internal.get("1.0", tk.END).strip()
        comments = self.ent_comments.get("1.0", tk.END).strip()
        duration = str(self.elapsed_time).split(".")[0]

        # Save to memory for "Resume" feature
        self.last_entry = {"project": project, "internal": internal, "comments": comments}

        # Save to CSV
        file_exists = os.path.isfile(LOG_FILE)
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Date", "Project", "Duration", "Internal Details", "Invoice Comments"])
            writer.writerow([date_str, project, duration, internal, comments])

        messagebox.showinfo("Success", "Time logged successfully!")
        self.input_frame.pack_forget()
        self.btn_start.config(state="normal")
        self.btn_resume.config(state="normal")
        self.label_timer.config(text="00:00:00")


if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTracker(root)
    root.mainloop()