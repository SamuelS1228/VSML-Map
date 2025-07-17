
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import random

st.set_page_config(page_title="Warehouse Mapper", layout="wide")
st.title("US Warehouse Mapper")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

# Use session state to prevent infinite refresh loop
if 'uploaded' not in st.session_state:
    st.session_state.uploaded = False

if uploaded_file and not st.session_state.uploaded:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.lower()

        # Check required columns
        if not all(col in df.columns for col in ['lat', 'long', 'type']):
            st.error("File must have columns: 'lat' in column A, 'long' in column B, and 'type' in column C (OEM name).")
        else:
            st.session_state.uploaded = True
            st.session_state.df = df
    except Exception as e:
        st.error(f"Error loading file: {e}")

if st.session_state.uploaded:
    df = st.session_state.df
    st.success(f"Loaded {len(df)} warehouse locations.")

    unique_oems = df['type'].unique()
    color_palette = [
        'red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
        'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
        'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray'
    ]
    random.shuffle(color_palette)
    oem_colors = {oem: color_palette[i % len(color_palette)] for i, oem in enumerate(unique_oems)}

    # Display legend
    st.subheader("OEM Legend")
    for oem, color in oem_colors.items():
        st.markdown(f"<span style='color:{color}'>●</span> {oem}", unsafe_allow_html=True)

    # Initialize Folium Map
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        lat, lon, oem = row['lat'], row['long'], row['type']
        color = oem_colors.get(oem, "gray")
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color=color,
            fill=True,
            fill_opacity=0.8,
            popup=f"OEM: {oem}"
        ).add_to(marker_cluster)

    st_data = st_folium(m, width=1000, height=600)
else:
    st.info("Please upload an Excel file to view warehouse locations.")
