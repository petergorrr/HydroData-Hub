import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_image_comparison import image_comparison

# Set page configuration
st.set_page_config(page_title="Smart Water Meter System", page_icon="🚿", layout='centered', initial_sidebar_state='expanded')

# Title and description of the app
st.title("Smart Water Management Dashboard")
st.write("---")  # Horizontal rule for visual separation

# Sidebar setup
with st.sidebar:
    st.image("images/smart_water_meter.jpg", use_column_width=True)
    st.info(
        "This app uses a smart water meter system with comprehensive visualization tools "
        "and an advanced warning system. It helps authorities save water and manage resources better."
    )
    st.markdown("---")
    st.write("This application is for authorized use only.")
    st.markdown("Copyright © Make Water OK Malaysia")
    st.markdown("---")
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

# Load datasets
V_Metric_Data = pd.read_csv('V_Metric_Data.csv')
V_Choropleth_Data = pd.read_csv('V_Choropleth_Data.csv')
V_Reservoir_Data = pd.read_csv('V_Reservoir_Data.csv')
V_Compare_Data = pd.read_csv('V_Compare_Data.csv')
data = pd.read_csv('water_data.csv')

def V_Metric_Data_Function(selected_month, dataset):
    container = st.container()
    with container:
        col1, col2, col3 = st.columns(3)
        selected_month_data = dataset[dataset["Metric_Month"] == selected_month]

        with col1:
            avg_temperature = selected_month_data["Metric_Avg_Temperature_Degree_Celsius"].values[0]
            avg_temperature_delta = selected_month_data["Metric_Avg_Temperature_Degree_Celsius_Delta"].values[0]
            st.metric("Avg Temperature🌡️", f"{avg_temperature} °C", f"{avg_temperature_delta}°C from last month", delta_color="inverse")

        with col2:
            avg_rainfall = selected_month_data["Metric_Avg_Rainfall_Mm"].values[0]
            avg_rainfall_delta = selected_month_data["Metric_Avg_Rainfall_Mm_Delta"].values[0]
            st.metric("Avg Rainfall🌧️", f"{avg_rainfall} mm", f"{avg_rainfall_delta}mm from last month", delta_color="normal")

        with col3:
            avg_humidity = selected_month_data["Metric_Avg_Humidity_Percent"].values[0]
            avg_humidity_delta = selected_month_data["Metric_Avg_Humidity_Percent_Delta"].values[0]
            st.metric("Avg Humidity💧", f"{avg_humidity} %", f"{avg_humidity_delta}% from last month", delta_color="normal")

