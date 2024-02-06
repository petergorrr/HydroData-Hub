import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import geopandas as gpd
import plotly.express as px


# Load data
df_reshaped = pd.read_csv('water_data.csv')


def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, geojson="Penang_PAR_2015.geojson",
                               color_continuous_scale=input_color_theme,
                               #    range_color=(0, max(df_selected_month.water_consumption)),
                               scope="asia",
                               locationmode="ISO-3",
                               labels={
                                   'water consumption(litres)': 'Water Consumption(litres)'}
                               )

    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth


def display_smart_water_meter_interface():

    # Sidebar
    with st.sidebar:
        st.title('Smart Water Meter System🚰')
        st.sidebar.image("images/smart_water_meter.jpg", use_column_width=True)
        st.sidebar.info(
            "The Smart Water Meter System provides real-time monitoring and analytics for water consumption. "
            "Track usage patterns, detect leaks, and make informed decisions for efficient water management."
        )

        month_list = list(df_reshaped.month.unique())[::-1]
        selected_month = st.selectbox('Select a month', month_list)
        df_selected_month = df_reshaped[df_reshaped.month == selected_month]
        df_selected_month_sorted = df_selected_month.sort_values(
            by="water_consumption", ascending=True)

        color_theme_list = ['blues', 'cividis', 'greens', 'inferno',
                            'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']

        selected_color_theme = st.selectbox(
            'Select a color theme', color_theme_list)

    # Dashboard Main Panel
    col = st.columns((1.5, 4.5, 2), gap='medium')

    # Example usage in your main code
    with col[0]:
        st.markdown('#### Water Usage Metrics')

    with col[1]:
        st.markdown('#### Water Consumption Distribution')
        choropleth = make_choropleth(
            df_selected_month, 'states_code', 'water_consumption', selected_color_theme)
        st.plotly_chart(choropleth, use_container_width=True)

    with col[2]:
        pass
