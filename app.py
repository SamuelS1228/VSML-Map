import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from io import BytesIO
import random

st.set_page_config(page_title="Warehouse Mapper", layout="wide")
st.title("US Warehouse Mapper")

# Upload file and save bytes in session state
if "file_data" not in st.session_state:
    st.session_state.file_data = None

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None and st.session_state.file_data is None:
    st.session_state.file_data = uploaded_file.read()

# Only render map once file is uploaded and cached
if st.session_state.file_data is not None:
    df = pd.read_excel(BytesIO(st.session_state.file_data))
    df.columns = df.columns.str.lower()

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

        # OEM Legend
        st.subheader("OEM Legend")
        for oem, color in oem_colors.items():
            st.markdown(f"<span style='color:{color}'>●</span> {oem}", unsafe_allow_html=True)

        # Folium Map
        m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row['lat'], row['long']],
                radius=5,
                color=oem_colors.get(row['type'], 'gray'),
                fill=True,
                fill_opacity=0.8,
                popup=f"OEM: {row['type']}"
            ).add_to(marker_cluster)

        st_folium(m, width=1000, height=600)

else:
    st.info("Please upload an Excel file to view warehouse locations.")
