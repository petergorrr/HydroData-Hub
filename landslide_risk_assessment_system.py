import streamlit as st
import numpy as np
import pydeck as pdk
import skfuzzy as fuzz
from skfuzzy import control as ctrl



# Function to create the fuzzy system
def create_fuzzy_system():
    # Create input variables
    rainfall = ctrl.Antecedent(np.arange(0, 101, 1), 'rainfall')
    soil_saturation = ctrl.Antecedent(np.arange(0, 101, 1), 'soil_saturation')
    terrain_steepness = ctrl.Antecedent(
        np.arange(0, 101, 1), 'terrain_steepness')
    occurrence_before = ctrl.Antecedent(
        np.arange(0, 101, 1), 'occurrence_before')

    # Create output variable
    landslide_risk = ctrl.Consequent(np.arange(0, 101, 1), 'landslide_risk')

    # Define membership functions
    rainfall['low'] = fuzz.trimf(rainfall.universe, [0, 0, 50])
    rainfall['moderate'] = fuzz.trimf(rainfall.universe, [0, 50, 100])
    rainfall['high'] = fuzz.trimf(rainfall.universe, [50, 100, 100])

    soil_saturation['low'] = fuzz.trimf(soil_saturation.universe, [0, 0, 50])
    soil_saturation['medium'] = fuzz.trimf(
        soil_saturation.universe, [0, 50, 100])
    soil_saturation['high'] = fuzz.trimf(
        soil_saturation.universe, [50, 100, 100])

    terrain_steepness['gentle'] = fuzz.trimf(
        terrain_steepness.universe, [0, 0, 50])
    terrain_steepness['moderate'] = fuzz.trimf(
        terrain_steepness.universe, [0, 50, 100])
    terrain_steepness['steep'] = fuzz.trimf(
        terrain_steepness.universe, [50, 100, 100])

    occurrence_before['no'] = fuzz.trimf(
        occurrence_before.universe, [0, 0, 50])
    occurrence_before['yes'] = fuzz.trimf(
        occurrence_before.universe, [50, 100, 100])

    landslide_risk['low'] = fuzz.trimf(landslide_risk.universe, [0, 0, 50])
    landslide_risk['moderate'] = fuzz.trimf(
        landslide_risk.universe, [0, 50, 100])
    landslide_risk['high'] = fuzz.trimf(
        landslide_risk.universe, [50, 100, 100])

    # Define rules
    rule1 = ctrl.Rule(
        antecedent=(
            (rainfall['low'] & soil_saturation['low'] & occurrence_before['no'])),
        consequent=landslide_risk['low']
    )

    rule2 = ctrl.Rule(
        antecedent=((rainfall['high'] | soil_saturation['high'] | terrain_steepness['steep'] |
                     occurrence_before['yes'])),
        consequent=landslide_risk['high']
    )

    rule3 = ctrl.Rule(
        antecedent=((rainfall['moderate'] & soil_saturation['medium'])),
        consequent=landslide_risk['moderate']
    )

    rule4 = ctrl.Rule(
        antecedent=(terrain_steepness['gentle']),
        consequent=landslide_risk['low']
    )

    rule5 = ctrl.Rule(
        antecedent=((rainfall['high'] & terrain_steepness['moderate'])),
        consequent=landslide_risk['moderate']
    )

    rule6 = ctrl.Rule(
        antecedent=((soil_saturation['high'] & terrain_steepness['gentle'])),
        consequent=landslide_risk['moderate']
    )

    rule7 = ctrl.Rule(
        antecedent=((rainfall['moderate'] & terrain_steepness['steep'])),
        consequent=landslide_risk['high']
    )

    # Create the control system
    return ctrl.ControlSystem(rules=[rule1, rule2, rule3, rule4, rule5, rule6, rule7])


# Function to calculate landslide risk
def calculate_landslide_risk(fuzzy_system, inputs):
    landslide_sim = ctrl.ControlSystemSimulation(fuzzy_system)
    landslide_sim.input['rainfall'] = inputs['rainfall']
    landslide_sim.input['soil_saturation'] = inputs['soil_saturation']
    landslide_sim.input['terrain_steepness'] = inputs['terrain_steepness']
    landslide_sim.input['occurrence_before'] = inputs['occurrence_before']
    landslide_sim.compute()
    return landslide_sim.output['landslide_risk']


# Function to map risk to category
def map_risk_to_category(landslide_risk_result):
    if landslide_risk_result <= 30:
        return "Low Risk"
    elif 30 < landslide_risk_result <= 70:
        return "Moderate Risk"
    else:
        return "High Risk"


