# SiloGuard AI: Early Combustion & Worker Health Ecosystem 🌾🛡️

**SiloGuard AI** is a state-of-the-art preventive safety system for grain storage. It combines **IoT Moving Probes**, **Machine Learning**, and **Digital Twin** technology to predict spontaneous combustion and protect workers from hazardous gases.

## 🌟 Core Concepts

### 1. Moving Sensor Technology (3D Profiling)
Unlike traditional static sensors, our system uses a motorized **Vertical Probe**. By moving through the grain mass, it creates a 3D profile of temperature and gas levels, identifying deep-seated "Hot Spots" that surface sensors miss.

### 2. Digital Twin Visualization
The dashboard acts as a **Digital Twin** of the silo. It maps real-time data onto a 3D virtual space, allowing operators to visualize exactly where a thermal anomaly is located within the grain bulk.

### 3. 72-Hour Risk Prediction
Our AI analyzes the **Rate of Change** ($\Delta T$) and the **Chemical Signature** (CO/VOC fusion) to provide a 72-hour early warning window, allowing for preventive grain aeration before a fire starts.

### 4. Worker Health Risk Index (WHRI)
A proprietary algorithm translates complex gas and thermal data into a 0-100 safety score, alerting workers to dangerous CO levels or heat stress before they enter the facility.

## 💻 Technical Requirements

### Software Environment
* **Python Version:** Python 3.9, 3.10, or 3.11 (Recommended).
* **Operating System:** Windows 10/11, macOS, or Linux (Ubuntu/Debian).
* **Core Libraries:** * `Streamlit`: Web Interface & Dashboard.
    * `Scikit-Learn`: Machine Learning (Random Forest).
    * `Pandas`: Data Manipulation.
    * `Plotly`: 3D Interactive Visualizations.
    * `Joblib`: Model Serialization.

### Hardware Specifications (Planned Deployment)
* **Microcontroller:** ESP32-WROOM-32 (Dual-core for simultaneous sensing and transmission).
* **Gas Sensors:** * **MQ-7:** For Carbon Monoxide (CO).
    * **MQ-135:** For Volatile Organic Compounds (VOCs).
* **Thermal Sensors:** **DHT22** or **DS18B20** (Waterproof probe).
* **Motion:** **NEMA 17 Stepper Motor** + **A4988 Driver** for vertical movement logic.

## 🧪 Simulation & Synthetic Data
To ensure accuracy without burning real grain, we utilized:
* **Synthetic Data Generation:** 5,500+ samples simulated using grain combustion physics.
* **Hardware-in-the-Loop Simulator:** A built-in `SiloProbeSimulator` that mimics real-time IoT sensor drift and noise for software testing.


## 📂 Project Structure
```text
SiloGuard-AI/
├── app.py                # Streamlit Web Dashboard
├── train_model.py        # ML Training Script
├── silo_sensor_data.csv  # Synthetic Dataset
├── models/
│   └── silo_risk_model.joblib # Trained AI Brain
├── src/
│   ├── ml/
│   │   ├── health_logic.py    # WHRI Algorithm
│   │   └── preprocessing.py   # Feature Engineering
│   └── sim/
│       └── sensor_simulator.py # Hardware Simulator
└── hardware/
    └── silo_probe.ino    # ESP32 Firmware
```

## 🚦 Installation & Quick Start

Follow these steps to download and run the project locally.

### 1. Clone the Project
```bash
git clone [https://github.com/your-username/SiloGuard-AI.git](https://github.com/your-username/SiloGuard-AI.git)
cd SiloGuard-AI
