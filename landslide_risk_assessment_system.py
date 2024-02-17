import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def define_membership_function(variable, names, points):
    for name, point in zip(names, points):
        variable[name] = fuzz.trimf(variable.universe, point)


def create_rule(conditions, output):
    return ctrl.Rule(antecedent=conditions, consequent=output)


def create_fuzzy_system():
    # Antecedent/Consequent objects hold universe variables and membership functions
    variables = {
        'rainfall': np.arange(0, 101, 1),
        'soil_saturation': np.arange(0, 101, 1),
        'terrain_steepness': np.arange(0, 101, 1),
        'occurrence_before': np.arange(0, 101, 1),
        'landslide_risk': np.arange(0, 101, 1)
    }

    # Create input and output variables
    inputs = {k: ctrl.Antecedent(
        v, k) for k, v in variables.items() if k != 'landslide_risk'}
    landslide_risk = ctrl.Consequent(
        variables['landslide_risk'], 'landslide_risk')

    # Membership function names and points for inputs
    mf_names = {
        'rainfall': ['low', 'moderate', 'high'],
        'soil_saturation': ['low', 'medium', 'high'],
        'terrain_steepness': ['gentle', 'moderate', 'steep'],
        'occurrence_before': ['no', 'yes']
    }

    mf_points = {
        'rainfall': [[0, 0, 50], [0, 50, 100], [50, 100, 100]],
        'soil_saturation': [[0, 0, 50], [0, 50, 100], [50, 100, 100]],
        'terrain_steepness': [[0, 0, 50], [0, 50, 100], [50, 100, 100]],
        'occurrence_before': [[0, 0, 50], [50, 100, 100]]
    }

    # Define membership functions for inputs
    for var_name, names in mf_names.items():
        define_membership_function(
            inputs[var_name], names, mf_points[var_name])

    # Define membership functions for landslide risk
    landslide_risk_mf_names = ['low', 'moderate', 'high']
    landslide_risk_mf_points = [[0, 0, 50], [0, 50, 100], [50, 100, 100]]
    define_membership_function(
        landslide_risk, landslide_risk_mf_names, landslide_risk_mf_points)

    # Define rules
    rules = [
        create_rule((inputs['rainfall']['low'] & inputs['soil_saturation']
                    ['low'] & inputs['occurrence_before']['no']), landslide_risk['low']),
        create_rule((inputs['rainfall']['high'] | inputs['soil_saturation']['high'] |
                    inputs['terrain_steepness']['steep'] | inputs['occurrence_before']['yes']), landslide_risk['high']),
        create_rule((inputs['rainfall']['moderate'] &
                    inputs['soil_saturation']['medium']), landslide_risk['moderate']),
        create_rule((inputs['terrain_steepness']['gentle']),
                    landslide_risk['low']),
        create_rule((inputs['rainfall']['high'] & inputs['terrain_steepness']
                    ['moderate']), landslide_risk['moderate']),
        create_rule((inputs['soil_saturation']['high'] &
                    inputs['terrain_steepness']['gentle']), landslide_risk['moderate']),
        create_rule((inputs['rainfall']['moderate'] &
                    inputs['terrain_steepness']['steep']), landslide_risk['high'])
    ]

    return ctrl.ControlSystem(rules)


def calculate_landslide_risk(fuzzy_system, inputs):
    landslide_sim = ctrl.ControlSystemSimulation(fuzzy_system)
    for k, v in inputs.items():
        landslide_sim.input[k] = v
    landslide_sim.compute()
    return landslide_sim.output['landslide_risk']


def map_risk_to_category(landslide_risk_result):
    if landslide_risk_result <= 30:
        return "Safe"
    elif 30 < landslide_risk_result <= 70:
        return "Moderate"
    else:
        return "High"


def provide_advice(risk_category, inputs):
    # Example simplified advice logic
    advice = {
        'Safe': "It's relatively safe, but remain vigilant for any changes.",
        'Moderate': "Exercise caution and monitor for any signs of instability.",
        'High': "Immediate evacuation is necessary due to high risk."
    }
    return advice.get(risk_category, "Invalid risk level. Please input a valid risk level.")


