
import streamlit as st
import pandas as pd
import plotly.express as px
import random
from io import StringIO

st.set_page_config(page_title='Warehouse Mapper', layout='wide')
st.title("US Warehouse Mapper (Plotly Edition)")

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
        color_palette = px.colors.qualitative.Dark24
        random.shuffle(color_palette)
        oem_colors = {oem: color_palette[i % len(color_palette)] for i, oem in enumerate(unique_oems)}
        df['color'] = df['type'].map(oem_colors)

        # Show OEM legend
        st.subheader("OEM Legend")
        for oem, color in oem_colors.items():
            st.markdown(f"<span style='color:{color}'>●</span> {oem}", unsafe_allow_html=True)

        # Plotly map
        fig = px.scatter_geo(
            df,
            lat='lat',
            lon='long',
            color='type',
            hover_name='type',
            color_discrete_map=oem_colors,
            scope='usa',
            title='Mapped Warehouses by OEM'
        )
        fig.update_traces(marker=dict(size=8))
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Please upload a CSV file to view warehouse locations.")
