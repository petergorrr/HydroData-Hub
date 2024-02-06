import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import geopandas as gpd


# Function to load Penang Hills GeoJSON data
def load_penang_hills_geojson():
    penang_hills_geojson_path = "Penang_DM_2015.geojson"
    penang_hills_data = gpd.read_file(penang_hills_geojson_path)
    return penang_hills_data

# Function to display the PyDeck Penang Hills map
def display_penang_hills_map(penang_hills_data):
    st.title("Penang Hills Map")

    # Create PyDeck Scatter Plot data
    data = [{"latitude": lat, "longitude": lon} for lon, lat in zip(
        penang_hills_data.geometry.centroid.x, penang_hills_data.geometry.centroid.y)]

    # Create PyDeck Scatter Plot
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data,
        get_position="[longitude, latitude]",
        get_radius=200,
        get_fill_color="[255, 0, 0]",
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        extruded=True,
    )

    # Set the initial view state
    view_state = pdk.ViewState(
        latitude=penang_hills_data.geometry.centroid.y.mean(),
        longitude=penang_hills_data.geometry.centroid.x.mean(),
        zoom=10,
        pitch=45,
        bearing=0,
    )

    # Create PyDeck Deck
    r = pdk.Deck(
        layers=[scatter_layer],
        initial_view_state=view_state,
    )

    # Display the PyDeck Chart
    st.pydeck_chart(r)


# Function to fetch fake water usage data
def fetch_water_usage_data():
    # Replace this with your actual data fetching logic
    # For the sake of example, let's create a DataFrame with fake data
    data = {
        'area': ['Area A', 'Area B', 'Area C', 'Area D'],
        'water_usage': np.random.randint(1000, 5000, size=(4,))
    }
    water_usage_df = pd.DataFrame(data)
    return water_usage_df


# Function to calculate fake water usage metrics
def calculate_water_usage_metrics(water_usage_data):
    # Replace this with your actual data processing logic
    # For the sake of example, let's sort the areas based on water usage
    sorted_data = water_usage_data.sort_values(
        by='water_usage', ascending=False)
    return sorted_data


# Function to display smart water meter system interface
def display_smart_water_meter_interface():

    # if st.button("Show Penang Hills Map"):
    #     # Load Penang Hills GeoJSON data
    #     penang_hills_data = load_penang_hills_geojson()
    #     display_penang_hills_map(penang_hills_data)

    # Dashboard Main Panel
    col = st.columns((1.5, 4.5, 2), gap='medium')

    # Example usage in your main code
    with col[0]:
        st.markdown('#### Water Usage Metrics')

        # Fetch fake water usage data
        water_usage_data = fetch_water_usage_data()

        # Calculate fake water usage metrics
        df_water_usage_sorted = calculate_water_usage_metrics(water_usage_data)

        if not df_water_usage_sorted.empty:
            most_water_usage_area = df_water_usage_sorted.area.iloc[0]
            # Use str() to convert to string
            most_water_usage = str(df_water_usage_sorted.water_usage.iloc[0])
        else:
            most_water_usage_area = '-'
            most_water_usage = '-'

        st.metric(label="Most Water Usage Area",
                  value=most_water_usage, delta=most_water_usage_area)

        # Add other relevant water usage metrics as needed
        # ...

        st.markdown('#### Other Relevant Metrics')

        # Add additional relevant metrics specific to your Smart Water Meter System
        # ...

        # Example: Average Daily Water Consumption
        # average_daily_usage = calculate_average_daily_water_usage(df_water_usage_sorted)
        # st.metric(label="Average Daily Water Consumption", value=average_daily_usage)

    with col[1]:
        pass

    with col[2]:
        pass

    # Sidebar
    with st.sidebar:
        st.title('Smart Water Meter System🚰')
        st.sidebar.image("images/smart_water_meter.jpg", use_column_width=True)
        st.sidebar.info(
            "The Smart Water Meter System provides real-time monitoring and analytics for water consumption. "
            "Track usage patterns, detect leaks, and make informed decisions for efficient water management."
        )

        # year_list = list(df_reshaped.year.unique())[::-1]
        # selected_year = st.selectbox('Select a year', year_list)
        # df_selected_year = df_reshaped[df_reshaped.year == selected_year]
        # df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

        color_theme_list = ['blues', 'cividis', 'greens', 'inferno',
                            'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']

        selected_color_theme = st.selectbox(
            'Select a color theme', color_theme_list)
