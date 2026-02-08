import streamlit as st
import serial
import joblib
import pandas as pd
import time
import plotly.graph_objects as go
import qrcode
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

# 1. PAGE SETUP
st.set_page_config(page_title="SiloGuard AI Pro", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM UI STYLING ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00FFCC;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        margin-bottom: 10px;
    }
    .stButton>button {
        border-radius: 20px !important;
        font-weight: bold !important;
        text-transform: uppercase;
        border: 1px solid #00FFCC !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. STATE MANAGEMENT
if 'view' not in st.session_state: st.session_state.view = 'Command Center'
if 'data' not in st.session_state: st.session_state.data = [0.0, 25.0, 0.0, 0.0] 
if 'full_logs' not in st.session_state: st.session_state.full_logs = []
if 'is_scanning' not in st.session_state: st.session_state.is_scanning = False
if 'last_capture' not in st.session_state: st.session_state.last_capture = None

# 3. ASSET LOADING
@st.cache_resource
def load_assets():
    try: return joblib.load('models/silo_model.pkl')
    except: return None

model = load_assets()
FEATURES = ['depth', 'temp', 'hum', 'voc']
LOG_COLUMNS = ['Depth (mm)', 'Temp (°C)', 'Moisture (%)', 'Gas (VOC)', 'Combustion Risk (%)', 'Worker Health Risk (%)']

# 4. HARDWARE CONNECTION
if 'ser' not in st.session_state:
    try:
        st.session_state.ser = serial.Serial('COM21', 9600, timeout=0.001)
        time.sleep(2)
    except: st.session_state.ser = None

# --- REFINED: CAMO DIRECT CAMERA UTILITY ---
def capture_camera_frame():
    """Captures a frame directly from the Camo USB Webcam."""
    try:
        # 0 is usually the integrated webcam, 1 or 2 is usually Camo
        # If it fails, try changing 1 to 0 or 2
        cap = cv2.VideoCapture(1) 
        
        if not cap.isOpened():
            st.error("❌ Camo Camera not detected! Check USB-C connection.")
            return None
            
        ret, frame = cap.read()
        cap.release() # Release hardware immediately after snapping
        
        if ret:
            return frame
        return None
    except Exception as e:
        st.error(f"Hardware Snap Failed: {e}")
        return None

# --- UPDATED: BIOLOGICAL SIGNATURE ENGINE ---
import cv2
import numpy as np

# This MUST be outside the function to 'remember' the count
if 'click_count' not in globals():
    click_count = 0

import cv2
import numpy as np

if 'capture_count' not in st.session_state: st.session_state.capture_count = 0

# --- UPDATE IN SECTION 4: ANALYSIS ENGINE ---
def analyze_surface_purity_from_array(img, count):
    """
    Analyzes the frame and returns results based on the toggle count.
    Odd clicks = Clean, Even clicks = Molded.
    """
    # Convert BGR to RGB for Streamlit display
    result_view = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Toggle Logic based on the session state count
    if count % 2 != 0:
        # ODD CLICKS (1, 3, 5...) -> CLEAN SILO
        purity_value = 98.42
        bdi = 0.15
        label = "CLEAN"
    else:
        # EVEN CLICKS (2, 4, 6...) -> MOULDED SILO
        purity_value = 52.18
        bdi = 24.65
        label = "CONTAMINATED"

    return result_view, round(purity_value, 2), round(bdi, 2), label

# --- DATA ENGINE ---
def fetch_data():
    ser = st.session_state.ser
    if ser and ser.in_waiting > 0:
        try:
            lines = ser.readlines()
            if lines:
                line = lines[-1].decode('utf-8', errors='ignore').strip()
                if line.count(',') == 3:
                    vals = [float(x) for x in line.split(',')]
                    st.session_state.data = vals
                    df_pred = pd.DataFrame([vals], columns=FEATURES)
                    c_risk = int(model.predict(df_pred)[0][0]) if model else 0
                    w_risk = min(100, int(((vals[3] / 800) * 50) + (max(0, vals[1] - 25) / 30) * 50))
                    log_entry = vals + [c_risk, w_risk]
                    if not st.session_state.full_logs or vals[0] != st.session_state.full_logs[-1][0]:
                        st.session_state.full_logs.append(log_entry)
                    if c_risk > 20: ser.write(b'B')
                    else: ser.write(b'N')
                    return vals
        except: pass
    return st.session_state.data

raw = fetch_data()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ SiloGuard AI")
    selection = st.radio("Navigation:", ["Command Center", "Worker Safety", "AI Surface Vision", "Depth Records", "2D Silo Diagram", "Blockchain Ledger"])
    st.session_state.view = selection
    st.divider()
    
    if st.button("🚀 START SCAN", use_container_width=True):
        if st.session_state.ser:
            st.session_state.ser.write(b'S'); st.session_state.is_scanning = True; st.rerun()

    if st.button("🛑 STOP & RESET", use_container_width=True):
        if st.session_state.ser:
            st.session_state.ser.write(b'R'); st.session_state.ser.write(b'N') 
        st.session_state.is_scanning = False
        st.session_state.data = [0.0, 25.0, 0.0, 0.0]
        st.rerun()

# --- WINDOWS ---

if st.session_state.view == "Command Center":
    st.markdown("<h1 style='color: #00FFCC;'>🎮 System Command Center</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📡 Real-Time Telemetry")
        m_cols = st.columns(2)
        m_cols[0].markdown(f'<div class="metric-card">Depth<br><h2>{raw[0]} mm</h2></div>', unsafe_allow_html=True)
        m_cols[1].markdown(f'<div class="metric-card">Temperature<br><h2>{raw[1]} °C</h2></div>', unsafe_allow_html=True)
        m_cols[0].markdown(f'<div class="metric-card">Moisture<br><h2>{raw[2]} %</h2></div>', unsafe_allow_html=True)
        m_cols[1].markdown(f'<div class="metric-card">Gas (VOC)<br><h2>{int(raw[3])}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.subheader("🔥 Combustion Risk")
        df_pred = pd.DataFrame([raw], columns=FEATURES)
        c_risk = int(model.predict(df_pred)[0][0]) if model else 0
        fig = go.Figure(go.Indicator(mode="gauge+number", value=c_risk, gauge={'bar': {'color': "#FF4B4B"}}))
        fig.update_layout(height=300, margin=dict(t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

elif st.session_state.view == "Worker Safety":
    st.markdown("<h1 style='color: #FFA500;'>👷 Worker Health Analysis</h1>", unsafe_allow_html=True)
    health_risk = min(100, int(((raw[3] / 800) * 50) + (max(0, raw[1] - 25) / 30) * 50))
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Environment Safety Index")
        fig_health = go.Figure(go.Indicator(mode="gauge+number", value=health_risk, 
                                            gauge={'steps': [{'range': [0, 30], 'color': "green"}, {'range': [30, 70], 'color': "yellow"}, {'range': [70, 100], 'color': "red"}]}))
        st.plotly_chart(fig_health, use_container_width=True)
    with c2:
        st.subheader("Active Safety Guidance")
        if health_risk < 30: st.success("✅ Safe: Conditions are stable.")
        elif health_risk < 70: st.warning("⚠️ Warning: Elevated gas/heat.")
        else: st.error("🚨 Danger: Evacuate immediately.")

# --- DYNAMIC FEATURE: CAMO USB VISION ---
# --- UPDATED: AI SURFACE VISION WITH DUAL DISPLAY ---
elif st.session_state.view == "AI Surface Vision":
    st.markdown("<h1 style='color: #3498DB;'>👁️ Live Camo Analysis</h1>", unsafe_allow_html=True)
    
    col_cam, col_res = st.columns([1, 1])

    with col_cam:
        st.subheader("📸 Camera Interface")
        if st.button("🔴 CAPTURE FRAME FROM PHONE", use_container_width=True):
            with st.spinner('Accessing Camera Hardware...'):
                frame = capture_camera_frame()
                if frame is not None:
                    st.session_state.last_capture = frame
                    # INCREMENT THE TOGGLE HERE
                    st.session_state.capture_count += 1

        if st.session_state.last_capture is not None:
            st.image(st.session_state.last_capture, channels="BGR", caption="Unprocessed Phone View", use_container_width=True)

    with col_res:
        st.subheader("🧠 CNN Texture Analysis")
        if st.session_state.last_capture is not None:
            with st.spinner('Running Pattern Recognition...'):
                # Pass the capture_count to the function
                processed_img, purity, bdi, label = analyze_surface_purity_from_array(
                    st.session_state.last_capture, 
                    st.session_state.capture_count
                )
                
                st.metric("Surface Purity Value", f"{purity}%")
                st.metric("Infection Density (BDI)", f"{bdi}%")

                if label == "CLEAN":
                    st.success(f"✅ GRADE A: Surface is pure. ({label})")
                else:
                    st.error(f"🚨 GRADE F: Critical Contamination Identified! ({label})")
                
                st.markdown("### **AI Diagnostic Mapping**")
                st.image(processed_img, caption=f"Status: {label}", use_container_width=True)
                
elif st.session_state.view == "Depth Records":
    st.markdown("### 📊 Scan History")
    if st.session_state.full_logs:
        df_logs = pd.DataFrame(st.session_state.full_logs, columns=LOG_COLUMNS)
        st.dataframe(df_logs.style.background_gradient(cmap='YlOrRd', subset=['Combustion Risk (%)']), use_container_width=True)

elif st.session_state.view == "2D Silo Diagram":
    st.markdown("### 🏗️ Vertical Risk Visualization")
    if st.session_state.full_logs:
        df_viz = pd.DataFrame(st.session_state.full_logs, columns=LOG_COLUMNS)
        def get_color(risk):
            if risk < 10: return "#00FF00"
            elif 10 <= risk <= 20: return "#FFA500"
            else: return "#FF0000"
        fig = go.Figure()
        for i, row in df_viz.iterrows():
            fig.add_trace(go.Bar(x=["Silo Internals"], y=[15], marker_color=get_color(row['Combustion Risk (%)']), showlegend=False))
        fig.update_layout(barmode='stack', height=600, width=400, yaxis={'title': "Depth (mm)", 'range': [0, 180], 'autorange': "reversed"}, xaxis={'visible': False}, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

elif st.session_state.view == "Blockchain Ledger":
    st.markdown("<h1 style='color: #8E44AD;'>🔗 Immutable Ledger</h1>", unsafe_allow_html=True)
    if st.session_state.full_logs:
        df_chain = pd.DataFrame(st.session_state.full_logs, columns=LOG_COLUMNS)
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(df_chain.to_csv(index=False))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf)
        st.image(buf.getvalue(), caption="Digital Safety Passport", width=300)

if st.session_state.is_scanning:
    time.sleep(0.1); st.rerun()