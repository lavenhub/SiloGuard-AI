import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
import os

# 1. Create directory
if not os.path.exists('models'):
    os.makedirs('models')

# 2. Load Data
df = pd.read_csv('silo_sensor_data.csv')

# 3. FEATURE ENGINEERING (This fixes your KeyError)
# Calculate the change in temperature (Delta T)
df = df.sort_values(['silo_id', 'timestamp'])
df['temp_diff'] = df.groupby('silo_id')['temp_c'].diff().fillna(0)

# Calculate the Digital Nose ratio (CO to VOC ratio)
df['gas_ratio'] = df['co_ppm'] / (df['voc_index'] + 1)

# 4. Select Features and Target
# Now these columns actually exist in the 'df' index!
features = ['depth_m', 'temp_c', 'co_ppm', 'voc_index', 'temp_diff', 'gas_ratio']
X = df[features]
y = df['label'] # Use 'label' or 'risk_label' based on your CSV column name

# 5. Train and Save
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, 'models/silo_risk_model.joblib')
print("✅ Success! The model is trained with all features and saved.")