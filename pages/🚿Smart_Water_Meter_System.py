import streamlit as st
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from streamlit_image_comparison import image_comparison

# Set page configuration
st.set_page_config(page_title="Smart Water Meter System", page_icon="🚿", layout='centered', initial_sidebar_state='expanded')

# Title and description of the app
st.title("Smart Water Management Dashboard")
st.write("---")  # Horizontal rule for visual separation

# Sidebar setup
with st.sidebar:
    # Display an image with description
    st.image("images/smart_water_meter.jpg", use_column_width=True)
    
    # Information section about the app usage
    st.info(
        "This app uses a smart water meter system with comprehensive visualization tools "
        "and an advanced warning system. It helps authorities save water and manage resources better."
    )
    
    # Legal and copyright information
    st.markdown("---")
    st.write("This application is for authorized use only.")
    st.markdown("Copyright © Make Water OK Malaysia")
    st.markdown("---")
    
    # Data sources and references section
    st.markdown("""
        <style>
            .data-sources {
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-size: 14px;
                margin-top: 10px;
            }
            .data-sources-header {
                font-weight: bold;
                font-size: 16px;
                margin-bottom: 5px;
            }
            .source-link {
                color: #f96854;
                text-decoration: none;
            }
        </style>
        <div class="data-sources">
            <div class="data-sources-header">Data Sources and References:</div>
            <ul>
                <li><a href="https://publicinfobanjir.water.gov.my/hujan/data-hujan/?state=PNG&lang=en" class="source-link" target="_blank">Rainfall Data - Malaysia Flood Information</a></li>
                <li><a href="https://www.accuweather.com/" class="source-link" target="_blank">Weather Forecast - AccuWeather</a></li>
                <li><a href="https://www.met.gov.my/" class="source-link" target="_blank">Malaysia Meteorological Department</a></li>
            </ul>
        </div>
    """, unsafe_allow_html=True)


#----VISUALIZE--------------------------------------------------------------------
V_Metric_Data = pd.read_csv('V_Metric_Data.csv')
V_Choropleth_Data = pd.read_csv('V_Choropleth_Data.csv')
V_Reservoir_Data = pd.read_csv('V_Reservoir_Data.csv')
V_Compare_Data = pd.read_csv('V_Compare_Data.csv')

def V_Metric_Data_Function(selected_month, dataset_1):
    container = st.container(border=True)
    
    with container:
        col1, col2, col3 = st.columns(3)

        with col1:
            selected_month_data = dataset_1[dataset_1["Metric_Month"] == selected_month]
            avg_temperature = selected_month_data["Metric_Avg_Temperature_Degree_Celsius"].values[0]
            avg_temperature_delta = selected_month_data["Metric_Avg_Temperature_Degree_Celsius_Delta"].values[0]
            st.metric(label="Avg Temperature🌡️", value = str(avg_temperature) + " °C", delta= str(avg_temperature_delta) + "°C from last month", delta_color="inverse", help=None, label_visibility="visible")

        with col2:
            avg_rainfall = selected_month_data["Metric_Avg_Rainfall_Mm"].values[0]
            avg_rainfall_delta = selected_month_data["Metric_Avg_Rainfall_Mm_Delta"].values[0]
            st.metric(label="Avg Rainfall🌧️", value = str(avg_rainfall) + " mm", delta= str(avg_rainfall_delta) + "mm from last month", delta_color="normal", help=None, label_visibility="visible")

        with col3:
            avg_humidity = selected_month_data["Metric_Avg_Humidity_Percent"].values[0]
            avg_humidity_delta = selected_month_data["Metric_Avg_Humidity_Percent_Delta"].values[0]
            st.metric(label="Avg Humidity💧", value = str(avg_humidity) + " %", delta=str(avg_humidity_delta) + "% from last month", delta_color="normal", help=None, label_visibility="visible")


