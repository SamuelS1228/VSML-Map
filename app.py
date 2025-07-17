
import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import random

st.set_page_config(page_title="Warehouse Mapper", layout="wide")
st.title("US Warehouse Mapper (Mapbox Edition)")

if 'csv_data' not in st.session_state:
    st.session_state.csv_data = None

uploaded_file = st.file_uploader("Upload Warehouse CSV", type=["csv"])

if uploaded_file is not None and st.session_state.csv_data is None:
    st.session_state.csv_data = uploaded_file.getvalue().decode("utf-8")

if st.session_state.csv_data is not None:
    df = pd.read_csv(StringIO(st.session_state.csv_data))
    df.columns = df.columns.str.lower()

    if not all(col in df.columns for col in ['lat', 'long', 'type']):
        st.error("CSV must contain 'lat', 'long', and 'type' columns.")
    else:
        st.success(f"Loaded {len(df)} warehouse locations.")

        unique_oems = df['type'].unique()
        color_palette = px.colors.qualitative.Plotly
        random.shuffle(color_palette)
        oem_colors = {oem: color_palette[i % len(color_palette)] for i, oem in enumerate(unique_oems)}
        df['color'] = df['type'].map(oem_colors)

        st.subheader("OEM Legend")
        for oem, color in oem_colors.items():
            st.markdown(f"<span style='color:{color}'>●</span> {oem}", unsafe_allow_html=True)

        fig = px.scatter_mapbox(
            df,
            lat='lat',
            lon='long',
            color='type',
            color_discrete_map=oem_colors,
            zoom=3,
            height=650,
            hover_name='type'
        )
        fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_traces(marker=dict(size=9))

        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Please upload a CSV file to view warehouse locations.")