def display_landslide_risk_interface():

    with st.sidebar:
        st.title("Landslide Risk Assessment System")
        st.image("images/landslide.jpg", use_column_width=True)
        st.info(
            "This app uses a fuzzy logic system to assess landslide risk based on input parameters. "
            "Adjust the parameters and click 'Calculate Risk' to see the results on the map."
        )

    # Algorithm Overview

    st.markdown(
        """
        <div style="background-color:#FA9203; border-radius: 10px; padding: 20px;">
            <h3 style="color: #333333; font-size: 20px; margin-bottom: 10px;"><strong>Algorithm Overview🧑‍💻<strong></h3>
            <p style="color: #000000; font-size: 16px;">The landslide risk assessment involves standardizing several input parameters, including <strong>rainfall</strong>, <strong>soil saturation</strong>, and <strong>terrain steepness</strong>, through separate models tailored for each parameter.</p>
            <p style="color: #000000; font-size: 16px;">Here's the rationale behind standardizing each parameter:</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Rainfall Parameter Standardization
    st.markdown(
        """
        <div style="background-color: lightblue; border-radius: 5px; padding: 15px; margin-bottom: 10px;">
            <h4 style="color: steelblue; font-size: 18px; margin-bottom: 10px;"><span>&#x1F327;</span> Rainfall Parameter Standardization:</h4>
            <ul style="color: #333333; font-size: 16px;">
                <li>A model is constructed using advanced statistical techniques and machine learning algorithms. It incorporates inputs such as <strong>rain intensity</strong>, <strong>duration</strong>, <strong>prevailing wind</strong>, and other relevant meteorological data.</li>
                <li>The model undergoes rigorous training and validation processes using historical landslide data and meteorological records.</li>
                <li>Upon successful training, the model produces a standardized output value representing the extent of influence of <strong>rainfall</strong> towards landslide risk.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Soil Saturation Parameter Standardization
    st.markdown(
        """
        <div style="background-color: lightgreen; border-radius: 5px; padding: 15px; margin-bottom: 10px;">
            <h4 style="color: #1c7527; font-size: 18px; margin-bottom: 10px;"><span>🌱</span> Soil Saturation Parameter Standardization:</h4>
            <ul style="color: #333333; font-size: 16px;">
                <li>Another specialized model is developed using comprehensive geotechnical data and environmental factors. It considers inputs such as <strong>soil depth</strong>, <strong>soil type</strong>, <strong>rock status</strong>, and other relevant soil properties.</li>
                <li>The model undergoes thorough calibration and validation procedures utilizing ground truth data from field surveys and laboratory experiments.</li>
                <li>Upon completion, the model generates a standardized output value indicating the influence extent of <strong>soil saturation</strong> towards landslide risk.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Terrain Steepness Parameter Standardization
    st.markdown(
        """
        <div style="background-color: #fde0e0; border-radius: 5px; padding: 15px; margin-bottom: 10px;">
            <h4 style="color: #af2e2e; font-size: 18px; margin-bottom: 10px;"><span>🐌</span> Terrain Steepness Parameter Standardization:</h4>
            <ul style="color: #333333; font-size: 16px;">
                <li>A separate model is developed utilizing advanced terrain analysis techniques and remote sensing data. It takes into account inputs such as <strong>inclination</strong>, <strong>height</strong>, <strong>gravity erosion</strong>, and other pertinent terrain characteristics.</li>
                <li>The model is fine-tuned through extensive validation against high-resolution elevation data and geological surveys.</li>
                <li>Once trained, the model provides a standardized output value reflecting the influence extent of <strong>terrain steepness</strong> towards landslide risk.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # User Input: Latitude and Longitude
    st.header("Location Coordinates")
    latitude_longitude = st.text_input(
        "Enter Latitude and Longitude (comma-separated):", "5.4085,100.2773")
    latitude, longitude = map(float, latitude_longitude.split(','))

    # User Input: Fuzzy Logic Variables
    st.header("Landslide Risk Parameters")
    with st.expander("Standardised Values of the Parameters", expanded=True):
        rainfall_value = st.slider("Select Rainfall (0-100):", 0, 100, 50)
        saturation_value = st.slider(
            "Select Soil Saturation (0-100):", 0, 100, 50)
        steepness_value = st.slider(
            "Select Terrain Steepness (0-100):", 0, 100, 50)
        occurrence_before_value = st.radio(
            "Was there an Occurrence Before?", ['No', 'Yes'])

    st.write("*Note: The standardized value indicates the* ***extent of influence towards landslide risk***.")

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
                <h3 style="margin-bottom: 10px; text-align: center;">Risk Level ⚠️</h3>
                <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 5px;">
                    <span style="color: green; font-size: 24px; margin-right: 10px;">&#9679;</span>
                    <span style="margin-right: 10px;">Safe</span>
                </div>
                <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 5px;">
                    <span style="color: orange; font-size: 24px; margin-right: 10px;">&#9679;</span>
                    <span style="margin-right: 10px;">Moderate</span>
                </div>
                <div style="display: flex; align-items: center; justify-content: center;">
                    <span style="color: red; font-size: 24px; margin-right: 10px;">&#9679;</span>
                    <span>High</span>
                </div>
            </div>
        """

        # Generate HTML for the risk breakdown
        risk_breakdown = f"""
            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 10px; border: 1px solid #ddd; font-size: 16px;">
                <h3 style="margin-bottom: 10px;text-align:center">Risk Breakdown 💡</h3>
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; align-items: center; margin-bottom: 5px;">
                        <span style="font-size: 20px; color: #333333; margin-right: 10px;">🌧️</span>
                        <span style="margin-right: 10px;">Rainfall: {rainfall_value}</span>
                        <span style="color: #666666;">(Low rainfall indicates lower risk of landslides)</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 5px;">
                        <span style="font-size: 20px; color: #333333; margin-right: 10px;">🌿</span>
                        <span style="margin-right: 10px;">Soil Saturation: {saturation_value}</span>
                        <span style="color: #666666;">(Higher soil saturation increases the risk of landslides)</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 5px;">
                        <span style="font-size: 20px; color: #333333; margin-right: 10px;">🏞️</span>
                        <span style="margin-right: 10px;">Terrain Steepness: {steepness_value}</span>
                        <span style="color: #666666;">(Steep terrain is more prone to landslides)</span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 20px; color: #333333; margin-right: 10px;">🔄</span>
                        <span style="margin-right: 10px;">Landslide Occurrence: {occurrence_before_value}</span>
                        <span style="color: #666666;">(Past occurrences may increase landslide risk)</span>
                    </div>
                </div>
                <div style="color: #555555; font-style: italic;">*Note: The values displayed above represent standardized scores indicating the influence of each parameter on landslide risk. Higher values suggest a higher level of risk associated with the respective parameter.</div>
            </div>
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
                    Landslide Risk: {landslide_risk_result:.2f}% - Risk Level: {risk_category}
                </div>
                {combined_legend_and_breakdown}
            </div>
        """

        # Display the combined component
        st.markdown(combined_component, unsafe_allow_html=True)

       # Display the advice with custom font
        st.markdown(
            """
            <div style="background-color: #CCCCFF; border-radius: 10px; padding: 20px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); font-family: 'Cambria', sans-serif;">
                <h3 style="color: #333333; font-size: 28px; margin-bottom: 15px;">Advice on Site 📝</h3>
                <p style="color: black; font-size: 18px; line-height: 1.6; margin-bottom: 0;">{}</p>
            </div>
            """.format(advice),
            unsafe_allow_html=True
        )

        # Display Map with PyDeck Scatter Plot
        st.header("GIS of Penang Hill Biosphere Reserve(PHBR) 🗺️")
        with st.expander("Landslide Hazard Map 📌", expanded=True):
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

        # Generate the report data (example DataFrame)
        report_data = pd.DataFrame({
            'Parameter': ['Rainfall', 'Soil Saturation', 'Terrain Steepness', 'Latitude', 'Longitude', 'Risk Figure', 'Risk Category', 'Advice'],
            'Value': [rainfall_value, saturation_value, steepness_value, latitude, longitude, landslide_risk_result, risk_category, advice]
        })

        # Convert DataFrame to CSV bytes
        csv_bytes = report_data.to_csv(index=False).encode('utf-8')

        # Create the download button
        st.download_button(
            label="Download Landslide Report",
            data=csv_bytes,
            file_name='report.csv',
            mime='text/csv',
            key='download_button'
        )
