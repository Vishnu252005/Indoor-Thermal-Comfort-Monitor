import streamlit as st
import altair as alt
import pandas as pd
from datetime import datetime

def create_header(custom_title, custom_subtitle, session_tag, session_tag_color):
    """Create the app header with custom styling"""
    return f"""
        <div style='background:linear-gradient(90deg,{session_tag_color},#222 80%);padding:2rem;border-radius:1rem;margin-bottom:2rem;'>
            <h1 style='color:white;margin-bottom:0.5rem;'>{custom_title}</h1>
            <p style='color:white;font-size:1.2rem;margin-bottom:0;'>{custom_subtitle}</p>
            <span style='float:right;background:{session_tag_color};color:white;padding:0.5rem 1rem;border-radius:0.5rem;font-weight:bold;margin-top:-2.5rem;'>{session_tag}</span>
        </div>
    """

def create_metrics_display(air_temperature, relative_humidity, pmv_display, ppd_display, air_velocity, session_start):
    """Create the metrics display section"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🌡️ Air Temperature", f"{air_temperature:.1f}°C")
        st.metric("💧 Humidity", f"{relative_humidity:.1f}%")
    with col2:
        st.metric("🔥 PMV", pmv_display)
        st.metric("🚨 PPD", f"{ppd_display}%")
    with col3:
        st.metric("💨 Air Speed", f"{air_velocity:.2f} m/s")
        st.metric("⏱️ Session Duration", str(datetime.now() - session_start).split('.')[0])

def create_charts(pmv_history, ppd_history, timestamp_history, comfort_pmv_min, comfort_pmv_max, comfort_ppd_max):
    """Create the charts section"""
    if len(pmv_history) > 1:
        chart_data = pd.DataFrame({
            'Timestamp': timestamp_history,
            'PMV': pmv_history,
            'PPD': ppd_history
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
        
        return pmv_chart, ppd_chart
    return None, None

def create_feedback_section(feedback_counts):
    """Create the user feedback section"""
    feedback_df = pd.DataFrame({
        'Feedback': list(feedback_counts.keys()),
        'Count': list(feedback_counts.values())
    })
    
    feedback_pie = alt.Chart(feedback_df).mark_arc(innerRadius=40).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color("Feedback:N", scale=alt.Scale(
            domain=["Too Cold", "Comfortable", "Too Hot"],
            range=["#2196F3", "#4CAF50", "#F44336"]
        ))
    ).properties(title="Live Comfort Feedback")
    
    return feedback_pie 