# Function to display landslide risk assessment interface
def display_landslide_risk_interface():

    with st.sidebar:
        st.title("Landslide Risk Assessment System")
        st.image("images/landslide.jpg", use_column_width=True)
        st.info(
            "This app uses a fuzzy logic system to assess landslide risk based on input parameters. "
            "Adjust the parameters and click 'Calculate Risk' to see the results on the map."
        )

    # Add a section to explain the algorithm/rules
    st.header("Algorithm Rules")
    st.markdown(
        """
        - **Rule 1:** If rainfall is low, soil saturation is low, and no occurrence before, then the landslide risk is low.
        - **Rule 2:** If any of the following conditions are met - high rainfall, high soil saturation, steep terrain, or an occurrence before - the landslide risk is high.
        - **Rule 3:** If rainfall is moderate and soil saturation is medium, then the landslide risk is moderate.
        - **Rule 4:** If the terrain is gentle, then the landslide risk is low.
        - **Rule 5:** If both rainfall and terrain steepness are high, the landslide risk is moderate.
        - **Rule 6:** If soil saturation is high and terrain steepness is gentle, the landslide risk is moderate.
        - **Rule 7:** If rainfall is moderate and terrain steepness is steep, the landslide risk is high.
        """
    )

    # User Input: Latitude and Longitude
    st.header("Location Coordinates")
    latitude_longitude = st.text_input(
        "Enter Latitude and Longitude (comma-separated):", "5.4085,100.2773")
    latitude, longitude = map(float, latitude_longitude.split(','))

    # User Input: Fuzzy Logic Variables
    st.header("Landslide Risk Parameters")
    with st.expander("Input Standardised Parameters", expanded=True):
        rainfall_value = st.slider("Select Rainfall (0-100):", 0, 100, 50)
        saturation_value = st.slider(
            "Select Soil Saturation (0-100):", 0, 100, 50)
        steepness_value = st.slider(
            "Select Terrain Steepness (0-100):", 0, 100, 50)
        occurrence_before_value = st.radio(
            "Was there an Occurrence Before?", ['No', 'Yes'])

    # Convert the occurrence_before_value to a numerical value
    occurrence_mapping = {'No': 25, 'Yes': 75}
    occurrence_before_num = occurrence_mapping[occurrence_before_value]

    inputs = {
        'rainfall': float(rainfall_value),
        'soil_saturation': float(saturation_value),
        'terrain_steepness': float(steepness_value),
        'occurrence_before': float(occurrence_before_num)
    }

    # Create and calculate fuzzy system
    fuzzy_system = create_fuzzy_system()

    if st.button("Calculate Risk"):
        landslide_risk_result = calculate_landslide_risk(fuzzy_system, inputs)
        risk_category = map_risk_to_category(landslide_risk_result)

        # Display the risk category with enhanced styling and additional information
        category_color = 'red' if risk_category == 'High Risk' else 'orange' if risk_category == 'Moderate Risk' else 'green'

        # Add additional information based on the risk category
        if risk_category == 'High Risk':
            additional_info = "This area is at high risk of landslides. Please take necessary precautions."
        elif risk_category == 'Moderate Risk':
            additional_info = "This area has a moderate risk of landslides. Stay vigilant and monitor the surroundings."
        else:
            additional_info = "This area is in a safe zone with low risk of landslides. Enjoy the surroundings responsibly."

        styled_message = f'<div style="background-color: #f8f9fa; padding: 10px; border-radius: 10px; border: 1px solid {category_color}; color: {category_color}; font-size: 18px;">Landslide Risk: {landslide_risk_result:.2f}% - Category: {risk_category}<br>{additional_info}</div>'
        st.markdown(styled_message, unsafe_allow_html=True)

        # Display Map with PyDeck Scatter Plot
        st.header("GIS of Penang Hill Biosphere Reserve")
        with st.expander("Landslide Hazard Map", expanded=True):
            # Create PyDeck Scatter Plot data
            data = [{"latitude": latitude, "longitude": longitude,
                     "risk": landslide_risk_result}]

            # Create PyDeck Scatter Plot
            scatter_layer = pdk.Layer(
                "ScatterplotLayer",
                data,
                get_position="[longitude, latitude]",
                get_radius=200,
                get_fill_color="[255, risk, 0]",
                pickable=True,
                opacity=0.8,
                stroked=True,
                filled=True,
                extruded=True,
            )

            # Set the initial view state
            view_state = pdk.ViewState(
                latitude=latitude,
                longitude=longitude,
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