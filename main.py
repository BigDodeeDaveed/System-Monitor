import customtkinter as ctk
from stats_collector import SystemMonitor
import threading
import time

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SystemMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("System Monitor")
        self.geometry("600x400")
        self.monitor = SystemMonitor()
        
        # Configure Grid Layout (2x2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # CPU Frame
        self.cpu_frame = ctk.CTkFrame(self)
        self.cpu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.cpu_label = ctk.CTkLabel(self.cpu_frame, text="CPU Usage", font=("Arial", 16, "bold"))
        self.cpu_label.pack(pady=5)
        
        # Get initial CPU stats
        init_cpu = self.monitor.get_cpu_usage()
        
        self.cpu_progress = ctk.CTkProgressBar(self.cpu_frame)
        self.cpu_progress.set(init_cpu / 100)
        self.cpu_progress.pack(pady=10, padx=10, fill="x")
        
        self.cpu_percent_label = ctk.CTkLabel(self.cpu_frame, text=f"{init_cpu}%")
        self.cpu_percent_label.pack(pady=5)

        # RAM Frame
        self.ram_frame = ctk.CTkFrame(self)
        self.ram_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.ram_label = ctk.CTkLabel(self.ram_frame, text="RAM Usage", font=("Arial", 16, "bold"))
        self.ram_label.pack(pady=5)
        
        # Get initial RAM stats
        init_ram = self.monitor.get_ram_usage()
        
        self.ram_progress = ctk.CTkProgressBar(self.ram_frame)
        self.ram_progress.set(init_ram["percent"] / 100)
        self.ram_progress.pack(pady=10, padx=10, fill="x")
        
        self.ram_text_label = ctk.CTkLabel(
            self.ram_frame, 
            text=f"Used: {init_ram['used'] / (1024**3):.1f} GB / Total: {init_ram['total'] / (1024**3):.1f} GB"
        )
        self.ram_text_label.pack(pady=5)
        
        self.free_mem_btn = ctk.CTkButton(self.ram_frame, text="Free Memory", command=self.free_memory_action)
        self.free_mem_btn.pack(pady=5)

    def free_memory_action(self):
        self.monitor.free_memory()
        original_text = self.free_mem_btn.cget("text")
        self.free_mem_btn.configure(text="Freed!", state="disabled")
        self.after(2000, lambda: self.free_mem_btn.configure(text=original_text, state="normal"))

        # Disk Frame
        self.disk_frame = ctk.CTkFrame(self)
        self.disk_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.disk_label = ctk.CTkLabel(self.disk_frame, text="Disk Usage", font=("Arial", 16, "bold"))
        self.disk_label.pack(pady=5)
        
        # Get initial Disk stats
        init_disk = self.monitor.get_disk_usage()
        
        self.disk_progress = ctk.CTkProgressBar(self.disk_frame)
        self.disk_progress.set(init_disk["percent"] / 100)
        self.disk_progress.pack(pady=10, padx=10, fill="x")
        
        self.disk_text_label = ctk.CTkLabel(
            self.disk_frame, 
            text=f"Used: {init_disk['used'] / (1024**3):.1f} GB / Free: {init_disk['free'] / (1024**3):.1f} GB"
        )
        self.disk_text_label.pack(pady=5)

        # Application close flag
        self.running = True
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start update loop
        self.after(100, self.update_stats)

    def update_stats(self):
        if not self.running:
            return
        
        try:
            # CPU
            cpu = self.monitor.get_cpu_usage()
            self.cpu_progress.set(cpu / 100)
            self.cpu_percent_label.configure(text=f"{cpu}%")

            # RAM
            ram = self.monitor.get_ram_usage()
            self.ram_progress.set(ram["percent"] / 100)
            self.ram_text_label.configure(
                text=f"Used: {ram['used'] / (1024**3):.1f} GB / Total: {ram['total'] / (1024**3):.1f} GB"
            )
            
            # Disk
            disk = self.monitor.get_disk_usage()
            self.disk_progress.set(disk["percent"] / 100)
            self.disk_text_label.configure(
                text=f"Used: {disk['used'] / (1024**3):.1f} GB / Free: {disk['free'] / (1024**3):.1f} GB"
            )

        
        except Exception as e:
            print(f"Error in update_stats: {e}")

        self.after(1000, self.update_stats)

    def on_close(self):
        self.running = False
        self.destroy()

if __name__ == "__main__":
    app = SystemMonitorApp()
    app.mainloop()
