import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import os

def train_silo_ai(csv_file='silo_data.csv'):
    if not os.path.exists(csv_file):
        print("❌ Error: CSV file not found. Run generation script first.")
        return

    # 1. Load Data
    df = pd.read_csv(csv_file)
    X = df[['depth', 'temp', 'hum', 'voc']]
    y = df[['risk', 'time_to_incident']] # Multi-output target
    
    # 2. Initialize Model
    # Using a Multi-Output Regressor to handle both risk and time prediction
    model = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42)
    
    print("🧠 Training SiloGuard AI (Multi-Output Mode)...")
    model.fit(X, y)
    
    # 3. Create Model Directory if missing
    if not os.path.exists('models'):
        os.makedirs('models')
        
    # 4. Save Model
    joblib.dump(model, 'models/silo_model.pkl')
    print("✅ Model saved as 'models/silo_model.pkl'")

    # 5. Quick Verification Test
    # Scenario: Low Temp, but High Moisture and VOC
    test_data = pd.DataFrame([[105.0, 25.0, 90.0, 600.0]], columns=['depth', 'temp', 'hum', 'voc'])
    prediction = model.predict(test_data)[0]
    
    print("\n--- Model Verification ---")
    print(f"Input: Temp 25C, Moisture 90%, VOC 600")
    print(f"Predicted Risk: {prediction[0]:.2f}% (Should be < 50%)")
    print(f"Est. Time: {prediction[1]:.2f} hours")

if __name__ == "__main__":
    train_silo_ai()