import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_silo_data(num_days=7, num_silos=3):
    data = []
    start_time = datetime.now() - timedelta(days=num_days)
    depths = range(0, 11) # 0 to 10 meters
    
    for silo_id in range(1, num_silos + 1):
        for day in range(num_days):
            for hour in range(24):
                current_time = start_time + timedelta(days=day, hours=hour)
                
                # Assign health state to the silo
                if silo_id == 1: state = 'safe'
                elif silo_id == 2: state = 'warning' if day > 3 else 'safe'
                else: state = 'critical' if day > 5 else ('warning' if day > 2 else 'safe')
                
                for depth in depths:
                    # Base Physics
                    base_temp = 20 + (depth * 0.5) 
                    
                    if state == 'safe':
                        temp = base_temp + np.random.normal(0, 1)
                        co = max(0, 2 + np.random.normal(0, 0.5))
                        voc = max(0, 10 + np.random.normal(0, 2))
                    elif state == 'warning':
                        temp = base_temp + 15 + (day * 2) + np.random.normal(0, 2)
                        co = 15 + np.random.normal(0, 3)
                        voc = 60 + np.random.normal(0, 10)
                    elif state == 'critical':
                        temp = base_temp + 40 + (day * 5) + np.random.normal(0, 5)
                        co = 60 + (day * 10) + np.random.normal(0, 10)
                        voc = 250 + np.random.normal(0, 50)

                    # Labeling Logic
                    label = 'Safe'
                    if temp > 55 or co > 50 or voc > 200: label = 'Critical'
                    elif temp > 35 or co > 10 or voc > 50: label = 'Warning'
                    
                    data.append({
                        'timestamp': current_time,
                        'silo_id': f'SILO_{silo_id:03d}',
                        'depth_m': depth,
                        'temp_c': round(temp, 2),
                        'co_ppm': round(co, 2),
                        'voc_index': round(voc, 2),
                        'label': label
                    })
    return pd.DataFrame(data)

df = generate_silo_data()
df.to_csv('silo_sensor_data.csv', index=False)