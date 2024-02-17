import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import json

# Assuming the correct paths to your dataset and GeoJSON file
dataset_path = 'enhanced_water_data.csv'
geojson_path = 'Penang.geojson'

# Load the dataset
df = pd.read_csv(dataset_path)
df['date'] = pd.to_datetime(df['year'].astype(str) + df['month'], format='%Y%B')

# Load the GeoJSON
with open(geojson_path, 'r') as file:
    penang_geojson = json.load(file)

# Update GeoJSON features with water consumption data
for feature in penang_geojson['features']:
    parliament = feature['properties']['Parliament']
    water_consumption = df[(df['states'] == parliament) & (df['year'] == 2020)]['water_consumption'].sum()
    feature['properties']['water_consumption'] = water_consumption

# Define necessary functions from your initial code
def format_number(number):
    """Formats a number with commas for readability."""
    return f"{number:,}"

def plot_time_series(df):
    """Plots time series of water consumption."""
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('date:T', title='Month'),
        y=alt.Y('water_consumption:Q', title='Water Consumption (liters)'),
        color='states:N',
        tooltip=['states:N', 'water_consumption:Q', 'date:T']).properties(width=700, height=400).interactive()
    return chart

def compare_states(df, states):
    """Compares water consumption across selected states."""
    df_filtered = df[df['states'].isin(states)]
    chart = alt.Chart(df_filtered).mark_bar().encode(
        x='states:N',
        y='sum(water_consumption):Q',
        color='states:N',
        tooltip=['states:N', 'sum(water_consumption):Q']).properties(width=700, height=400)
    return chart

def display_forecast_chart(df):
    """Generates and displays a forecast chart for water consumption for all states."""
    states = df['states'].unique()
    forecast_values = np.random.randint(500, 1000, size=len(states))
    forecast_df = pd.DataFrame({'State': states, 'Forecasted Water Consumption (liters)': forecast_values})
    forecast_chart = alt.Chart(forecast_df).mark_bar().encode(
        x='State:N',
        y='Forecasted Water Consumption (liters):Q',
        color='State:N',
        tooltip=['State:N', 'Forecasted Water Consumption (liters):Q']).properties(width=700, height=400)
    return forecast_chart

# Function to display choropleth map
def display_choropleth(geojson):
    """Display a choropleth map using Pydeck."""
    # Define the Pydeck layer for the choropleth map
    layer = pdk.Layer(
        'GeoJsonLayer',
        geojson,
        opacity=0.8,
        stroked=True,
        filled=True,
        extruded=False,
        get_fill_color="""
            [
                255,
                255 - properties.water_consumption / 1000 * 255,
                255 - properties.water_consumption / 1000 * 255,
                properties.water_consumption / 2000 * 255 + 100
            ]
        """,  # Blue color scale based on water consumption
        get_line_color=[255, 255, 255],
        line_width_min_pixels=1,
    )

    # Define the initial view state for the Pydeck map
    view_state = pdk.ViewState(latitude=5.4164, longitude=100.3327, zoom=10)

    # Render the map with Pydeck
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
    
# Streamlit application layout
def display_smart_water_meter_interface():
    st.title('Enhanced Smart Water Meter Dashboard')
    st.markdown("""Explore dynamic water consumption patterns across different states and months. Adjust the selections below to analyze trends, compare states, and uncover insights.""")

    # Sidebar for settings
    with st.sidebar:
        st.markdown("## Dashboard Settings 🛠")
        selected_color_theme = st.selectbox('Select a color theme', ['blue', 'green', 'red', 'orange'], index=0)
        selected_month = st.selectbox('Select Month', df['month'].unique(), index=0)
        selected_states = st.multiselect('Select states for comparison:', df['states'].unique())

    # Water Consumption Analysis
    st.markdown("## Water Consumption Analysis 📊")
    st.altair_chart(plot_time_series(df))

    if selected_states:
        st.markdown("### State Comparison")
        st.altair_chart(compare_states(df, selected_states))

    # Forecast section
    st.markdown("## Forecast Analysis 🚀")
    st.markdown("### Forecasted Water Consumption by State for the Coming Year")
    st.altair_chart(display_forecast_chart(df))
    
    # Display the choropleth map
    st.markdown("## Water Consumption in Penang - Choropleth Map")
    display_choropleth(penang_geojson)

    # Display a legend for the choropleth map
    st.markdown("### Legend")
    st.markdown("""
    - **Blue**: 0-500 liters
    - **Light Blue**: 500-1000 liters
    - **Very Light Blue**: 1000-2000 liters
    - **Almost White**: 2000+ liters
    """)

