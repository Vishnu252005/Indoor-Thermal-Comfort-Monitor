import streamlit as st
import pandas as pd
import numpy as np
import time
from pythermalcomfort.models import pmv_ppd_iso

# Generate dummy sensor data
def generate_dummy_data():
    return {
        'air_temperature': np.random.uniform(22, 35),     # °C
        'relative_humidity': np.random.uniform(30, 80),   # %
        'air_velocity': np.random.uniform(0.1, 0.5),       # m/s
        'mean_radiant_temp': np.random.uniform(22, 35),   # °C
        'met': 1.2,        # metabolic rate (seated activity)
        'clo': 0.5         # clothing insulation (summer clothes)
    }

# Streamlit App
st.title("🔵 Indoor Thermal Comfort Monitor (Simulation)")
placeholder = st.empty()

# Simulate streaming
for i in range(30):  # simulate 30 readings
    data = generate_dummy_data()
    
    # PMV and PPD Calculation using ISO standard
    result = pmv_ppd_iso(
        tdb=data['air_temperature'],
        tr=data['mean_radiant_temp'],
        vr=data['air_velocity'],
        rh=data['relative_humidity'],
        met=data['met'],
        clo=data['clo'],
        model="7730-2005"  # Using ISO 7730:2005 standard
    )

    # Update dashboard
    with placeholder.container():
        st.metric("🌡️ Air Temp (°C)", f"{data['air_temperature']:.1f}")
        st.metric("💧 Humidity (%)", f"{data['relative_humidity']:.1f}")
        st.metric("💨 Air Speed (m/s)", f"{data['air_velocity']:.2f}")
        st.metric("🔥 PMV", f"{result.pmv:.2f}")
        st.metric("🚨 PPD (%)", f"{result.ppd:.1f}")
        
        if result.pmv > 0.5 or result.ppd > 10:
            st.error("⚠️ Thermal discomfort detected!")

    time.sleep(1)  # simulate 1-second interval
    placeholder.empty()