def Area_Map():

    with st.container():
        st.markdown("""
    <h3 style="text-align: center;">
        Area Map of Penang Hill Biosphere Reserve
    </h3>
    """, unsafe_allow_html=True)

        image_comparison(img1="slide2.png", img2="slide1.png", width=670)
    
    with st.expander("Map Legend"):
        # Including custom styles for better typography and a solid border box
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap');
            .info-box {
                border: 2px solid ;
                border-radius: 10px;
                padding: 15px;
                font-family: 'Nunito', sans-serif;
                font-size: 16px;
                line-height: 1.6;
                margin-top: 5px;
                background-color: #ffffff;
            }
            .area {
                font-weight: bold;
                color: #618685;
            }
            .location {
                margin-left: 20px;
                color: #555;
            }
            .icon {
                color: #2ca02c;
                margin-right: 5px;
            }
        </style>
        <div class='info-box'>
            <p><span class='icon'>📍</span><span class='area'>Area N:</span>
                <span class='location' title='Click for more info'>Bypath D restroom, Sri Aruloli Thirumurugan Temple, Earthquake & Typhoon Pavilion, Toy Museum & 5D, Bellevue Hotel</span></p>
            <p><span class='icon'>📍</span><span class='area'>Area E:</span>
                <span class='location' title='Click for more info'>Penang Hill Gallery@Edgecliff, Henna Art & Spa</span></p>
            <p><span class='icon'>📍</span><span class='area'>Area S:</span>
                <span class='location' title='Click for more info'>TeddyVille Museum, Astaka(Cliff Café), David Brown’s Restaurant, Kota Dine & Coffee and The Loaf Railway Café, Little Village, Penang Hill Kacang Putih</span></p>
            <p><span class='icon'>📍</span><span class='area'>Area W:</span>
                <span class='location' title='Click for more info'>Monkey Cup Garden, Gate House Bel Retiro, Penang Hill mosque, Hillside retreat</span></p>
        </div>
        """, unsafe_allow_html=True)



def Combined(selected_month, dataset_2, dataset_3):
    
    container = st.container(border=True)

    with container:
        # Split the container into two columns
        col1, col2 = st.columns((5, 5))

    # Component 1: Choropleth Data Function
    with col1:
        st.markdown('### Area Water Usage')

        # Set the "Area" column as the index if it isn't already
        if dataset_2.index.name != 'Area':
            dataset_2 = dataset_2.set_index('Area')

        # Filter the DataFrame to include only the selected month's data
        selected_month_data_choropleth = dataset_2[[selected_month]]

        # Sort values for better visualization
        selected_month_data_choropleth = selected_month_data_choropleth.sort_values(by=selected_month)

        # Plotting with Matplotlib
        plt.style.use('ggplot')  # Use ggplot style for more visually appealing plots
        fig, ax = plt.subplots(figsize=(10, 6))  # Set figure size
        bars = ax.barh(selected_month_data_choropleth.index, selected_month_data_choropleth[selected_month])
        ax.set_xlabel('Water Usage (Litre)', fontsize=22, fontweight='bold')
        ax.set_title('Water Usage For Selected Month', fontsize=22, fontweight='bold')
        ax.spines['top'].set_visible(False)  # Remove top spine
        ax.spines['right'].set_visible(False)  # Remove right spine
        ax.spines['bottom'].set_color('#DDDDDD')  # Lighten bottom spine
        ax.spines['left'].set_color('#DDDDDD')  # Lighten left spine
        ax.tick_params(axis='y', which='major', labelsize=22)  # Adjust y-axis label size
        ax.tick_params(axis='x', which='major', labelsize=22)  # Adjust x-axis label size

        # Add value labels to each bar
        for bar in bars:
            ax.text(
                bar.get_width(),  # Get the horizontal position of the bar end
                bar.get_y() + bar.get_height() / 2,  # Get the vertical position of the bar center
                f' {bar.get_width():.0f} L',  # The label text
                va='center',  # Center alignment
                ha='left',  # Left alignment relative to the bar end
                fontsize=10
            )

        # Display the bar chart
        st.pyplot(fig)


            
    # Component 2: Reservoir Data Function
    with col2:
        st.markdown('### Reservoir Water Level')

        # Set the "Reservoir" column as the index
        dataset_3.set_index("Reservoir", inplace=True)

        # Filter the DataFrame to include only the selected month's data
        selected_month_data_reservoir = dataset_3[selected_month]

        # Display the filtered data
        st.data_editor(selected_month_data_reservoir,
                        column_config={
                            selected_month: st.column_config.ProgressColumn(
                                "Water Level (%)",
                                format="%f",
                                width="medium",
                                min_value=0,
                                max_value=100,),},
                                width=320,
                                disabled=True,
                                hide_index=False)
    
    st.info(
    "Efficient water resource management requires a clear understanding of the water condition. "
    "The above section provides two key metrics:\n\n"
    
    "**Area Water Usage:**\n"
    "Shows water consumption distribution across regions. Identifies areas with high or low usage patterns, "
    "enabling proactive measures to optimize distribution and mitigate water scarcity risks.\n\n"
    
    "**Reservoir Water Level:**\n"
    "Indicates the current water storage percentage in the dam. It helps estimate how long the water can last "
    "based on consumption rates, aiding in informed decisions on allocation and conservation.\n\n"
)



def Leakage_Info_Function():
    container = st.container(border=True)

    with container:
        st.markdown("""
    <h3 style="text-align: center;">
        ⚠️Alert Warning⚠️
    </h3>
    """, unsafe_allow_html=True)
        # Create a dictionary with the data
        Leakage_Data = pd.DataFrame(
            {"Area": [["Area E"], ["Area W"],["Area N"],["Area S"]],
            "Abnormalities": [["4/4"], ["2/4"],["0/4"],["0/4"]],
            "Indicators": [
                ["🚨 Unusual Water Usage", "🚨 Acoustic Leak Detection", "🚨 Abnormal Water Temperature", "🚨 Abnormal Water Pressure"],
                ["🚨 Abnormal Water Temperature", "🚨 Abnormal Water Pressure"],["All Good!"],["All Good!"]],})

        st.data_editor(Leakage_Data, 
                        column_config={"Leakage":st.column_config.ListColumn(
                            "Abnormality",),},
                            width=670,
                            hide_index=True)    
    
    with st.popover("4 Leakage Indicators", help=None, disabled=False, use_container_width=True):
                st.markdown("🚨 Unusual Water Usage ***(Monitor unusual spikes or drops in water consumption)***")
                st.markdown("🚨 Acoustic Leak Detection ***(Sound sensors detect unique noise patterns caused by escaping water)***")
                st.markdown("🚨 Abnormal Water Temperature ***(Monitor deviations from expected water temperature ranges)***")
                st.markdown("🚨 Abnormal Water Pressure ***(Detect Unexplained sudden increases and drops in water pressure)***")

def Compare_Water_Level(selected_month, dataset_4):
    container = st.container(border=True)

    with container:
        st.markdown('### Water Supply/Demand')
        
        dataset_4.set_index("Component", inplace=True)

        # Filter the DataFrame to include only the selected month's data
        selected_month_data_compare = dataset_4[selected_month]

        # Display the filtered data
        st.data_editor(selected_month_data_compare,
                        column_config={
                            selected_month: st.column_config.ProgressColumn(
                                "Water Supply/Demand",
                                help="The Water Usage is in Litre",
                                format="%f L",
                                min_value=0,
                                max_value=100000000,),},
                                width = 670,
                                disabled=True,
                                hide_index=False)

# Display the current year in an aesthetic way
st.markdown("### 📅 Year: 2023")

# Revised month selection with a more natural phrase
option = st.selectbox(
    "Select a Month to Display",
    ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
)

# Call the functions for visualization
if __name__ == "__main__":
    V_Metric_Data_Function(option, V_Metric_Data)
    Area_Map()
    Combined(option, V_Choropleth_Data, V_Reservoir_Data)
    Compare_Water_Level(option, V_Compare_Data)
    Leakage_Info_Function()

# Title for the Forecasting section
st.title("Forecasting")

def load_model():
    """Function to load the trained model and label encoders from a pickle file."""
    with open("water_model.pkl", "rb") as file:
        data = pickle.load(file)
    return data

# Load the model and label encoders
data = load_model()
regressor = data["model"]
le_Month = data["le_Month"]
le_Area = data["le_Area"]
le_Weather = data["le_Weather"]
le_Festival = data["le_Festival"]

def display_forecast_interface():
    """Function to display the prediction interface and handle forecasting."""
    st.write("Input features for forecasting:")

    # Define options for dropdown selection
    months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    areas = ("Area N", "Area E", "Area S", "Area W")
    weather_conditions = ("Sunny", "Cloudy", "Rainy")
    festival_options = ("Yes", "No")

    # User input for forecasting
    selected_month = st.selectbox("Month", months)
    selected_area = st.selectbox("Area", areas)
    selected_weather = st.selectbox("Weather", weather_conditions)
    selected_festival = st.selectbox("Festival", festival_options)
    no_visitor_area = st.text_input("Number of visitors")
    no_residence_area = st.text_input("Number of residences")

    if st.button("Calculate"):
        # Prepare input data for the prediction model
        input_features = np.array([[selected_month, selected_area, selected_weather, selected_festival, no_visitor_area, no_residence_area]])
        input_features[:, 0] = le_Month.transform([input_features[:, 0][0]])
        input_features[:, 1] = le_Area.transform([input_features[:, 1][0]])
        input_features[:, 2] = le_Weather.transform([input_features[:, 2][0]])
        input_features[:, 3] = le_Festival.transform([input_features[:, 3][0]])
        input_features = input_features.astype(float)

        # Predict using the loaded model
        estimated_water_usage = regressor.predict(input_features)

        # Display the prediction result
        st.subheader(f"The estimated water usage is {int(estimated_water_usage[0]):,} Litre")

# Execute the forecast interface function
display_forecast_interface()