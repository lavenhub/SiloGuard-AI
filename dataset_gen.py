import pandas as pd
import numpy as np
import os

def generate_silo_dataset(filename='silo_data.csv', samples=5000):
    np.random.seed(42)
    
    # 1. Simulate Raw Sensor Inputs
    # Depth matches your 'levels' array [0, 15, ..., 180]
    depth = np.random.choice([0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180], samples)
    temp = np.random.uniform(15, 75, samples)      # DHT22 Range
    moisture = np.random.uniform(0, 100, samples)  # Water Sensor %
    voc = np.random.uniform(50, 800, samples)     # MQ Sensor units
    
    # 2. Triple-Gate Logic for Combustion Risk
    # Risk only crosses 50% if (Temp > 45) AND (Moisture > 50) AND (VOC > 200)
    gate_met = (temp > 45) & (moisture > 50) & (voc > 200)
    
    # Base calculation for smooth scaling
    base_factor = ((temp/75) + (moisture/100) + (voc/800)) / 3.0
    
    # Apply the logic: Jump to 50+ if gate met, else stay below 50
    risk = np.where(gate_met, 
                    50 + (base_factor * 50), 
                    base_factor * 45)
    
    risk = np.clip(risk, 0, 100)
    
    # 3. Calculate Estimated Time to Incident (Hours)
    # Higher risk = Lower time. If risk is 0, time is high (e.g., 72 hours).
    incident_time = 72.0 - (risk * 0.7)
    incident_time = np.clip(incident_time, 1.0, 72.0)
    
    # 4. Save to CSV
    df = pd.DataFrame({
        'depth': depth,
        'temp': temp,
        'hum': moisture, # Matches FEATURES['hum'] in your app
        'voc': voc,
        'risk': risk,
        'time_to_incident': incident_time
    })
    
    df.to_csv(filename, index=False)
    print(f"✅ Dataset with {samples} samples saved to {filename}")

if __name__ == "__main__":
    generate_silo_dataset()