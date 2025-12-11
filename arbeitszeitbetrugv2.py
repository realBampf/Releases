import tkinter as tk
import time
import threading
import math

STUNDENLOHN = 22.0

class SciFiTicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Credit Counter")

        self.bg = "#0A0F1F"
        self.fg = "#34E8FF"
        self.accent = "#1F3B4D"
        self.timer_color = "#39FF14"

        root.configure(bg=self.bg)

        
        self.running = False
        self.paused = False
        self.gesamt = 0.0
        self.start_time = None
        self.pause_offset = 0  

        # credits
        self.label = tk.Label(
            root,
            text="Gesamt: 0.00 €",
            font=("Consolas", 20, "bold"),
            bg=self.accent,
            fg=self.fg,
            padx=20,
            pady=15
        )
        self.label.pack(pady=20)

        # 
        self.timer_label = tk.Label(
            root,
            text="00:00:00",
            font=("Consolas", 22, "bold"),
            bg=self.bg,
            fg=self.timer_color,
            pady=10
        )
        self.timer_label.pack()

        # Buttons
        self.start_button = tk.Button(
            root,
            text="Start",
            command=self.start,
            font=("Consolas", 14),
            fg=self.fg, bg=self.bg,
            bd=3, relief="ridge"
        )
        self.start_button.pack(pady=5, ipadx=20, ipady=5)

        self.pause_button = tk.Button(
            root,
            text="Pause",
            command=self.pause,
            font=("Consolas", 14),
            fg=self.fg, bg=self.bg,
            bd=3, relief="ridge"
        )
        self.pause_button.pack(pady=5, ipadx=20, ipady=5)

        self.reset_button = tk.Button(
            root,
            text="Reset",
            command=self.reset,
            font=("Consolas", 14),
            fg=self.fg, bg=self.bg,
            bd=3, relief="ridge"
        )
        self.reset_button.pack(pady=5, ipadx=20, ipady=5)

        root.after(50, self.pulse)

    def start(self):
        if not self.running:
            # Start oder Resume
            self.running = True
            self.paused = False

            if self.start_time is None:
                # echter Neustart
                self.start_time = time.time()
            else:
                # Wiederaufnahme: neue Startzeit minus bereits vergangene zeit
                self.start_time = time.time() - self.pause_offset

            threading.Thread(target=self.tick_loop, daemon=True).start()
            self.update_timer()

    def pause(self):
        if self.running and not self.paused:
            self.paused = True
            self.running = False
            # Zeit bis zur Pause merken
            self.pause_offset = time.time() - self.start_time

    def reset(self):
        self.running = False
        self.paused = False
        self.gesamt = 0.0
        self.start_time = None
        self.pause_offset = 0

        self.label.config(text="Gesamt: 0.00 €")
        self.timer_label.config(text="00:00:00")

    def tick_loop(self):
        while self.running:
            time.sleep(3600)  # 1 Stunde
            if self.running:
                self.gesamt += STUNDENLOHN
                self.label.config(text=f"Gesamt: {self.gesamt:.2f} €")

    def update_timer(self):
        if self.running and not self.paused:
            elapsed = time.time() - self.start_time
            total = int(elapsed)

            h = total // 3600
            m = (total % 3600) // 60
            s = total % 60

            self.timer_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")

            self.root.after(200, self.update_timer)

    def pulse(self):
        now = time.time()
        glow = 20 + int((1 + math.sin(now)) * 10)
        color = f"#{glow:02X}{glow:02X}{glow:02X}"
        self.root.configure(highlightthickness=2, highlightbackground=color)
        self.root.after(60, self.pulse)


root = tk.Tk()
app = SciFiTicker(root)
root.mainloop()
