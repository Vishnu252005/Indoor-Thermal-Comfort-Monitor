import streamlit as st
import pandas as pd
import numpy as np
import time
import math
from pythermalcomfort.models import pmv_ppd_iso

# Generate dummy sensor data with clamped values
def generate_dummy_data():
    return {
        'air_temperature': np.clip(np.random.uniform(23, 30), 15, 30),     # °C, safe range
        'relative_humidity': np.clip(np.random.uniform(35, 70), 10, 90),   # %, safe range
        'air_velocity': np.clip(np.random.uniform(0.1, 0.3), 0.05, 1.0),   # m/s, safe range
        'mean_radiant_temp': np.clip(np.random.uniform(23, 30), 15, 30),   # °C, safe range
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

    pmv = result.pmv
    ppd = result.ppd

    # Handle nan values
    if math.isnan(pmv) or math.isnan(ppd):
        pmv_display = "Invalid input"
        ppd_display = "Invalid input"
    else:
        pmv_display = f"{pmv:.2f}"
        ppd_display = f"{ppd:.1f}"

    # Update dashboard
    with placeholder.container():
        st.metric("🌡️ Air Temp (°C)", f"{data['air_temperature']:.1f}")
        st.metric("💧 Humidity (%)", f"{data['relative_humidity']:.1f}")
        st.metric("💨 Air Speed (m/s)", f"{data['air_velocity']:.2f}")
        st.metric("🔥 PMV", pmv_display)
        st.metric("🚨 PPD (%)", ppd_display)
        
        if not math.isnan(pmv) and (pmv > 0.5 or ppd > 10):
            st.error("⚠️ Thermal discomfort detected!")

    time.sleep(1)  # simulate 1-second interval
    placeholder.empty()
