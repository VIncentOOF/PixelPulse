import subprocess
import re
import tkinter as tk
from tkinter import ttk
import time
import threading
import math
import platform

def get_connected_network_interface() -> str:
    try:
        if platform.system() == "Linux":
            result = subprocess.run(['nmcli', '-t', '-f', 'DEVICE,STATE', 'device'], capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Failed to execute nmcli: {result.stderr}")

            output = result.stdout
            for line in output.splitlines():
                device, state = line.split(':')
                if state == 'connected':
                    return device

        elif platform.system() == "Windows":
            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Failed to execute netsh: {result.stderr}")

            output = result.stdout
            match = re.search(r'Name\s*:\s*(.*)', output)
            if match:
                return match.group(1).strip()
            else:
                raise ValueError("No connected wireless interface found")

    except Exception as e:
        print(f"Error: {e}")
        return None

def get_rssi(interface: str) -> int:
    try:
        if platform.system() == "Linux":
            result = subprocess.run(['iwconfig', interface], capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Failed to execute iwconfig: {result.stderr}")

            output = result.stdout
            rssi_search = re.search(r'Signal level=(-?\d+) dBm', output)
            if rssi_search:
                rssi = int(rssi_search.group(1))
                return rssi
            else:
                raise ValueError("Could not find RSSI in iwconfig output")

        elif platform.system() == "Windows":
            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Failed to execute netsh: {result.stderr}")

            output = result.stdout
            rssi_search = re.search(r'Signal\s*:\s*(-?\d+)', output)
            if rssi_search:
                rssi = int(rssi_search.group(1))
                return rssi
            else:
                raise ValueError("Could not find RSSI in netsh output")

    except Exception as e:
        print(f"Error: {e}")
        return None

class WifiSignalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wi-Fi Signal Strength Compass")

        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack()

        self.compass_needle = self.canvas.create_line(150, 150, 150, 50, width=4, fill="red")

        self.rssi_label = ttk.Label(root, text="RSSI: N/A")
        self.rssi_label.pack()

        self.current_interface = get_connected_network_interface()
        if not self.current_interface:
            self.rssi_label.config(text="No connected wireless interface found")
        else:
            self.update_signal()

    def update_signal(self):
        if self.current_interface:
            rssi = get_rssi(self.current_interface)
            if rssi is not None:
                self.rssi_label.config(text=f"RSSI: {rssi} dBm")
                angle = self.calculate_direction(rssi)
                self.update_needle(angle)
            else:
                self.rssi_label.config(text="Failed to retrieve RSSI")

        self.root.after(2000, self.update_signal)

    def calculate_direction(self, rssi):
        # Simulate direction based on RSSI (this is just an example)
        # Higher RSSI values (closer to 0) mean better signal
        if rssi > -50:
            return 0  # Best signal (up)
        elif rssi > -60:
            return 45
        elif rssi > -70:
            return 90
        elif rssi > -80:
            return 135
        else:
            return 180  # Worst signal (down)

    def update_needle(self, angle):
        length = 100
        x_center, y_center = 150, 150
        x_end = x_center + length * math.sin(math.radians(angle))
        y_end = y_center - length * math.cos(math.radians(angle))
        self.canvas.coords(self.compass_needle, x_center, y_center, x_end, y_end)

if __name__ == "__main__":
    root = tk.Tk()
    app = WifiSignalApp(root)
    root.mainloop()
