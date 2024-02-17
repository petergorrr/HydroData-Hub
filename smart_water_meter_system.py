import streamlit as st
import pandas as pd
import altair as alt

# Load the dataset
file_path = 'water_data.csv'
df = pd.read_csv(file_path)

# Function to format numbers


def format_number(number):
    return f"{number:,}"


# Function to calculate water consumption difference
def calculate_water_consumption_difference(df, selected_month):
    df_selected_month = df[df['month'] == selected_month]
    df_sorted = df_selected_month.sort_values(
        by='water_consumption', ascending=False)
    if df_sorted.shape[0] > 1:
        df_sorted['difference'] = df_sorted['water_consumption'].diff(
            -1).fillna(0).abs()
    else:
        df_sorted['difference'] = 0
    return df_sorted


# Donut chart function
def make_donut(input_response, input_text, input_color):
    chart_colors = {
        'blue': ['#29b5e8', '#155F7A'],
        'green': ['#27AE60', '#12783D'],
        'orange': ['#F39C12', '#875A12'],
        'red': ['#E74C3C', '#781F16']
    }
    chart_color = chart_colors.get(input_color, ['#29b5e8', '#155F7A'])

    source = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100 - input_response, input_response]
    })

    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta=alt.Theta("% value:Q", stack=True),
        color=alt.Color("Topic:N", scale=alt.Scale(
            range=chart_color), legend=None),
        tooltip=["Topic:N", "% value:Q"]
    ).properties(width=200, height=200)

    return plot


def display_smart_water_meter_interface():
    st.title('Smart Water Meter Dashboard')

    # Sidebar for user inputs
    with st.sidebar:
        selected_month = st.selectbox('Select Month', df['month'].unique())
        selected_color_theme = st.selectbox(
            'Select a color theme', ['blue', 'green', 'red', 'orange'])

    # Main dashboard layout
    df_consumption_difference_sorted = calculate_water_consumption_difference(
        df, selected_month)

    if not df_consumption_difference_sorted.empty:
        # High consumption data
        high_consumption_state_name = df_consumption_difference_sorted.iloc[0]['states']
        high_consumption_value = df_consumption_difference_sorted.iloc[0]['water_consumption']
        high_consumption_delta = df_consumption_difference_sorted.iloc[0]['difference']

        # Low consumption data
        low_consumption_state_name = df_consumption_difference_sorted.iloc[-1]['states']
        low_consumption_value = df_consumption_difference_sorted.iloc[-1]['water_consumption']
        low_consumption_delta = df_consumption_difference_sorted.iloc[-1]['difference']

        # Layout adjustment
        col = st.columns((1, 1), gap="medium")

        with col[0]:
            st.markdown('#### High Consumption')
            st.metric(label=high_consumption_state_name,
                      value=f"{high_consumption_value} liters", delta=f"Δ {high_consumption_delta} liters")
            st.altair_chart(make_donut(high_consumption_value, 'High Consumption',
                            selected_color_theme), use_container_width=True)

        with col[1]:
            st.markdown('#### Low Consumption')
            st.metric(label=low_consumption_state_name,
                      value=f"{low_consumption_value} liters", delta=f"Δ {low_consumption_delta} liters")
            st.altair_chart(make_donut(low_consumption_value, 'Low Consumption',
                            selected_color_theme), use_container_width=True)

    else:
        st.write("No data available for the selected month.")
