import streamlit as st
import pickle
import numpy as np
import pandas as pd
import altair as alt
import plotly.express as px
from streamlit_image_comparison import image_comparison


st.set_page_config(layout='centered', initial_sidebar_state='expanded')

# Title and description of the app
st.title("Smart Water Meter System")
st.write("---")

#----VISUALIZE--------------------------------------------------------------------
st.title("Visualization")

V_Metric_Data = pd.read_csv('V_Metric_Data.csv')
V_Choropleth_Data = pd.read_csv('V_Choropleth_Data.csv')
V_Reservoir_Data = pd.read_csv('V_Reservoir_Data.csv')
V_Compare_Data = pd.read_csv('V_Compare_Data.csv')

st.selectbox("Choose Year To Visualize", ("2023"," "))

option = st.selectbox(
    "Choose Month To Visualize",
    ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"))

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
    container = st.container(border=True)
    
    with container:
        st.markdown('### Area Map')
        image_comparison(img1="Slide2.png",img2="Slide1.png", width=670)

def Combined(selected_month, dataset_2, dataset_3):
    
    container = st.container(border=True)

    with container:
        # Split the container into two columns
        col1, col2 = st.columns((5, 5))

    # Component 1: Choropleth Data Function
    with col1:
        st.markdown('### Area Water Usage')

        # Set the "Area" column as the index
        dataset_2.set_index("Area", inplace=True)

        # Filter the DataFrame to include only the selected month's data
        selected_month_data_choropleth = dataset_2[selected_month]

        # Display the filtered data
        st.data_editor(selected_month_data_choropleth,
                        column_config={
                            selected_month: st.column_config.ProgressColumn(
                                "Water Usage For Selected Month",
                                help="The Water Usage is in Litre",
                                format="%f L",
                                min_value=0,
                                max_value=6000000,),},
                                width = 320,
                                disabled = True,
                                hide_index=False)
            
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
                                "Reservoir Water Level (%)",
                                format="%f",
                                width="medium",
                                min_value=0,
                                max_value=100,),},
                                width=320,
                                disabled=True,
                                hide_index=False)

def Leakage_Info_Function():
    container = st.container(border=True)

    with container:
        st.markdown('### ⚠️Leakage Warning⚠️')
        # Create a dictionary with the data
        Leakage_Data = pd.DataFrame(
            {"Area": [["Area E"], ["Area W"]],
            "Abnormal": [["4/4"], ["2/4"]],
            "Indicators": [
                ["🚨 Unusual Water Usage", "🚨 Acoustic Leak Detection", "🚨 Abnormal Water Temperature", "🚨 Abnormal Water Pressure"],
                ["🚨 Abnormal Water Temperature", "🚨 Abnormal Water Pressure"],],})

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

# Call the functions for visualization
if __name__ == "__main__":
    V_Metric_Data_Function(option, V_Metric_Data)
    Area_Map()
    Combined(option, V_Choropleth_Data, V_Reservoir_Data)
    Leakage_Info_Function()
    Compare_Water_Level(option, V_Compare_Data)

#----FORECASTING--------------------------------------------------------------------
st.title("Forecasting")

# Function to load the trained model and label encoders
def load_model():
    with open("water_model.pkl", "rb") as file:
        data = pickle.load(file)
    return data

# Load the model and label encoders
data = load_model()

# Retrieve the trained model and label encoders
regressor = data["model"]
le_Month = data["le_Month"]
le_Area = data["le_Area"]
le_Weather = data["le_Weather"]
le_Festival = data["le_Festival"] 

# Function to display the prediction interface
def F_Forecast():
    # Sidebar title
    st.write("Input features for forecasting:")

    # Options for selecting month, area, weather, and festival
    Month = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    Area = ("Area N", "Area E", "Area S", "Area W")
    Weather = ("Sunny", "Cloudy", "Rainy")
    Festival = ("Yes","No")

    # Selection boxes and text input for user input
    Month = st.selectbox("Month", Month)
    Area = st.selectbox("Area", Area)
    Weather = st.selectbox("Weather", Weather)
    Festival = st.selectbox("Festival", Festival)
    No_Visitor_Area = st.text_input("Number of visitors")
    No_Residence_Area = st.text_input("Number of Residence")


    # Button to trigger calculation
    ok = st.button("Calculate")

    # If the button is clicked
    if ok:
        # Prepare the input data for prediction
        X = np.array([[Month, Area, Weather, Festival, No_Visitor_Area, No_Residence_Area]])
        X[:, 0] = le_Month.transform(X[:,0])
        X[:, 1] = le_Area.transform(X[:,1])
        X[:, 2] = le_Weather.transform(X[:,2])
        X[:, 3] = le_Festival.transform(X[:,3])
        X = X.astype(float)

        # Make prediction using the loaded model
        water = regressor.predict(X)

        # Display the prediction result
        st.subheader(f"The estimated water usage is {int(water[0]):,} Litre")

if __name__ == "__main__":
    F_Forecast()

    