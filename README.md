# 🛡️ SiloGuard AI Pro  
### Industrial Grain Monitoring & Safety Ecosystem

**SiloGuard AI Pro** is an advanced, end-to-end monitoring solution designed to provide a **digital twin of silo health**.  
By combining IoT sensor arrays with computer vision, it focuses on:

- 🔥 Early combustion detection  
- 👷 Worker safety monitoring  
- 🌾 Biological purity analysis  

---

## 📸 System Preview

![SiloGuard Dashboard](webpage_image.png)

---

# 🏗️ System Architecture

SiloGuard AI Pro is built on a **four-pillar architecture** that ensures seamless data flow from the physical silo to a blockchain-secured dashboard.

---

## 1️⃣ Hardware Integration Layer

The system communicates with an **Arduino / ESP32 sensor array** via Serial communication (COM21).

### 🔎 Sensors Integrated:

- **Ultrasonic Sensors** → Grain depth & volume tracking  
- **DHT22** → Temperature & humidity monitoring  
- **MQ-Series Gas Sensors** → VOC detection  
- **Smartphone (USB-C via Camo/DroidCam)** → High-fidelity vision sensor  

---

## 2️⃣ Vision & Analysis Layer (CNN-Inspired)

The vision system simulates CNN behavior through structured image-processing pipelines.

### 🧠 Processing Steps:

- **Gaussian Pre-processing**  
  Eliminates geometric noise from natural kernel shadows  

- **Laplacian Feature Extraction**  
  Detects fuzzy, low-frequency mold textures  

- **HSV Gating**  
  Confirms infected grain color spectrum (desaturated green/grey)  

- **Biological Density Index (BDI)**  
  Proprietary metric calculating infected surface percentage  
  → Final Grain Grade (A–F)

---

## 3️⃣ Data Processing & Machine Learning

- 🔥 **Combustion Prediction Model**  
  Scikit-learn model (`silo_model.pkl`) predicts spontaneous combustion risk  

- 📊 **Dynamic Risk Scoring**  
  Real-time gauges visualize:
  - Worker Health Risk
  - VOC Index
  - Temperature Index

---

## 4️⃣ Security & Compliance (Blockchain Ledger)

- 🔐 Immutable Scan Logs  
- 📁 Structured DataFrame Storage  
- 📲 QR Code Digital Safety Passport  
  Inspectors can verify silo history through encrypted QR verification  

---

# 🚀 Dashboard Modules

---

## 📊 Command Center

- Live Arduino telemetry  
- Metric card UI  
- Auto-updating risk gauges  
- Real-time gas and combustion indicators  

---

## 👷 Worker Safety Analysis

- Environmental hazard detection  
- VOC + Temperature combined risk index  
- Actionable Guidance:
  - ✅ Safe  
  - ⚠ Warning  
  - 🚨 Danger  

---

## 👁️ AI Surface Vision (USB Camo Mode)

Primary diagnostic interface.

### Features:

- 🖥 Dual View Display  
  - Raw Camera Feed  
  - AI Diagnostic Mapping  

- 🎯 Circular Targeted Capture  
  Focuses on grain center  
  Ignores metallic silo walls  

- 🌫 Reflection Logic  
  Detects matte zones indicating biological growth  

---

## 🏗️ 2D Vertical Silo Diagram

Stacked-bar visualization representing:

- Internal silo layers  
- Depth-based combustion risk  
- Color-coded risk segmentation  

---

# 🛠 Installation & Configuration

---

## 📦 Prerequisites

- Python 3.9+
- Arduino USB Drivers
- Camo Studio / DroidCam Desktop Client
- Required Python Libraries:
  ```bash
  pip install numpy opencv-python pandas scikit-learn matplotlib qrcode streamlit


### Dependencies
```bash
pip install streamlit opencv-python numpy pandas plotly joblib qrcode pillow pyserial
