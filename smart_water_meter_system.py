import streamlit as st
import pandas as pd
import altair as alt


# Function to format numbers
def format_number(number):
    return f"{number:,}"


# Function to calculate water consumption difference
def calculate_water_consumption_difference(df, selected_month):
    df_selected_month = df[df['month'] == selected_month]
    df_sorted = df_selected_month.sort_values(
        by='water_consumption', ascending=False)
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
    source_bg = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100, 0]
    })

    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color=alt.Color("Topic:N", scale=alt.Scale(
            domain=[input_text, ''], range=chart_color), legend=None)
    ).properties(width=130, height=130)

    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32,
                          fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))

    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color=alt.Color("Topic:N", scale=alt.Scale(
            domain=[input_text, ''], range=chart_color), legend=None)
    ).properties(width=130, height=130)

    return plot_bg + plot + text



# Main function to display interface
def display_smart_water_meter_interface():
    with st.sidebar:
        st.title('Smart Water Meter System🚰')
        st.image("images/smart_water_meter.jpg", use_column_width=True)
        st.info("The Smart Water Meter System provides real-time monitoring and analytics for water consumption. "
                "Track usage patterns, detect leaks, and make informed decisions for efficient water management.")

        selected_month = st.selectbox('Select Month', df['month'].unique())
        selected_color_theme = st.selectbox(
            'Select a color theme', ['blues', 'greens', 'reds'])

    with st.container():
        st.markdown('#### Water Consumption Metrics')

        df_consumption_difference_sorted = calculate_water_consumption_difference(
            df, selected_month)

        high_consumption_state_name = df_consumption_difference_sorted.iloc[0]['states']
        high_consumption_value = df_consumption_difference_sorted.iloc[0]['water_consumption']
        high_consumption_delta = int(df_consumption_difference_sorted.iloc[0]['water_consumption'] -
                                     df_consumption_difference_sorted.iloc[1]['water_consumption'])

        low_consumption_state_name = df_consumption_difference_sorted.iloc[-1]['states']
        low_consumption_value = df_consumption_difference_sorted.iloc[-1]['water_consumption']
        low_consumption_delta = int(df_consumption_difference_sorted.iloc[-1]['water_consumption'] -
                                    df_consumption_difference_sorted.iloc[-2]['water_consumption'])

        migrations_col = st.columns((0.2, 1, 0.2))
        with migrations_col[1]:
            st.metric(label=high_consumption_state_name,
                      value=high_consumption_value, delta=high_consumption_delta)
            st.write('High Consumption')
            st.altair_chart(make_donut(high_consumption_value,
                            'High Consumption', selected_color_theme))

            st.metric(label=low_consumption_state_name,
                      value=low_consumption_value, delta=low_consumption_delta)
            st.write('Low Consumption')
            st.altair_chart(make_donut(low_consumption_value,
                            'Low Consumption', selected_color_theme))

# Read the dataset
file_path = 'water_data.csv'
df = pd.read_csv(file_path)
