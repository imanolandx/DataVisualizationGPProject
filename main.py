import streamlit as st
import pandas as pd

# Set up Streamlit page
st.set_page_config(page_title="F1 Aggression Analysis", layout="wide")
st.title("🏁 F1 Driver Aggression Analysis Portal")

# --- Sidebar navigation ---
st.sidebar.title("📂 Navigation")
st.sidebar.markdown("Select a page to explore:")

pages = [
    "🏠 Home",
    "🧠 Stint Management Strategies by Team/Driver",
    "🔥 Driver Aggression Patterns",
    "🔧 Tyre Compound Effectiveness vs. Aggression",
    "🎯 Aggression vs Outcome Correlation"
]
selected_page = st.sidebar.radio("Go to", pages)

# --- Main Page Logic ---
if selected_page == "🏠 Home":
    st.subheader("📊 Overview")
    st.markdown("""
    Welcome to the F1 Aggression Analysis Dashboard!  
    This interactive dashboard was developed as part of a Data Visualization course project.  
    It allows users to explore the strategic behaviors of F1 drivers and teams through aggression scores,
    stint lengths, tyre compounds, and race outcomes from 2018 until 2024.

    🔍 Key features include:
    - Visualizing driver aggression trends
    - Comparing tyre compound effectiveness
    - Understanding how aggression impacts results
    - Exploring team-level stint strategies

    ---
    """)

    # Contributors Section
    st.subheader("👨‍💻 Contributors")
    st.markdown("""
    - Imran Haqeem (Aggression vs Outcome Correlation)  
    - Yusuf Wafiy (Tyre Compound Effectiveness vs Aggression)  
    - Iman Kamil (Driver Aggression Patterns)  
    - Aqil Fauzan(Data Pre-processing and Documentation)  

    📍 Developed in Python using Streamlit, Matplotlib, Seaborn, and Folium.
    """)
else:
    st.info(f"🛠️ This page is under construction: {selected_page}")
