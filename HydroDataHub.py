from landslide_risk_assessment_system import *
from smart_water_meter_system import *

def main():
    st.set_page_config(page_title="HydroDataHub",
                       page_icon="🌍",
                       layout="wide",
                       initial_sidebar_state="expanded")

    st.title("Welcome to HydroDataHub💧")

    with st.sidebar:
        st.title("Navigation")
        selected_section = st.radio(
            "", ["Landslide Risk Assessment System", "Smart Water Meter System (still in progress⚒️)"])

    if selected_section == "Landslide Risk Assessment System":
        display_landslide_risk_interface()
    elif selected_section == "Smart Water Meter System (still in progress⚒️)":
        display_smart_water_meter_interface()


if __name__ == "__main__":
    main()
