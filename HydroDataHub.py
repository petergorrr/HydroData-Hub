import streamlit as st
from landslide_risk_assessment_system import display_landslide_risk_interface
from smart_water_meter_system import display_smart_water_meter_interface
from smart_water_meter_system import df

def main():
    st.set_page_config(
        page_title="HydroDataHub",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Welcome to HydroDataHub💧")

    with st.sidebar:
        st.title("Navigation")
        selected_section = st.radio(
            "",
            ["Landslide Risk Assessment System",
                "Smart Water Meter System"]
        )

    if selected_section == "Landslide Risk Assessment System":
        display_landslide_risk_interface()
    elif selected_section == "Smart Water Meter System":
        display_smart_water_meter_interface(df)


if __name__ == "__main__":
    main()
