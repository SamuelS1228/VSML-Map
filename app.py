
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import random
from io import BytesIO

st.set_page_config(page_title="Warehouse Mapper", layout="wide")
st.title("US Warehouse Mapper")

# File upload
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

# If uploaded, store contents in session_state as a DataFrame
if uploaded_file is not None and 'df' not in st.session_state:
    data = uploaded_file.read()
    df = pd.read_excel(BytesIO(data))
    df.columns = df.columns.str.lower()
    st.session_state.df = df

# Only proceed if a DataFrame is in session_state
if 'df' in st.session_state:
    df = st.session_state.df

    if not all(col in df.columns for col in ['lat', 'long', 'type']):
        st.error("Excel must contain 'lat', 'long', and 'type' columns.")
    else:
        st.success(f"Loaded {len(df)} warehouse locations.")

        unique_oems = df['type'].unique()
        color_palette = [
            'red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
            'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
            'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray'
        ]
        random.shuffle(color_palette)
        oem_colors = {oem: color_palette[i % len(color_palette)] for i, oem in enumerate(unique_oems)}

        st.subheader("OEM Legend")
        for oem, color in oem_colors.items():
            st.markdown(f"<span style='color:{color}'>●</span> {oem}", unsafe_allow_html=True)

        # Build map
        m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in df.iterrows():
            lat, lon, oem = row['lat'], row['long'], row['type']
            color = oem_colors.get(oem, 'gray')
            folium.CircleMarker(
                location=[lat, lon],
                radius=5,
                color=color,
                fill=True,
                fill_opacity=0.8,
                popup=f"OEM: {oem}"
            ).add_to(marker_cluster)

        st_folium(m, width=1000, height=600)

elif uploaded_file is None:
    st.info("Please upload an Excel file to view warehouse locations.")
