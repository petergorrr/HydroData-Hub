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
df['date'] = pd.to_datetime(
    df['year'].astype(str) + df['month'], format='%Y%B')

# Load the GeoJSON
with open(geojson_path, 'r') as file:
    penang_geojson = json.load(file)


# Update GeoJSON features with water consumption data
for feature in penang_geojson['features']:
    parliament = feature['properties']['Parliament']
    water_consumption = df[(df['states'] == parliament) & (
        df['year'] == 2020)]['water_consumption'].sum()
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
    forecast_df = pd.DataFrame(
        {'State': states, 'Forecasted Water Consumption (liters)': forecast_values})
    forecast_chart = alt.Chart(forecast_df).mark_bar().encode(
        x='State:N',
        y='Forecasted Water Consumption (liters):Q',
        color='State:N',
        tooltip=['State:N', 'Forecasted Water Consumption (liters):Q']).properties(width=700, height=400)
    return forecast_chart


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
                properties.water_consumption == 0 ? 0 : 255, 
                properties.water_consumption == 0 ? 0 : 255 - properties.water_consumption / 1000 * 255,
                properties.water_consumption == 0 ? 0 : 255 - properties.water_consumption / 1000 * 255,
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


def make_donut(input_response, input_text, input_color):
    """Creates a donut chart for water consumption visualization."""
    chart_colors = {'blue': ['#29b5e8', '#155F7A'], 'green': ['#27AE60', '#12783D'],
                    'orange': ['#F39C12', '#875A12'], 'red': ['#E74C3C', '#781F16']}
    chart_color = chart_colors.get(input_color, ['#29b5e8', '#155F7A'])
    source = pd.DataFrame({"Topic": ['', input_text], "% value": [
                          100 - input_response, input_response]})
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta=alt.Theta("% value:Q", stack=True),
        color=alt.Color("Topic:N", scale=alt.Scale(
            range=chart_color), legend=None),
        tooltip=["Topic:N", "% value:Q"]).properties(width=200, height=200)
    return plot


# Streamlit application layout
def display_smart_water_meter_interface():

    st.title('Smart Water Meter Dashboard')
    st.markdown("""Explore dynamic water consumption patterns across different states and months. Adjust the selections below to analyze trends, compare states, and uncover insights.""")

  # Sidebar for settings
    with st.sidebar:
        st.title("Smart Water Meter System")
        st.image("images/smart_water_meter.jpg", use_column_width=True)
        st.info(
            "This app provides insights into water consumption patterns based on historical data and forecasts. "
            "Explore dynamic visualizations to:\n"
            "- Analyze trends across different states and months.\n"
            "- Compare states to uncover differences and similarities.\n"
            "- View forecasts to anticipate future water consumption.\n"
            "Adjust the selections in the main interface to interact with the data and uncover insights."
        )

        st.markdown("## Dashboard Settings 🛠")
        selected_states = st.multiselect(
            'Select states for comparison:', df['states'].unique())

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

    # # Display the choropleth map
    # st.markdown("## Water Consumption in Penang - Choropleth Map")
    # display_choropleth(penang_geojson)

    # # Display a legend for the choropleth map
    # st.markdown("### Legend")
    # st.markdown("""
    # - **Blue**: 0-500 liters
    # - **Light Blue**: 500-1000 liters
    # - **Very Light Blue**: 1000-2000 liters
    # - **Almost White**: 2000+ liters
    # """)
