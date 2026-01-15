import time
import random
import pandas as pd
from datetime import datetime

class SiloProbeSimulator:
    def __init__(self, silo_id="SIM_SILO_001"):
        self.silo_id = silo_id
        self.current_depth = 0
        self.state = "safe" # Can be: safe, warning, critical
        
    def set_state(self, state):
        self.state = state

    def get_reading(self):
        # Base physics with random "sensor noise"
        if self.state == "safe":
            temp = 22 + random.uniform(-1, 1)
            co = max(0, 2 + random.uniform(-0.5, 0.5))
            voc = 10 + random.uniform(-2, 2)
        elif self.state == "warning":
            temp = 38 + random.uniform(-2, 5)
            co = 18 + random.uniform(-3, 8)
            voc = 80 + random.uniform(-10, 20)
        else: # Critical
            temp = 65 + random.uniform(0, 15)
            co = 120 + random.uniform(20, 50)
            voc = 400 + random.uniform(50, 100)

        reading = {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'silo_id': self.silo_id,
            'depth_m': self.current_depth,
            'temp_c': round(temp, 2),
            'co_ppm': round(co, 2),
            'voc_index': round(voc, 2)
        }
        
        # Simulate the probe moving down (0m to 10m)
        self.current_depth = (self.current_depth + 1) % 11
        return reading

if __name__ == "__main__":
    sim = SiloProbeSimulator()
    print("Starting Virtual Sensor Stream (Ctrl+C to stop)...")
    while True:
        data = sim.get_reading()
        print(f"📡 Sensor Out -> Depth: {data['depth_m']}m | Temp: {data['temp_c']}°C | CO: {data['co_ppm']}ppm")
        time.sleep(2) # Sends a reading every 2 seconds