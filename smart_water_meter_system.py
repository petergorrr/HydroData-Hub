import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Load the dataset
file_path = 'enhanced_water_data.csv'
df = pd.read_csv(file_path)
df['date'] = pd.to_datetime(df['year'].astype(str) + df['month'], format='%Y%B')

def format_number(number):
    """Formats a number with commas for readability."""
    return f"{number:,}"

def calculate_water_consumption_difference(df, selected_month):
    """Calculates water consumption differences for a selected month."""
    df_selected_month = df[df['month'] == selected_month]
    df_sorted = df_selected_month.sort_values(by='water_consumption', ascending=False)
    df_sorted['difference'] = df_sorted['water_consumption'].diff(-1).fillna(0).abs()
    return df_sorted

def make_donut(input_response, input_text, input_color):
    """Creates a donut chart for water consumption visualization."""
    chart_colors = {'blue': ['#29b5e8', '#155F7A'], 'green': ['#27AE60', '#12783D'],
                    'orange': ['#F39C12', '#875A12'], 'red': ['#E74C3C', '#781F16']}
    chart_color = chart_colors.get(input_color, ['#29b5e8', '#155F7A'])
    source = pd.DataFrame({"Topic": ['', input_text], "% value": [100 - input_response, input_response]})
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta=alt.Theta("% value:Q", stack=True),
        color=alt.Color("Topic:N", scale=alt.Scale(range=chart_color), legend=None),
        tooltip=["Topic:N", "% value:Q"]).properties(width=200, height=200)
    return plot

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
    if states:
        df_filtered = df[df['states'].isin(states)]
        chart = alt.Chart(df_filtered).mark_bar().encode(
            x=alt.X('states:N', title='State'),
            y=alt.Y('sum(water_consumption):Q', title='Total Water Consumption (liters)'),
            color='states:N',
            tooltip=['states:N', 'sum(water_consumption):Q']).properties(width=700, height=400)
        return chart
    return alt.Chart(pd.DataFrame()).mark_text(text='No states selected for comparison').properties(width=700, height=400)

def display_forecast_chart(df):
    """Generates and displays a forecast chart for water consumption for all states."""
    # Simulate forecast data
    states = df['states'].unique()
    forecast_values = np.random.randint(500, 1000, size=len(states))  # Simulated forecast values
    
    # Create a DataFrame for the forecast data
    forecast_df = pd.DataFrame({
        'State': states,
        'Forecasted Water Consumption (liters)': forecast_values
    }).sort_values(by='Forecasted Water Consumption (liters)', ascending=False)
    
    # Generate a bar chart
    forecast_chart = alt.Chart(forecast_df).mark_bar().encode(
        x=alt.X('State:N', sort='-y', title='State'),
        y=alt.Y('Forecasted Water Consumption (liters):Q', title='Forecasted Water Consumption (liters)'),
        color=alt.Color('State:N', legend=None),
        tooltip=['State:N', 'Forecasted Water Consumption (liters):Q']
    ).properties(
        width=700,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(fontSize=16)
    
    return forecast_chart


def display_smart_water_meter_interface(df):
    """Displays the enhanced smart water meter dashboard interface with a professional layout."""
    st.title('Enhanced Smart Water Meter Dashboard')
    st.markdown("""
        Explore dynamic water consumption patterns across different states and months. 
        Adjust the selections below to analyze trends, compare states, and uncover insights.
        """)
    
    # Sidebar for color theme selection and month/state filters
    with st.sidebar:
        st.markdown("## Dashboard Settings 🛠")
        selected_color_theme = st.selectbox('Select a color theme', ['blue', 'green', 'red', 'orange'], index=0)
        selected_month = st.selectbox('Select Month', df['month'].unique(), index=0)
        selected_states = st.multiselect('Select states for comparison:', df['states'].unique())

    # Main content area for selections and charts
    st.markdown("## Water Consumption Analysis 📊")
    st.altair_chart(plot_time_series(df), use_container_width=True)

    if selected_states:
        st.markdown("### State Comparison")
        st.altair_chart(compare_states(df, selected_states), use_container_width=True)
    else:
        st.write("Please select one or more states above to compare their water consumption.")

    # High and low consumption details
    df_consumption_difference_sorted = calculate_water_consumption_difference(df, selected_month)
    if not df_consumption_difference_sorted.empty:
        col1, col2 = st.columns(2)
        high_consumption_state = df_consumption_difference_sorted.iloc[0]
        low_consumption_state = df_consumption_difference_sorted.iloc[-1]
        with col1:
            st.subheader('High Consumption')
            st.write(f"State: {high_consumption_state['states']}")
            st.write(f"Consumption: {format_number(high_consumption_state['water_consumption'])} liters")
            st.altair_chart(make_donut(high_consumption_state['water_consumption'], 'High Consumption', selected_color_theme), use_container_width=True)
        with col2:
            st.subheader('Low Consumption')
            st.write(f"State: {low_consumption_state['states']}")
            st.write(f"Consumption: {format_number(low_consumption_state['water_consumption'])} liters")
            st.altair_chart(make_donut(low_consumption_state['water_consumption'], 'Low Consumption', selected_color_theme), use_container_width=True)
    

    # Forecast section with chart
    st.markdown("## Forecast Analysis 🚀")
    st.markdown("### Forecasted Water Consumption by State for the Coming Year")
    forecast_chart = display_forecast_chart(df)
    st.altair_chart(forecast_chart, use_container_width=True)