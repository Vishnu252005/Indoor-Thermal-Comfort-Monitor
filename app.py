import streamlit as st
import pandas as pd
import numpy as np
import time
import math
import altair as alt
from datetime import datetime
import json
import io
import qrcode
from PIL import Image
from pythermalcomfort.models import pmv_ppd_iso
import socket
import random
from utils.helpers import get_local_ip, generate_qr_code, save_session_data, load_session_data, get_current_time

# Sensor Interface Integration (Commented out - Uncomment when using physical sensors)
# from sensors.sensor_interface import SensorInterface
# sensor = SensorInterface(port='COM3')  # Change port as needed
# sensor_connected = False

# Set page config for better layout
st.set_page_config(
    page_title="Thermal Comfort Monitor",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    /* Removed .stMetric background-color for theme compatibility */
    .stMetric {
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        height: 3em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #4CAF50;
        color: white;
        transition: all 0.3s ease;
    }
    .css-1d391kg {
        padding: 1rem;
    }
    .stAlert {
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for history
if 'pmv_history' not in st.session_state:
    st.session_state.pmv_history = []
if 'ppd_history' not in st.session_state:
    st.session_state.ppd_history = []
if 'timestamp_history' not in st.session_state:
    st.session_state.timestamp_history = []
if 'user_notes' not in st.session_state:
    st.session_state.user_notes = ""
if 'session_start' not in st.session_state:
    st.session_state.session_start = datetime.now()
if 'feedback_counts' not in st.session_state:
    st.session_state.feedback_counts = {'Too Cold': 0, 'Comfortable': 0, 'Too Hot': 0}

# Detect local IP address for QR code
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
except Exception:
    local_ip = "localhost"

# Sidebar styling and organization
with st.sidebar:
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sensor Connection Section (Commented out - Uncomment when using physical sensors)
    """
    st.markdown("### 🔌 Sensor Connection")
    with st.expander("Connect Sensors", expanded=True):
        if st.button("Connect to Sensors"):
            sensor_connected = sensor.connect()
            if sensor_connected:
                st.success("✅ Connected to sensors successfully!")
            else:
                st.error("❌ Failed to connect to sensors")
        
        if sensor_connected:
            if st.button("Disconnect Sensors"):
                sensor.disconnect()
                sensor_connected = False
                st.info("Sensors disconnected")
            
            # Read sensor data
            sensor_data = sensor.read_sensors()
            if sensor_data:
                st.markdown("#### 📊 Sensor Readings")
                st.write(f"Air Temperature: {sensor_data['air_temperature']:.1f}°C")
                st.write(f"Relative Humidity: {sensor_data['relative_humidity']:.1f}%")
                st.write(f"Air Velocity: {sensor_data['air_velocity']:.2f} m/s")
                st.write(f"Mean Radiant Temp: {sensor_data['mean_radiant_temp']:.1f}°C")
                
                # Update environmental parameters with sensor data
                air_temperature = sensor_data['air_temperature']
                relative_humidity = sensor_data['relative_humidity']
                air_velocity = sensor_data['air_velocity']
                mean_radiant_temp = sensor_data['mean_radiant_temp']
    """
    
    # Real-time clock with better styling
    st.markdown(f"""
        <div style='background-color: #4CAF50; color: white; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
            <h3 style='margin: 0;'>Current Time</h3>
            <p style='margin: 0; font-size: 1.2rem;'>{get_current_time()}</p>
        </div>
    """, unsafe_allow_html=True)

    # QR Code for Network Access
    st.markdown("### 📱 Mobile Access")
    try:
        network_url = f"http://{get_local_ip()}:8501"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(network_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        qr_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Display QR code with just the caption "Scan to access"
        st.image(img_byte_arr, caption="Scan to access", use_container_width=True)
        st.info("Scan this QR code with your mobile device to access the app on your local network.")
    except Exception as e:
        st.error(f"Could not generate QR code: {str(e)}")

    # User notes with better styling
    st.markdown("### 📝 Session Notes")
    st.session_state.user_notes = st.text_area("Add your notes for this session:", st.session_state.user_notes, height=100)

    # Environmental Parameters with better organization
    st.markdown("### 🌍 Environmental Parameters")
    with st.expander("Adjust Parameters", expanded=True):
        air_temperature = st.slider('Air Temperature (°C)', 15.0, 30.0, 27.0, 0.1)
        mean_radiant_temp = st.slider('Mean Radiant Temp (°C)', 15.0, 30.0, 27.0, 0.1)
        relative_humidity = st.slider('Relative Humidity (%)', 10.0, 90.0, 50.0, 0.1)
        air_velocity = st.slider('Air Velocity (m/s)', 0.05, 1.0, 0.1, 0.01)
        met = st.slider('Metabolic Rate (met)', 0.8, 2.0, 1.2, 0.01)
        clo = st.slider('Clothing Insulation (clo)', 0.3, 1.5, 0.5, 0.01)

    # Comfort Thresholds with better organization
    st.markdown("### 🎯 Comfort Thresholds")
    with st.expander("Set Thresholds", expanded=True):
        comfort_pmv_min = st.number_input('Min PMV for Comfort', value=-0.5, step=0.01, format="%.2f")
        comfort_pmv_max = st.number_input('Max PMV for Comfort', value=0.5, step=0.01, format="%.2f")
        comfort_ppd_max = st.number_input('Max PPD (%) for Comfort', value=10.0, step=0.1, format="%.1f")

    # App Customization
    st.markdown("### 🎨 App Customization")
    with st.expander("Customize App", expanded=True):
        custom_title = st.text_input("App Title", value="🔵 Indoor Thermal Comfort Monitor")
        custom_subtitle = st.text_input("Subtitle", value="Monitor and analyze indoor comfort in real time")
        session_tag = st.text_input("Session Tag", value="")
        session_tag_color = st.color_picker("Tag Color", value="#4CAF50")

    # Session Management
    st.markdown("### 💾 Session Management")
    with st.expander("Manage Session", expanded=True):
        col_save, col_load = st.columns(2)
        with col_save:
            if st.button("💾 Save Session"):
                session_data = {
                    'pmv_history': st.session_state.get('pmv_history', []),
                    'ppd_history': st.session_state.get('ppd_history', []),
                    'timestamp_history': st.session_state.get('timestamp_history', []),
                    'user_notes': st.session_state.get('user_notes', ""),
                    'session_start': str(st.session_state.get('session_start', datetime.now())),
                    'custom_title': custom_title,
                    'custom_subtitle': custom_subtitle,
                    'session_tag': session_tag,
                    'session_tag_color': session_tag_color,
                    'air_temperature': air_temperature,
                    'mean_radiant_temp': mean_radiant_temp,
                    'relative_humidity': relative_humidity,
                    'air_velocity': air_velocity,
                    'met': met,
                    'clo': clo,
                    'comfort_pmv_min': comfort_pmv_min,
                    'comfort_pmv_max': comfort_pmv_max,
                    'comfort_ppd_max': comfort_ppd_max
                }
                json_str = json.dumps(session_data)
                st.download_button("📥 Download Session", data=json_str, file_name="session.json", mime="application/json")
        with col_load:
            uploaded_file = st.file_uploader("📤 Load Session", type=["json"])
            if uploaded_file is not None:
                loaded_data = json.load(uploaded_file)
                st.session_state.pmv_history = loaded_data.get('pmv_history', [])
                st.session_state.ppd_history = loaded_data.get('ppd_history', [])
                st.session_state.timestamp_history = loaded_data.get('timestamp_history', [])
                st.session_state.user_notes = loaded_data.get('user_notes', "")
                st.session_state.session_start = datetime.now()
                st.success("✅ Session loaded successfully!")

# Main content area
# Stylish header with gradient background
st.markdown(f"""
    <div style='background:linear-gradient(90deg,{session_tag_color},#222 80%);padding:2rem;border-radius:1rem;margin-bottom:2rem;'>
        <h1 style='color:white;margin-bottom:0.5rem;'>{custom_title}</h1>
        <p style='color:white;font-size:1.2rem;margin-bottom:0;'>{custom_subtitle}</p>
        <span style='float:right;background:{session_tag_color};color:white;padding:0.5rem 1rem;border-radius:0.5rem;font-weight:bold;margin-top:-2.5rem;'>{session_tag}</span>
    </div>
""", unsafe_allow_html=True)

# Create three columns for metrics
col1, col2, col3 = st.columns(3)

# PMV and PPD Calculation
result = pmv_ppd_iso(
    tdb=air_temperature,
    tr=mean_radiant_temp,
    vr=air_velocity,
    rh=relative_humidity,
    met=met,
    clo=clo,
    model="7730-2005"
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
    st.session_state.pmv_history.append(pmv)
    st.session_state.ppd_history.append(ppd)
    st.session_state.timestamp_history.append(datetime.now().strftime('%H:%M:%S'))
    if len(st.session_state.pmv_history) > 30:
        st.session_state.pmv_history.pop(0)
        st.session_state.ppd_history.pop(0)
        st.session_state.timestamp_history.pop(0)

# Display metrics in columns with better styling
with col1:
    st.metric("🌡️ Air Temperature", f"{air_temperature:.1f}°C")
    st.metric("💧 Humidity", f"{relative_humidity:.1f}%")
with col2:
    st.metric("🔥 PMV", pmv_display)
    st.metric("🚨 PPD", f"{ppd_display}%")
with col3:
    st.metric("💨 Air Speed", f"{air_velocity:.2f} m/s")
    st.metric("⏱️ Session Duration", str(datetime.now() - st.session_state.session_start).split('.')[0])

# Comfort status with better styling
if not math.isnan(pmv):
    if pmv < comfort_pmv_min or pmv > comfort_pmv_max or ppd > comfort_ppd_max:
        st.error("⚠️ Thermal discomfort detected!")
        recommendations = []
        if pmv < comfort_pmv_min:
            recommendations.append("• Increase air temperature or clothing insulation")
            recommendations.append("• Reduce air speed")
        elif pmv > comfort_pmv_max:
            recommendations.append("• Decrease air temperature or clothing insulation")
            recommendations.append("• Increase air speed")
        if ppd > comfort_ppd_max:
            recommendations.append("• Adjust humidity levels if possible")
        st.info("**Recommendations:**\n" + "\n".join(recommendations))
    else:
        st.success("✅ Thermal comfort zone achieved!")

# Charts section with better organization
st.markdown("### 📊 Comfort Analysis")
tab1, tab2, tab3 = st.tabs(["History", "Comfort Timeline", "Statistics"])

with tab1:
    if len(st.session_state.pmv_history) > 1:
        chart_data = pd.DataFrame({
            'Timestamp': st.session_state.timestamp_history,
            'PMV': st.session_state.pmv_history,
            'PPD': st.session_state.ppd_history
        })
        
        # PMV Chart
        pmv_chart = alt.Chart(chart_data).mark_line(color='orange').encode(
            x='Timestamp',
            y=alt.Y('PMV', scale=alt.Scale(domain=[-2, 2]))
        ).properties(
            title='PMV History',
            height=300
        )
        
        # PPD Chart
        ppd_chart = alt.Chart(chart_data).mark_line(color='pink').encode(
            x='Timestamp',
            y=alt.Y('PPD', scale=alt.Scale(domain=[0, 100]))
        ).properties(
            title='PPD History',
            height=300
        )
        
        st.altair_chart(pmv_chart, use_container_width=True)
        st.altair_chart(ppd_chart, use_container_width=True)

with tab2:
    if len(st.session_state.pmv_history) > 0:
        comfort_status = [
            "Comfort" if (comfort_pmv_min <= pmv <= comfort_pmv_max and ppd <= comfort_ppd_max) else "Discomfort"
            for pmv, ppd in zip(st.session_state.pmv_history, st.session_state.ppd_history)
        ]
        timeline_df = pd.DataFrame({
            'Timestamp': st.session_state.timestamp_history,
            'Status': comfort_status
        })
        color_map = {"Comfort": "#4CAF50", "Discomfort": "#F44336"}
        timeline_df['Color'] = timeline_df['Status'].map(color_map)
        
        st.markdown("**Comfort Timeline:**")
        st.write(
            "".join([
                f'<span style="display:inline-block;width:20px;height:20px;background:{color};margin-right:3px;border-radius:4px;"></span>'
                for color in timeline_df['Color']
            ]),
            unsafe_allow_html=True
        )

with tab3:
    if len(st.session_state.pmv_history) > 0:
        stats_df = pd.DataFrame({
            'PMV': st.session_state.pmv_history,
            'PPD': st.session_state.ppd_history
        })
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("PMV Statistics", 
                     f"Min: {stats_df['PMV'].min():.2f}\nMax: {stats_df['PMV'].max():.2f}\nAvg: {stats_df['PMV'].mean():.2f}")
        with col2:
            st.metric("PPD Statistics",
                     f"Min: {stats_df['PPD'].min():.1f}%\nMax: {stats_df['PPD'].max():.1f}%\nAvg: {stats_df['PPD'].mean():.1f}%")
        
        # Comfort vs Discomfort Pie Chart
        comfort_counts = pd.Series(comfort_status).value_counts()
        pie_chart = alt.Chart(pd.DataFrame({
            'Status': comfort_counts.index,
            'Count': comfort_counts.values
        })).mark_arc(innerRadius=50).encode(
            theta='Count',
            color=alt.Color('Status:N', scale=alt.Scale(domain=["Comfort", "Discomfort"], range=["#4CAF50", "#F44336"]))
        ).properties(
            title="Comfort vs Discomfort Proportion",
            height=300
        )
        st.altair_chart(pie_chart, use_container_width=True)

# Help section with better styling
with st.expander("ℹ️ Help & Instructions", expanded=False):
    st.markdown("""
        ### How to use this app:
        1. **Adjust Parameters**: Use the sidebar to set environmental and personal parameters
        2. **Monitor Comfort**: View real-time PMV/PPD metrics and comfort status
        3. **Analyze Data**: Check the charts and statistics for detailed analysis
        4. **Save/Load**: Save your session data or load previous sessions
        
        ### Understanding the Metrics:
        - **PMV (Predicted Mean Vote)**: 
          - Range: -3 (cold) to +3 (hot)
          - Comfort zone: -0.5 to +0.5
        
        - **PPD (Predicted Percentage of Dissatisfied)**:
          - Range: 0% to 100%
          - Comfort threshold: < 10%
    """)

# Footer with better styling
st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #666;'>
        <p>Built with ❤️ using Streamlit | Thermal Comfort Monitor v1.0</p>
    </div>
""", unsafe_allow_html=True)

# --- User Feedback Poll ---
st.markdown("### 🗳️ User Comfort Feedback")
feedback_col1, feedback_col2 = st.columns([2, 3])
with feedback_col1:
    feedback = st.radio("How do you feel right now?", ["Too Cold", "Comfortable", "Too Hot"], horizontal=True)
    if st.button("Submit Feedback"):
        st.session_state.feedback_counts[feedback] += 1
        st.success("Thank you for your feedback!")
with feedback_col2:
    feedback_df = pd.DataFrame({
        'Feedback': list(st.session_state.feedback_counts.keys()),
        'Count': list(st.session_state.feedback_counts.values())
    })
    feedback_pie = alt.Chart(feedback_df).mark_arc(innerRadius=40).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color("Feedback:N", scale=alt.Scale(domain=["Too Cold", "Comfortable", "Too Hot"], range=["#2196F3", "#4CAF50", "#F44336"]))
    ).properties(title="Live Comfort Feedback")
    st.altair_chart(feedback_pie, use_container_width=True)
