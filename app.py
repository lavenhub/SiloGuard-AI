import streamlit as st
import pandas as pd
import joblib
import time
import os
import plotly.graph_objects as go
from src.ml.health_logic import calculate_worker_health_index
from src.sim.sensor_simulator import SiloProbeSimulator

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SiloGuard AI | Advanced Monitoring",
    page_icon="🌾",
    layout="wide"
)

# --- HELPER FUNCTIONS ---
@st.cache_resource
def load_ai_model():
    """Loads the trained Random Forest model with error handling."""
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path, 'models', 'silo_risk_model.joblib')
    
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)

# --- INITIALIZATION ---
model = load_ai_model()

# Persist the simulator in session state so depth doesn't reset on rerun
if 'sim' not in st.session_state:
    st.session_state.sim = SiloProbeSimulator()
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Timestamp', 'Depth', 'Temp', 'CO', 'Risk'])

# --- SIDEBAR CONTROLS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1162/1162456.png", width=100)
st.sidebar.title("SiloGuard Control Center")
st.sidebar.markdown("---")

mode = st.sidebar.selectbox("Operation Mode", ["Live Simulation", "System Diagnostics"])
sim_speed = st.sidebar.slider("Polling Interval (seconds)", 1, 5, 2)
target_state = st.sidebar.radio("Simulate Environmental Condition", ["safe", "warning", "critical"])

st.sidebar.markdown("---")
if st.sidebar.button("Reset Simulation Data"):
    st.session_state.history = pd.DataFrame(columns=['Timestamp', 'Depth', 'Temp', 'CO', 'Risk'])
    st.rerun()

# --- MAIN DASHBOARD UI ---
st.title("🌾 SiloGuard AI: Early Combustion Detection")
st.markdown(f"**Status:** `System Operational` | **Active Silo:** `SILO_001` | **Model Status:** `{'Loaded' if model else 'Missing'}`")

if not model:
    st.error("⚠️ AI Model not found! Please run `python train_model.py` first.")
    st.stop()

# Layout Containers
metric_placeholder = st.empty()
col_left, col_right = st.columns([2, 1])

# --- LIVE LOGIC ---
if mode == "Live Simulation":
    # 1. Get current data from persistent simulator
    sim = st.session_state.sim
    sim.set_state(target_state)
    data = sim.get_reading()
    
    # 2. Prepare Features for AI
    # (Matches features: depth_m, temp_c, co_ppm, voc_index, temp_diff, gas_ratio)
    input_df = pd.DataFrame([{
        'depth_m': data['depth_m'],
        'temp_c': data['temp_c'],
        'co_ppm': data['co_ppm'],
        'voc_index': data['voc_index'],
        'temp_diff': 0.15, # Simulated rate of change
        'gas_ratio': data['co_ppm'] / (data['voc_index'] + 1)
    }])
    
    # 3. AI Inference
    risk_code = model.predict(input_df)[0]
    risk_map = {0: "Safe", 1: "Warning", 2: "Critical"}
    current_risk = risk_map.get(risk_code, "Unknown")
    
    # 4. Health Index Calculation
    health_idx = calculate_worker_health_index(data['co_ppm'], data['voc_index'], data['temp_c'])

    # --- RENDER METRICS ---
    with metric_placeholder.container():
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Probe Depth", f"{data['depth_m']} m")
        m2.metric("Grain Temperature", f"{data['temp_c']} °C")
        m3.metric("CO Concentration", f"{data['co_ppm']} ppm")
        
        # Color-coded Health Index
        if health_idx > 60:
            m4.metric("Worker Health Risk", f"{health_idx}/100", delta="- DANGER", delta_color="inverse")
        else:
            m4.metric("Worker Health Risk", f"{health_idx}/100", delta="+ NORMAL")

    # --- RENDER CHARTS ---
    with col_left:
        st.subheader("Real-Time Telemetry")
        # Add to history
        new_entry = pd.DataFrame([{
            'Timestamp': data['timestamp'], 'Depth': data['depth_m'], 
            'Temp': data['temp_c'], 'CO': data['co_ppm'], 'Risk': current_risk
        }])
        st.session_state.history = pd.concat([st.session_state.history, new_entry]).tail(20)
        
        # Line chart for Temp & CO
        st.line_chart(st.session_state.history.set_index('Timestamp')[['Temp', 'CO']])
        
        # Warning Messages
        if risk_code == 2:
            st.error(f"🚨 ALERT: CRITICAL HEAT DETECTED AT {data['depth_m']}M DEPTH")
        elif risk_code == 1:
            st.warning(f"⚠️ NOTICE: Unusual microbial activity/self-heating at {data['depth_m']}m")

    with col_right:
        st.subheader("Internal Probe Mapping")
        # 3D Visualization of the probe inside the silo
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=[0], y=[0], z=[-data['depth_m']],
            mode='markers+text',
            text=[f"{data['temp_c']}°C"],
            textposition="top center",
            marker=dict(
                size=18, 
                color=data['temp_c'], 
                colorscale='Inferno', 
                cmin=20, cmax=80,
                showscale=True,
                colorbar=dict(title="Temp °C", x=-0.2)
            )
        )])
        
        fig_3d.update_layout(
            scene=dict(
                zaxis=dict(range=[-10, 0], title="Silo Depth (m)"),
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                aspectratio=dict(x=1, y=1, z=2)
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            height=450
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    # --- AUTO-REFRESH ---
    time.sleep(sim_speed)
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()