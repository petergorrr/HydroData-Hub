import streamlit as st
import numpy as np
import pydeck as pdk
import skfuzzy as fuzz
from skfuzzy import control as ctrl


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
    # Membership functions for rainfall
    rainfall['low'] = fuzz.trimf(rainfall.universe, [0, 0, 50])
    rainfall['moderate'] = fuzz.trimf(rainfall.universe, [0, 50, 100])
    rainfall['high'] = fuzz.trimf(rainfall.universe, [50, 100, 100])

    # Membership functions for soil saturation
    soil_saturation['low'] = fuzz.trimf(soil_saturation.universe, [0, 0, 50])
    soil_saturation['medium'] = fuzz.trimf(
        soil_saturation.universe, [0, 50, 100])
    soil_saturation['high'] = fuzz.trimf(
        soil_saturation.universe, [50, 100, 100])

    # Membership functions for terrain steepness
    terrain_steepness['gentle'] = fuzz.trimf(
        terrain_steepness.universe, [0, 0, 50])
    terrain_steepness['moderate'] = fuzz.trimf(
        terrain_steepness.universe, [0, 50, 100])
    terrain_steepness['steep'] = fuzz.trimf(
        terrain_steepness.universe, [50, 100, 100])

    # Membership functions for occurrence before
    occurrence_before['no'] = fuzz.trimf(
        occurrence_before.universe, [0, 0, 50])
    occurrence_before['yes'] = fuzz.trimf(
        occurrence_before.universe, [50, 100, 100])

    # Membership functions for landslide risk
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


def calculate_landslide_risk(fuzzy_system, inputs):
    landslide_sim = ctrl.ControlSystemSimulation(fuzzy_system)
    landslide_sim.input['rainfall'] = inputs['rainfall']
    landslide_sim.input['soil_saturation'] = inputs['soil_saturation']
    landslide_sim.input['terrain_steepness'] = inputs['terrain_steepness']
    landslide_sim.input['occurrence_before'] = inputs['occurrence_before']
    landslide_sim.compute()
    return landslide_sim.output['landslide_risk']



def map_risk_to_category(landslide_risk_result):
    if landslide_risk_result <= 30:
        return "Safe"
    elif 30 < landslide_risk_result <= 70:
        return "Moderate"
    else:
        return "High"


# Function to provide advice based on landslide risk level and input parameters
def provide_advice(landslide_risk_level, inputs):
    advice = ""
    if landslide_risk_level == 'Safe':
        if inputs['rainfall'] <= 30:
            advice += "Rainfall is low. It's relatively safe, but keep an eye on any changes. "
        elif 30 < inputs['rainfall'] <= 60:
            advice += "Rainfall is moderate. Exercise caution and monitor for any signs of saturation. "
        else:
            advice += "Rainfall is high. Although the risk is low, be vigilant for any unusual activity. "

        if inputs['soil_saturation'] <= 40:
            advice += "Soil saturation is moderate. Stay alert for signs of instability. "
        elif 40 < inputs['soil_saturation'] <= 70:
            advice += "Soil saturation is high. Avoid steep slopes and areas prone to erosion. "
        else:
            advice += "Soil saturation is very high. Evacuate immediately to higher ground. "

        if inputs['terrain_steepness'] <= 40:
            advice += "Terrain is moderately steep. Continue to monitor for any changes. "
        elif 40 < inputs['terrain_steepness'] <= 70:
            advice += "Terrain is very steep. Exercise caution and avoid steep areas. "
        else:
            advice += "Terrain is extremely steep. Evacuate to high ground immediately. Do not return until it's safe. "
    elif landslide_risk_level == 'Moderate':
        if inputs['rainfall'] <= 30:
            advice += "Rainfall is low, but soil saturation and terrain steepness pose moderate risk. "
        elif 30 < inputs['rainfall'] <= 60:
            advice += "Rainfall is moderate. Exercise caution due to moderate soil saturation and terrain steepness. "
        else:
            advice += "Rainfall is high. Be extremely cautious due to high soil saturation and steep terrain. "
    elif landslide_risk_level == 'High':
        advice += "High risk of landslide due to extreme conditions. Immediate evacuation is necessary. "
    else:
        advice = "Invalid risk level. Please input a valid risk level (Low Risk, Moderate Risk, High Risk)."

    return advice


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
    with st.expander("Standardised Parameters", expanded=True):
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

        # Determine the color based on the risk category
        if risk_category == 'High':
            category_color = 'red'
        elif risk_category == 'Moderate':
            category_color = 'orange'
        else:
            category_color = 'green'

        # Provide advice based on the calculated risk level and input parameters
        advice = provide_advice(risk_category, inputs)

        # Define the legend for risk levels
        legend = """
            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 10px; border: 1px solid #ddd; font-size: 16px;">
                <h3 style="margin-bottom: 10px;">Risk Category</h3>
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <span style="color: green; font-size: 24px; margin-right: 10px;">&#9679;</span>
                    <span style="margin-right: 10px;">Safe</span>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <span style="color: orange; font-size: 24px; margin-right: 10px;">&#9679;</span>
                    <span style="margin-right: 10px;">Moderate</span>
                </div>
                <div style="display: flex; align-items: center;">
                    <span style="color: red; font-size: 24px; margin-right: 10px;">&#9679;</span>
                    <span>High</span>
                </div>
            </div>
        """

        # Generate HTML for the risk breakdown
        risk_breakdown = """
            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 10px; border: 1px solid #ddd; font-size: 16px;">
                <h3 style="margin-bottom: 10px;">Risk Breakdown</h3>
        """

        # Combine the legend and risk breakdown into one component
        combined_legend_and_breakdown = f"""
            <div style="display: flex; justify-content: space-between;">
                {legend}
                {risk_breakdown}
            </div>
        """

        # Combine the risk figure, combined legend and breakdown, and advice into one component
        combined_component = f"""
            <div>
                <div style="background-color: #f8f9fa; padding: 10px; border-radius: 10px; border: 1px solid {category_color}; color: {category_color}; font-size: 18px; margin-bottom: 20px;text-align:center">
                    Landslide Risk: {landslide_risk_result:.2f}% - Risk Category: {risk_category}
                </div>
                {combined_legend_and_breakdown}
            </div>
        """

        # Display the combined component
        st.markdown(combined_component, unsafe_allow_html=True)

        # Display the advice with custom font
        st.header("Advice on Site")
        st.write(advice, unsafe_allow_html=True)

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
