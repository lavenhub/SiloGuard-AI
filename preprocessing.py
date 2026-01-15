import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_silo_data(file_path):
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 1. Feature Engineering: Calculate Rate of Change (Delta)
    # We group by silo and depth to see how values change at that specific spot
    df = df.sort_values(['silo_id', 'depth_m', 'timestamp'])
    df['temp_diff'] = df.groupby(['silo_id', 'depth_m'])['temp_c'].diff().fillna(0)
    df['co_diff'] = df.groupby(['silo_id', 'depth_m'])['co_ppm'].diff().fillna(0)
    
    # 2. Digital Nose: Gas Ratio
    # High CO relative to VOC often indicates deep smoldering
    df['gas_ratio'] = df['co_ppm'] / (df['voc_index'] + 1)
    
    # 3. Encode Labels (Safe=0, Warning=1, Critical=2)
    le = LabelEncoder()
    df['label_encoded'] = le.fit_transform(df['label'])
    
    return df, le

if __name__ == "__main__":
    data, encoder = preprocess_silo_data('silo_sensor_data.csv')
    print("Features engineered. Sample delta values:")
    print(data[['temp_c', 'temp_diff', 'gas_ratio']].head())