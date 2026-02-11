import psutil
import gc

class SystemMonitor:
    def __init__(self):
        self.last_net_io = psutil.net_io_counters()
        psutil.cpu_percent(interval=None) # Init CPU counter

    def free_memory(self):
        """Attempts to free up memory by collecting garbage."""
        gc.collect()
        return True

    def get_cpu_usage(self):
        """Returns the current CPU usage percentage."""
        return psutil.cpu_percent(interval=None)

    def get_ram_usage(self):
        """Returns a dictionary with RAM usage details."""
        ram = psutil.virtual_memory()
        return {
            "total": ram.total,
            "available": ram.available,
            "percent": ram.percent,
            "used": ram.used
        }

    def get_disk_usage(self):
        """Returns the disk usage for the main partition."""
        disk = psutil.disk_usage('/')
        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }

