# 🛡️ SiloGuard AI Pro: Industrial Grain Monitoring & Safety Ecosystem

**SiloGuard AI Pro** is an advanced, end-to-end monitoring solution designed to provide a "digital twin" of silo health. By combining IoT sensor arrays with computer vision, it focuses on early combustion detection, worker safety, and biological purity.

![Image Alt][(Screenshot 2026-01-20 160349.png)](Screenshot 2026-01-20 160349.png)
---

## 🏗️ System Architecture

The project is built on a four-pillar architecture that ensures data flows from the physical silo to a blockchain-secured dashboard.

### 1. Hardware Integration Layer
The system communicates with an Arduino/ESP32 sensor array via Serial communication (COM21).
* **Depth Measurement:** Ultrasonic sensors track grain levels and remaining volume.
* **Atmospheric Monitoring:** DHT22 and MQ-series sensors monitor heat, moisture, and VOCs (Volatile Organic Compounds).
* **Vision Sensor:** A smartphone serves as the primary vision sensor, connected via **USB-C** and bridged through **Camo** to act as a high-fidelity webcam.

### 2. Vision & Analysis Layer (CNN-Inspired)
The core analysis has evolved from simple color-math to a pattern-recognition model that simulates the behavior of a Convolutional Neural Network (CNN).
* **Gaussian Pre-processing:** Smoothes the image to eliminate the sharp "geometric noise" caused by natural shadows between healthy grain kernels.
* **Laplacian Feature Extraction:** A high-pass filter that identifies "low-frequency blobs" and fuzzy textures characteristic of mold growth.
* **HSV Gating:** Confirms the color of detected textures falls within the specific desaturated green/grey spectrum identified in infected grain samples.
* **Biological Density Index (BDI):** A proprietary metric that calculates the percentage of the grain surface infected to determine the final Grade (A-F).

### 3. Data Processing & Machine Learning
* **Combustion Prediction:** A Scikit-learn model (`silo_model.pkl`) processes telemetry to predict spontaneous combustion risks.
* **Risk Scoring:** Dynamic gauges visualize "Worker Health Risk" based on combined VOC and Temperature indices.

### 4. Security & Compliance (Blockchain Ledger)
* **Immutable Logs:** Every scan is logged into a structured dataframe.
* **QR Generation:** A digital safety passport is generated for every session, allowing inspectors to verify silo history via an encrypted QR code.

---

## 🚀 Dashboard Modules

### 📊 Command Center
Displays real-time telemetry from the Arduino. It features a "Metric Card" UI with auto-updating gauges for combustion risk and gas levels.

### 👷 Worker Safety Analysis
A dedicated safety suite that analyzes environmental hazards. It provides actionable guidance (Safe, Warning, or Danger) based on real-time atmospheric data.

### 👁️ AI Surface Vision (USB Camo Mode)
The primary diagnostic interface featuring:
* **Dual-View Display:** Shows the **Raw Captured Feed** (what the phone sees) side-by-side with the **AI Diagnostic Mapping**.
* **Targeted Region Capture:** Uses a circular gate to focus analysis on the grain center, ignoring metallic silo walls.
* **Reflection Logic:** Detects surface "matte" zones where biological growth has replaced the natural reflection of healthy grain.

### 🏗️ 2D Vertical Diagram
A stacked-bar visualization that represents the internal layers of the silo, color-coded by the combustion risk detected at various depths during the scan.

---

## 🛠️ Installation & Configuration

### Prerequisites
* **Python:** 3.9 or higher.
* **Drivers:** Arduino USB drivers and Camo/DroidCam desktop client.

### Dependencies
```bash
pip install streamlit opencv-python numpy pandas plotly joblib qrcode pillow pyserial
