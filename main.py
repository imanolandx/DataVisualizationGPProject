import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from PIL import Image
import os

import base64
from io import BytesIO

import aggVsOut

def img_to_base64(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_data = buf.getvalue()
    return base64.b64encode(byte_data).decode()
st.set_page_config(page_title="F1 Data Visualization", layout="wide")
st.title("🏎️ Formula 1 Data Visualizations")

# Dropdown navigation
page = st.selectbox("Select a page:", ["Home (Circuits)", "Aggression vs Outcome Correlation"])

# Load data
if page == "Home (Circuits)":
    csv_path = 'Data/circuit_locations.csv'
    image_folder = 'selected_f1_circuit_images'
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=["latitude", "longitude"])

# Streamlit setup
    st.markdown("Hover over a red dot to see the circuit name. Use the dropdown to zoom into a specific one.")

# Dropdown
    track_names = sorted(df['track'].unique())
    selected_track = st.selectbox("Select a circuit to zoom into", ["Show All"] + track_names)

# Layout: create 2 columns
    col1, col2 = st.columns([2, 1])  # Wider map, narrower image

# --- Column 1: MAP ---
    with col1:
        if selected_track == "Show All":
            m = folium.Map(location=[10, 10], zoom_start=2, scrollWheelZoom=False, dragging=False, zoom_control=False)
            for _, row in df.iterrows():
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=2,
                    color='red',
                    fill=True,
                    fill_opacity=0.8,
                    tooltip=row['track']
                ).add_to(m)
        else:
            selected_row = df[df['track'] == selected_track].iloc[0]
            lat, lon = selected_row['latitude'], selected_row['longitude']
            m = folium.Map(
                location=[lat, lon],
                zoom_start=14,
                tiles='OpenStreetMap',  # Ensures visible background
                scrollWheelZoom=False,
                dragging=False,
                zoom_control=False
            )

        # Marker at the center
            folium.CircleMarker(
                location=[lat, lon],
                radius=6,
                color='blue',
                fill=True,
                fill_opacity=0.9,
                tooltip=selected_track
            ).add_to(m)
    
        st_folium(m, width=800, height=550)

    with col2:
        if selected_track != "Show All":
            filename_base = selected_track.replace(" ", "_").replace("/", "_")
            png_path = os.path.join(image_folder, f"{filename_base}.png")
            svg_path = os.path.join(image_folder, f"{filename_base}.svg")

            with st.container():
                # Fake a white background using an image wrapper
                st.markdown("### 🗺️ Circuit Layout")
                
                if os.path.exists(png_path):
                    img = Image.open(png_path)
                    
                    # Put white background behind the image using markdown
                    st.markdown(
                        f"""
                        <div style='
                            background-color: white;
                            padding: 20px;
                            border-radius: 10px;
                            text-align: center;
                            box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
                        '>
                            <p style='color:black;'>Image size: {img.width} × {img.height} px</p>
                            <img src='data:image/png;base64,{img_to_base64(img)}' width='100%'/>
                            <p style='color:black;'>{selected_track}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                elif os.path.exists(svg_path):
                    with open(svg_path, "r", encoding="utf-8") as f:
                        svg_code = f.read()
                    st.components.v1.html(svg_code, height=500, scrolling=False)
                else:
                    st.warning("⚠️ No layout image found for this circuit.")
elif page == "Aggression vs Outcome Correlation":
    aggVsOut.render() 
