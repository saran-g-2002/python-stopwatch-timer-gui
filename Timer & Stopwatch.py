import tkinter as tk
from tkinter import ttk, messagebox
import time

class StopwatchTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch & Timer")
        self.root.geometry("500x600")
        self.root.configure(bg="#2c3e50")
        
        
        self.sw_running = False
        self.sw_start_time = 0
        self.sw_elapsed = 0
        self.sw_laps = []
        
    
        self.timer_running = False
        self.timer_remaining = 0
        self.timer_start_time = 0
        
        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        """Create all UI components."""
        title = tk.Label(self.root, text="⏱️ Stopwatch & Timer", font=("Arial", 20, "bold"),
                        bg="#2c3e50", fg="white")
        title.pack(pady=20)
        
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        
        self.sw_frame = ttk.Frame(notebook)
        notebook.add(self.sw_frame, text="Stopwatch")
        self.setup_stopwatch()
        
        
        self.timer_frame = ttk.Frame(notebook)
        notebook.add(self.timer_frame, text="Timer")
        self.setup_timer()

    def setup_stopwatch(self):
        """Setup stopwatch UI."""
        
        self.sw_display = tk.Label(self.sw_frame, text="00:00.00", font=("Digital-7", 48, "bold"),
                                 bg="#34495e", fg="#ecf0f1", relief="ridge", padx=30, pady=20)
        self.sw_display.pack(pady=30)
        
        
        btn_frame = tk.Frame(self.sw_frame, bg="#2c3e50")
        btn_frame.pack(pady=20)
        
        self.sw_start_btn = tk.Button(btn_frame, text="▶️ START", command=self.sw_start,
                                    width=12, height=2, font=("Arial", 12, "bold"),
                                    bg="#27ae60", fg="white", relief="flat")
        self.sw_start_btn.pack(side=tk.LEFT, padx=10)
        
        self.sw_pause_btn = tk.Button(btn_frame, text="⏸️ PAUSE", command=self.sw_pause,
                                    width=12, height=2, font=("Arial", 12, "bold"),
                                    bg="#f39c12", fg="white", relief="flat", state="disabled")
        self.sw_pause_btn.pack(side=tk.LEFT, padx=10)
        
        self.sw_reset_btn = tk.Button(btn_frame, text="🔄 RESET", command=self.sw_reset,
                                    width=12, height=2, font=("Arial", 12, "bold"),
                                    bg="#e74c3c", fg="white", relief="flat")
        self.sw_reset_btn.pack(side=tk.LEFT, padx=10)
        
        
        self.sw_lap_btn = tk.Button(self.sw_frame, text="LAP", command=self.sw_lap,
                                  width=10, font=("Arial", 10, "bold"),
                                  bg="#3498db", fg="white", relief="flat", state="disabled")
        self.sw_lap_btn.pack(pady=10)
        
        
        laps_frame = tk.Frame(self.sw_frame, bg="#2c3e50")
        laps_frame.pack(pady=20, fill="both", expand=True)
        
        tk.Label(laps_frame, text="Laps:", font=("Arial", 12, "bold"),
                bg="#2c3e50", fg="white").pack(anchor="w")
        
        self.sw_laps_list = tk.Listbox(laps_frame, font=("Arial", 10), bg="#34495e", fg="white",
                                     selectbackground="#3498db", height=8)
        self.sw_laps_list.pack(fill="both", expand=True, pady=(5,0))

    def setup_timer(self):
        """Setup timer UI."""
        
        input_frame = tk.Frame(self.timer_frame, bg="#2c3e50")
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="Set time (MM:SS):", font=("Arial", 14, "bold"),
                bg="#2c3e50", fg="white").pack()
        
        time_frame = tk.Frame(input_frame, bg="#2c3e50")
        time_frame.pack(pady=10)
        
        self.timer_min = tk.Spinbox(time_frame, from_=0, to=60, width=5, font=("Arial", 14),
                                  bg="#34495e", fg="white", relief="solid")
        self.timer_min.pack(side=tk.LEFT, padx=5)
        tk.Label(time_frame, text=":", bg="#2c3e50", fg="white", font=("Arial", 16)).pack(side=tk.LEFT)
        
        self.timer_sec = tk.Spinbox(time_frame, from_=0, to=59, width=5, font=("Arial", 14),
                                  bg="#34495e", fg="white", relief="solid")
        self.timer_sec.pack(side=tk.LEFT, padx=5)
        
        
        self.timer_display = tk.Label(self.timer_frame, text="00:00", font=("Digital-7", 48, "bold"),
                                    bg="#34495e", fg="#ecf0f1", relief="ridge", padx=30, pady=20)
        self.timer_display.pack(pady=30)
        
        
        btn_frame = tk.Frame(self.timer_frame, bg="#2c3e50")
        btn_frame.pack(pady=20)
        
        self.timer_start_btn = tk.Button(btn_frame, text="▶️ START", command=self.timer_start,
                                       width=12, height=2, font=("Arial", 12, "bold"),
                                       bg="#27ae60", fg="white", relief="flat")
        self.timer_start_btn.pack(side=tk.LEFT, padx=10)
        
        self.timer_pause_btn = tk.Button(btn_frame, text="⏸️ PAUSE", command=self.timer_pause,
                                       width=12, height=2, font=("Arial", 12, "bold"),
                                       bg="#f39c12", fg="white", relief="flat", state="disabled")
        self.timer_pause_btn.pack(side=tk.LEFT, padx=10)
        
        self.timer_reset_btn = tk.Button(btn_frame, text="🔄 RESET", command=self.timer_reset,
                                       width=12, height=2, font=("Arial", 12, "bold"),
                                       bg="#e74c3c", fg="white", relief="flat")
        self.timer_reset_btn.pack(side=tk.LEFT, padx=10)

    def format_time(self, total_ms):
        """Format milliseconds to MM:SS.ms."""
        total_seconds = int(total_ms / 1000)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        ms = int((total_ms % 1000) / 10)
        return f"{minutes:02d}:{seconds:02d}.{ms:02d}"

    def update_display(self):
        """Update displays every 10ms."""
        if self.sw_running:
            self.sw_elapsed = time.time() * 1000 - self.sw_start_time
            self.sw_display.config(text=self.format_time(self.sw_elapsed))
        
        if self.timer_running:
            elapsed = time.time() * 1000 - self.timer_start_time
            remaining = self.timer_remaining - elapsed
            if remaining > 0:
                self.timer_display.config(text=self.format_time(remaining), fg="#ecf0f1")
            else:
                self.timer_display.config(text="00:00.00", fg="#e74c3c")
                self.timer_complete()
        
        self.root.after(10, self.update_display)

    
    def sw_start(self):
        if not self.sw_running:
            self.sw_running = True
            if self.sw_elapsed == 0:
                self.sw_start_time = time.time() * 1000
            self.sw_start_btn.config(state="disabled")
            self.sw_pause_btn.config(state="normal")
            self.sw_lap_btn.config(state="normal")

    def sw_pause(self):
        if self.sw_running:
            self.sw_running = False
            self.sw_start_time = time.time() * 1000
            self.sw_start_btn.config(state="normal", text="▶️ RESUME")
            self.sw_pause_btn.config(state="disabled")
            self.sw_lap_btn.config(state="normal")

    def sw_reset(self):
        self.sw_running = False
        self.sw_elapsed = 0
        self.sw_laps = []
        self.sw_display.config(text="00:00.00")
        self.sw_start_btn.config(state="normal", text="▶️ START")
        self.sw_pause_btn.config(state="disabled")
        self.sw_lap_btn.config(state="disabled")
        self.sw_laps_list.delete(0, tk.END)

    def sw_lap(self):
        lap_time = self.format_time(self.sw_elapsed)
        self.sw_laps.append(lap_time)
        lap_num = len(self.sw_laps)
        self.sw_laps_list.insert(0, f"Lap {lap_num}: {lap_time}")

    
    def timer_start(self):
        mins = int(self.timer_min.get())
        secs = int(self.timer_sec.get())
        total_seconds = mins * 60 + secs
        
        if total_seconds == 0:
            messagebox.showwarning("Invalid Time", "Please set a time greater than 0!")
            return
            
        self.timer_remaining = total_seconds * 1000
        self.timer_start_time = time.time() * 1000
        self.timer_running = True
        
        self.timer_display.config(text=self.format_time(self.timer_remaining))
        self.timer_start_btn.config(state="disabled")
        self.timer_pause_btn.config(state="normal")
        self.timer_min.config(state="disabled")
        self.timer_sec.config(state="disabled")

    def timer_pause(self):
        if self.timer_running:
            elapsed = time.time() * 1000 - self.timer_start_time
            self.timer_remaining -= elapsed
            self.timer_running = False
            self.timer_start_btn.config(state="normal", text="▶️ RESUME")
            self.timer_pause_btn.config(state="disabled")

    def timer_reset(self):
        self.timer_running = False
        self.timer_remaining = 0
        self.timer_display.config(text="00:00")
        self.timer_start_btn.config(state="normal", text="▶️ START")
        self.timer_pause_btn.config(state="disabled")
        self.timer_min.config(state="normal")
        self.timer_sec.config(state="normal")
        self.timer_min.delete(0, tk.END)
        self.timer_sec.delete(0, tk.END)

    def timer_complete(self):
        self.root.bell()
        messagebox.showinfo("Time's Up!", "Timer completed!")
        self.timer_reset()

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchTimerApp(root)
    root.mainloop()