def Area_Map():
    with st.container():
        st.markdown("<h3 style='text-align: center;'>Area Map of Penang Hill Biosphere Reserve</h3>", unsafe_allow_html=True)
        image_comparison(img1="slide2.png", img2="slide1.png", width=670)
    
    with st.expander("Map Legend"):
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap');
            .info-box {
                border: 2px solid;
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
                <span class='location'>Bypath D restroom, Sri Aruloli Thirumurugan Temple, Earthquake & Typhoon Pavilion, Toy Museum & 5D, Bellevue Hotel</span></p>
            <p><span class='icon'>📍</span><span class='area'>Area E:</span>
                <span class='location'>Penang Hill Gallery@Edgecliff, Henna Art & Spa</span></p>
            <p><span class='icon'>📍</span><span class='area'>Area S:</span>
                <span class='location'>TeddyVille Museum, Astaka(Cliff Café), David Brown’s Restaurant, Kota Dine & Coffee and The Loaf Railway Café, Little Village, Penang Hill Kacang Putih</span></p>
            <p><span class='icon'>📍</span><span class='area'>Area W:</span>
                <span class='location'>Monkey Cup Garden, Gate House Bel Retiro, Penang Hill mosque, Hillside retreat</span></p>
        </div>
        """, unsafe_allow_html=True)

def Combined(selected_month, choropleth_data, reservoir_data):
    container = st.container()
    with container:
        col1, col2 = st.columns((5, 5))

    with col1:
        st.markdown('### Area Water Usage')
        choropleth_data.set_index('Area', inplace=True)
        selected_month_data_choropleth = choropleth_data[[selected_month]].sort_values(by=selected_month)

        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(selected_month_data_choropleth.index, selected_month_data_choropleth[selected_month])
        ax.set_xlabel('Water Usage (Litre)', fontsize=22, fontweight='bold')
        ax.set_title('Water Usage For Selected Month', fontsize=22, fontweight='bold')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#DDDDDD')
        ax.spines['left'].set_color('#DDDDDD')
        ax.tick_params(axis='y', which='major', labelsize=22)
        ax.tick_params(axis='x', which='major', labelsize=22)
        for bar in bars:
            ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f' {bar.get_width():.0f} L', va='center', ha='left', fontsize=10)
        st.pyplot(fig)
            
    with col2:
        st.markdown('### Reservoir Water Level')
        reservoir_data.set_index("Reservoir", inplace=True)
        selected_month_data_reservoir = reservoir_data[selected_month]
        st.data_editor(selected_month_data_reservoir,
                       column_config={
                           selected_month: st.column_config.ProgressColumn(
                               "Water Level (%)",
                               format="%f",
                               width="medium",
                               min_value=0,
                               max_value=100),
                       },
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

def display_supply_demand_ratio(selected_month, dataset):
    st.title('Water Supply/Demand Ratio')
    st.markdown(f"""
        <style>
            .info {{
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                background-color: #f9f9f9;
                padding: 10px;
                border: 2px solid #2c3e50;
                border-radius: 10px;
                box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
            }}
            .header {{
                color: #d35400;
                font-size: 16px;
                margin-bottom: 0;
            }}
        </style>
        <div class='info'>
            Displaying the water supply for <span class='header'>{selected_month}</span> as a percentage of the highest recorded demand for Penang Hill. This comparison provides insight into the current supply levels relative to historical peaks:
            <ul>
                <li><b>100%:</b> Current supply equals the historical peak.</li>
                <li><b>Below 100%:</b> Current supply is less than the peak, which indicates it's below the maximum recorded.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    for index, row in dataset.iterrows():
        component = row['Component']
        supply_percentage = row[f'{selected_month} % of Max Demand']
        supply = row[selected_month]
        st.markdown(f"**{component}**")
        st.progress(supply_percentage / 100)
        st.caption(f"{supply:,.0f} L - {supply_percentage:.2f}% of highest recorded demand ({row['Risk Assessment']})")
    st.write("---")

def Leakage_Info_Function():
    container = st.container()
    with container:
        st.markdown("""
        <h3 style="text-align: center;">
            ⚠️Alert Warning⚠️
        </h3>
        """, unsafe_allow_html=True)
        Leakage_Data = pd.DataFrame(
            {"Area": [["Area E"], ["Area W"], ["Area N"], ["Area S"]],
             "Abnormalities": [["4/4"], ["2/4"], ["0/4"], ["0/4"]],
             "Indicators": [
                ["🚨 Unusual Water Usage", "🚨 Acoustic Leak Detection", "🚨 Abnormal Water Temperature", "🚨 Abnormal Water Pressure"],
                ["🚨 Abnormal Water Temperature", "🚨 Abnormal Water Pressure"], ["All Good!"], ["All Good!"]],})

        st.data_editor(Leakage_Data, 
                       column_config={"Leakage": st.column_config.ListColumn("Abnormality",)},
                       width=670,
                       hide_index=True)
    
    with st.popover("4 Signs of Water Leakage", help=None, disabled=False, use_container_width=True):
        st.markdown("🚨 Unusual Water Usage : ***Keep an eye on unexpected increases or decreases in water consumption.***")
        st.markdown("🚨 Acoustic Leak Detection : ***Special sensors detect unique sounds made by leaking water.***")
        st.markdown("🚨 Abnormal Water Temperature : ***Look out for unusual changes in water temperature.***")
        st.markdown("🚨 Abnormal Water Pressure : ***Detect sudden and unexplained changes in water pressure.***")

# Display the current year
st.markdown("### 📅 Year: 2023")

# Month selection
option = st.selectbox(
    "Select a Month to Display",
    ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
)

# Call functions for visualization
if __name__ == "__main__":
    V_Metric_Data_Function(option, V_Metric_Data)
    Area_Map()
    Combined(option, V_Choropleth_Data, V_Reservoir_Data)
    display_supply_demand_ratio(option, V_Compare_Data)
    Leakage_Info_Function()

# Title for the Forecasting section
st.title("Monthly Water Watch")

# Ensure the 'Month' column is a categorical type with a defined order
month_order = ["January", "February", "March", "April", "May", "June", 
               "July", "August", "September", "October", "November", "December"]
data['Month'] = pd.Categorical(data['Month'], categories=month_order, ordered=True)

# Calculate the monthly average water usage
monthly_avg = data.groupby('Month')['Avg_Usage_Litre'].mean().reset_index()

# User input: select a month
selected_month = st.selectbox("Select a Month to Display Forecasting and Advice", monthly_avg['Month'])

# Find the average for the selected month
selected_month_avg = monthly_avg[monthly_avg['Month'] == selected_month]['Avg_Usage_Litre'].iloc[0]

# Display the average water usage
st.markdown(f"For {selected_month}, the historical average water usage is <span style='color: black; font-weight: bold;'>{selected_month_avg:,.0f} litres</span>.", unsafe_allow_html=True)

# Provide recommendations based on the average
if selected_month == "January":
    st.success(f"🎉 Warning: Expect increased water consumption in {selected_month} due to the Chinese New Year Festival. Implement water-saving tactics and monitor usage closely to manage the surge.")
elif selected_month == "April":
    st.success(f"🌙 Warning: Anticipate heightened water usage in {selected_month} for the Hari Raya Festival. Adopt proactive water-saving measures and keep a vigilant watch on consumption levels.")
elif selected_month == "December":
    st.success(f"🎄 Warning: Prepare for elevated water usage during {selected_month} owing to the Christmas and holiday celebrations. Engage in strategic water conservation and maintain strict usage oversight.")
elif selected_month == "November":
    st.success(f"🪔 Warning: Increased water usage likely in {selected_month} during the Deepavali festival. Prioritize implementing water conservation strategies and closely monitor water consumption.")
elif selected_month_avg > 3000000:
    st.success(f"⚠️ Warning: High water usage expected in {selected_month}. Consider implementing water-saving strategies and closely monitoring usage.")
elif selected_month_avg > 2000000:
    st.warning(f"🔍 Note: Moderate water usage expected in {selected_month}. It's a good time to check for any inefficiencies in water use.")
else:
    st.info(f"💧 Low water usage expected in {selected_month}. This is typically a lower demand period.")
