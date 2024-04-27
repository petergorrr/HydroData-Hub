import base64
import io

import numpy as np
import pandas as pd
import pydeck as pdk
import skfuzzy as fuzz
from PIL import Image
from skfuzzy import control as ctrl
import streamlit as st

from image_processing import detect_and_annotate

# Generates a download link for a text report
def get_download_link(report_content, filename="Landslide_Risk_Analysis_Report.txt"):
    bytes_report = report_content.encode()
    b64 = base64.b64encode(bytes_report).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download Report</a>'
    return href

# Static text-based risk analysis display
def static_risk_analysis():
    analysis_text = """
    <div style='border: 2px solid #4CAF50; background-color: #f4f4f4; padding: 20px; border-radius: 10px;'>
        <h3 style='color: #2c3e50;'>Landslide Risk Analysis Report</h3>
        <ul>
            <li><strong>Rainfall and Soil Moisture</strong> 🌧️: The site experiences average rainfall, which typically does not immediately threaten slope stability. Continuous monitoring of rainfall patterns is essential, especially during peak rainfall seasons. Soil moisture levels should be regularly checked using soil moisture sensors to preempt any potential risk due to unexpected heavy downpours.</li>
            <li><strong>Vegetation and Soil Conservation</strong> 🌱: The current vegetative cover is adequate but could be improved to enhance soil stability and water absorption capacity. Implementing additional soil conservation measures such as terracing and the planting of deep-rooted vegetation can significantly mitigate erosion risks.</li>
            <li><strong>Human Activity</strong> 👥: The area exhibits moderate human activity. It is recommended to conduct stability assessments before initiating any construction or large-scale land modifications. Areas with frequent human activity should be regularly inspected for signs of soil displacement or structural weakness.</li>
            <li><strong>Drainage System</strong> 🌊: Ensuring that drainage systems are well-maintained and capable of handling peak water flow is crucial. An inadequate drainage system can lead to water accumulation, which significantly increases the risk of landslides. Regular inspections and cleaning of drainage pathways are advised.</li>
            <li><strong>Observation of New Cracks</strong> 🔍: New cracks have been observed on the site, indicating potential subsurface movements. These should be addressed immediately to prevent any escalation. Geotechnical assessments should be carried out to determine the underlying causes of these cracks.</li>
            <li><strong>Overall Risk Level</strong> ⚠️: Based on the assessment, the current risk level of the site is classified as moderate. While there is no immediate threat, the combination of factors such as occasional heavy rainfall, observed new cracks, and human activities could escalate the situation. It is recommended to implement monitoring systems and consider preventive measures like reinforcing slope structures and improving water management systems.</li>
        </ul>
        <h4 style='color: #27ae60;'>Recommendations:</h4>
        <ul>
            <li>Install real-time monitoring systems for rainfall and soil moisture 🌧️📊.</li>
            <li>Enhance vegetation cover with species suitable for erosion control 🌿🌾.</li>
            <li>Regularly inspect and maintain the drainage system 🛠️🌊.</li>
            <li>Conduct detailed geotechnical evaluations in areas where new cracks have appeared 🔎🏞️.</li>
            <li>Develop a community awareness program on landslide risks and emergency procedures 📢🔗.</li>
        </ul>
    </div>
    """
    return analysis_text

def create_fuzzy_system():
        # Antecedent/Consequent objects hold universe variables and membership functions
        rainfall = ctrl.Antecedent(np.arange(0, 1001, 1), 'rainfall')
        soil_moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'soil_moisture')
        slope_steepness = ctrl.Antecedent(np.arange(0, 101, 1), 'slope_steepness')
        human_activity = ctrl.Antecedent(np.arange(0, 101, 1), 'human_activity')
        historical_landslides = ctrl.Antecedent(np.arange(0, 101, 1), 'historical_landslides')
        soil_type = ctrl.Antecedent(np.arange(0, 6, 1), 'soil_type')
        drainage_system = ctrl.Antecedent(np.arange(0, 101, 1), 'drainage_system')
        vegetated_surface = ctrl.Antecedent(np.arange(0, 101, 1), 'vegetated_surface')
        slope_nature = ctrl.Antecedent(np.arange(0, 101, 1), 'slope_nature')
        
        soil_nailing = ctrl.Antecedent(np.arange(0, 101, 1), 'soil_nailing')
        slope_netting = ctrl.Antecedent(np.arange(0, 101, 1), 'slope_netting')
        gabion_wall = ctrl.Antecedent(np.arange(0, 101, 1), 'gabion_wall')
        rubble_wall = ctrl.Antecedent(np.arange(0, 101, 1), 'rubble_wall')

        landslide_risk = ctrl.Consequent(np.arange(0, 101, 1), 'landslide_risk')

        # Auto-membership function population is possible with .automf
        rainfall.automf(3)
        soil_moisture.automf(3)
        slope_steepness.automf(3)
        human_activity.automf(3)
        historical_landslides.automf(3)
        drainage_system.automf(3)
        vegetated_surface.automf(3)
        
        soil_nailing.automf(3)
        slope_netting.automf(3)
        gabion_wall.automf(3)
        rubble_wall.automf(3)

        # Custom membership functions can be built interactively with a familiar Pythonic API
        soil_type['clay'] = fuzz.trimf(soil_type.universe, [0, 0, 1])
        soil_type['sand'] = fuzz.trimf(soil_type.universe, [1, 1, 2])
        soil_type['loam'] = fuzz.trimf(soil_type.universe, [2, 2, 3])
        soil_type['peat'] = fuzz.trimf(soil_type.universe, [3, 3, 4])
        soil_type['chalk'] = fuzz.trimf(soil_type.universe, [4, 4, 5])
        soil_type['silt'] = fuzz.trimf(soil_type.universe, [5, 5, 5])
        
        # Membership functions for slope nature
        slope_nature['natural'] = fuzz.trimf(slope_nature.universe, [0, 0, 50])
        slope_nature['engineered'] = fuzz.trimf(slope_nature.universe, [50, 100, 100])

        landslide_risk = ctrl.Consequent(np.arange(0, 101, 1), 'landslide_risk')

        # Custom membership functions for landslide risk
        landslide_risk['safe'] = fuzz.trimf(landslide_risk.universe, [0, 0, 30])
        landslide_risk['moderate'] = fuzz.trimf(landslide_risk.universe, [20, 50, 80])
        landslide_risk['high'] = fuzz.trimf(landslide_risk.universe, [70, 100, 100])

        # Define complex rules using fuzzy logic operators
        rule1 = ctrl.Rule(antecedent=(
            (rainfall['poor'] & soil_moisture['poor']) |
            (slope_steepness['poor'] & vegetated_surface['good']) |
            (human_activity['good'] & historical_landslides['good'])),
            consequent=landslide_risk['high'])

        rule2 = ctrl.Rule(antecedent=(
            (rainfall['average'] & drainage_system['average']) |
            (soil_type['clay'] & slope_nature['natural'])),
            consequent=landslide_risk['moderate'])

        rule3 = ctrl.Rule(antecedent=(
            (rainfall['good'] & soil_moisture['good']) |
            (vegetated_surface['poor'] & slope_steepness['good'])),
            consequent=landslide_risk['safe'])

        # Control System Creation and Simulation
        landslide_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
        landslide_simulation = ctrl.ControlSystemSimulation(landslide_ctrl)

        return landslide_simulation    


# Landslide risk calculation using the fuzzy system
def calculate_landslide_risk(fuzzy_system, inputs):
    for key, value in inputs.items():
        fuzzy_system.input[key] = value
    fuzzy_system.compute()
    return fuzzy_system.output['landslide_risk']


# Map numerical risk score to categorical description
def map_risk_to_category(risk_score):
    if risk_score <= 30:
        return "Safe"
    elif 30 < risk_score <= 70:
        return "Moderate"
    else:
        return "High"


# Set up the main title for the application
st.title("Landslide Risk Assessment System")

# Sidebar setup
with st.sidebar:
    # Display an image with description
    st.image("images/landslide.jpg", use_column_width=True)
    # Information section about the app usage
    st.info("This app uses a fuzzy logic system to assess landslide risk based on input parameters. Adjust the parameters and click 'Calculate Risk' to see the results on the map.")
    # Display legal and copyright information
    st.markdown("---")
    st.write("This application is for authorized use only.")
    st.markdown("Copyright © Make Water OK Malaysia")
    st.markdown("---")
    
    # Data sources and references section
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
                <li><a href="https://weather.com/" class="source-link" target="_blank">Rainfall Data - The Weather Company</a></li>
                <li><a href="https://www.usgs.gov/" class="source-link" target="_blank">Slope Steepness Data - USGS</a></li>
                <li><a href="https://smap.jpl.nasa.gov/" class="source-link" target="_blank">Soil Moisture Data - NASA's SMAP satellite</a></li>
                <li>Human Activity Data - Local government reports or construction industry records</li>
                <li>Groundwater Impact Data - Environmental protection agencies or geological surveys</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Function to determine color based on risk category
def get_risk_color(risk_category):
    if risk_category == "Safe":
        return "#32CD32"  # LimeGreen
    elif risk_category == "Moderate":
        return "#FFA500"  # Orange
    elif risk_category == "High":
        return "#FF4500"  # OrangeRed
    else:
        return "#FF0000"  # Red

# Main form for landslide risk assessment
with st.form("risk_assessment_form"):
    
    # Header for the form
    st.header("Assessment of Location and Environmental Risk Factors")

    # Assessment Date Entry
    col_date, _ = st.columns([1, 3])
    with col_date:
        assessment_date = st.date_input("Assessment Date")

    # Split the form into two columns
    col1, col2 = st.columns(2)

    import streamlit as st

    # First column for location, slope, and human activity details
    with col1:
        # Input for latitude coordinate
        latitude = st.number_input("Latitude Coordinate:", value=5.422500, format="%.6f")

        # Section header for slope inspection
        st.markdown("#### Inspection of Slope Conditions")

        # Input for the area covered by the slope
        slope_area_cover = st.number_input(
            "Area Covered by Slope (km²)", min_value=0.0, format="%.5f",
            help="Specify the slope's surface area in square kilometers."
        )

        # Input for the height of vegetation or material covering the slope
        surface_cover_height = st.number_input(
            "Height of Surface Cover (m)", min_value=0, value=100, step=1,
            help="Indicate the average height of the vegetation or material covering the slope."
        )

        # Dropdown for selecting slope steepness category
        slope_steepness_selection = st.selectbox(
            "Slope Steepness Category (%):",
            ['0-4.9 (Very Gentle)', '5-9.9 (Gentle)', '10-14.9 (Moderate)', 
             '15-19.9 (Steep)', '20-24.9 (Very Steep)', '25-29.9 (Extremely Steep)', 
             '>=30 (Precipitous)'],
            help="Choose the appropriate slope steepness category."
        )

        # Radio buttons to specify the nature of the slope
        slope_nature = st.radio(
            "Nature of Slope:",
            ('Natural', 'Engineered'),
            help="Specify whether the slope is a natural formation or has been modified by human activity."
        )

        # Dropdown for selecting the range of vegetation coverage on the slope
        coverage_of_vegetation = st.selectbox(
            "Vegetation Coverage on Slope in Percentage:",
            options=['0-10%', '11-20%', '21-30%', '31-40%', '41-50%', '51-60%', '61-70%', '71-80%', '81-90%', '91-100%'],
            help="Select the range that best describes the percentage of vegetation coverage on the slope."
        )

        # Section header for human activity impact
        st.markdown("## Impact of Human Activity")

        # Radio buttons to indicate the presence of human activity
        presence_of_human_activity = st.radio(
            "Presence of Human Activity:",
            ('Absent', 'Present'),
            help="Indicate whether there is any human activity present in the area."
        )

        # Expander for entering details about the human activity
        with st.expander("Activity Details", expanded=True):
            type_of_activity = st.text_input(
                "Activity Description",
                placeholder="Describe the type of human activity (e.g., residential, agricultural, logging)."
            )
            activity_details = st.text_area(
                "Additional Notes",
                placeholder="Enter any pertinent notes regarding the human activity.",
                height=120
            )

    # Second column for longitude, soil conditions, rainfall, and structural features
    with col2:
        # Input for longitude coordinate
        longitude = st.number_input("Longitude Coordinate:", value=100.271400, format="%.6f")

        # Section header for soil condition evaluation
        st.markdown("#### Soil Condition Evaluation")
        selection_of_soil_type = st.selectbox(
            "Soil Composition:",
            options=['Clay', 'Sand', 'Loam', 'Peat', 'Chalk', 'Silt'],
            help="Select the type of soil composition in the area."
        )
        level_of_soil_moisture = st.slider(
            "Soil Moisture Percentage (%):",
            min_value=0, max_value=100, value=50,
            help="Adjust the slider to estimate the current percentage of moisture content in the soil."
        )

        # Section header for rainfall forecasting
        st.markdown("#### Forecasting of Rainfall")
        expected_rainfall = st.number_input(
            "Projected Rainfall (mm) for the Next 3 Months:",
            min_value=0, value=300, step=10,
            help="Enter the projected total amount of rainfall expected in millimeters (mm) for the next three months. This information is crucial for assessing seasonal risks and planning appropriate mitigation strategies."
        )

        # Section header for structural features
        st.markdown("## Presence of Structural Features")
        st.markdown("#### Drainage System Condition")
        drainage_system_condition = st.selectbox(
            "Drainage System Condition:",
            options=['Clogged', 'Requires Maintenance', 'In Good Condition'],
            help="Select the current condition of the drainage system."
        )

        # Inputs for installed slope stabilization measures
        st.markdown("#### Installed Slope Stabilization Measures")
        installed_soil_nail = st.checkbox("Soil Nails")
        installed_netting = st.checkbox("Erosion Control Netting")
        installed_gabion = st.checkbox("Gabion Walls")
        installed_rubble = st.checkbox("Rubble Masonry Walls")

    # General input for historical landslide occurrences outside the columns
    historical_landslide_occurrences = st.radio(
        "Record of Previous Landslides in This Area:",
        options=["Yes", "No"], index=1,
        help="Information on past landslides can help evaluate the risk of recurrence."
    )

    # Submit button for the form
    submit_button = st.form_submit_button("Calculate Risk")


if 'uploaded_image' not in st.session_state:
    st.session_state['uploaded_image'] = None

# Check if the submit button was pressed
if submit_button:
    # Updated mappings for user inputs to numerical values
    human_activity_levels = {'Absent': 0, 'Present': 100}
    vegetation_coverage_levels = {
        '0-10%': 5, '11-20%': 15, '21-30%': 25,
        '31-40%': 35, '41-50%': 45, '51-60%': 55,
        '61-70%': 65, '71-80%': 75, '81-90%': 85,
        '91-100%': 95
    }
    drainage_conditions = {'Clogged': 25, 'Requires Maintenance': 50, 'In Good Condition': 75}
    historical_landslide_presence = {'Yes': 100, 'No': 0}
    slope_nature_levels = {'Natural': 0, 'Engineered': 100}
    slope_stabilization_measures = {
        'Soil Nails': 100,
        'Erosion Control Netting': 100,
        'Gabion Walls': 100,
        'Rubble Masonry Walls': 100
    }
    soil_types = {'Clay': 0, 'Sand': 1, 'Loam': 2, 'Peat': 3, 'Chalk': 4, 'Silt': 5}

    # Helper function to convert slope steepness selection to a numerical value
    def convert_slope_steepness_to_numerical(slope_steepness_category):
        slope_steepness_mapping = {
            '0-4.9 (Very Gentle)': 5,
            '5-9.9 (Gentle)': 10,
            '10-14.9 (Moderate)': 15,
            '15-19.9 (Steep)': 20,
            '20-24.9 (Very Steep)': 25,
            '25-29.9 (Extremely Steep)': 30,
            '>=30 (Precipitous)': 35
        }
        return slope_steepness_mapping[slope_steepness_category]

     # Collect inputs for the fuzzy logic risk calculation
    inputs = {
        'rainfall': expected_rainfall,  # User input for projected rainfall
        'soil_moisture': level_of_soil_moisture,  # User input for soil moisture level
        'slope_steepness': convert_slope_steepness_to_numerical(slope_steepness_selection),  # Converted from user input
        'human_activity': human_activity_levels[presence_of_human_activity],  # Mapped from user input
        'historical_landslides': historical_landslide_presence[historical_landslide_occurrences],  # Mapped from user input
        'soil_type': soil_types[selection_of_soil_type],  # Mapped from user input
        'drainage_system': drainage_conditions[drainage_system_condition],  # Mapped from user input
        'vegetated_surface': vegetation_coverage_levels[coverage_of_vegetation],  # Mapped from user input
        'slope_nature': slope_nature_levels[slope_nature],  # Mapped from user input
        
        # Each stabilization measure is checked if installed and given a corresponding numerical value
        # 'soil_nailing': slope_stabilization_measures['Soil Nails'] if installed_soil_nail else 0,
        # 'slope_netting': slope_stabilization_measures['Erosion Control Netting'] if installed_netting else 0,
        # 'gabion_wall': slope_stabilization_measures['Gabion Walls'] if installed_gabion else 0,
        # 'rubble_wall': slope_stabilization_measures['Rubble Masonry Walls'] if installed_rubble else 0,
    }

    # Execute fuzzy logic system
    fuzzy_system = create_fuzzy_system()
    risk_score = calculate_landslide_risk(fuzzy_system, inputs)
    risk_category = map_risk_to_category(risk_score)

    # Determine the color based on the risk category
    risk_color = get_risk_color(risk_category)

    # Enhanced output display with dynamic color and improved font styling
    st.markdown(f"""
    <div style='background-color:#f0f2f6; padding:20px; border-radius:12px; border: 4px solid {risk_color}; margin-bottom: 20px; text-align:center;'>
        <h2 style='color:{risk_color}; font-size: 24px; font-family: Arial, sans-serif;'>
            Landslide Risk Score: {risk_score:.2f}% 🤔<br>Risk Level: {risk_category} ⚠️
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Adding a spacer
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    
st.subheader("Upload an Image For Visual Inspection")
uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    image_np = np.array(Image.open(io.BytesIO(bytes_data)))

    # Process the image and annotate it
    annotated_image_np = detect_and_annotate(image_np)

    # Convert numpy array to PIL Image for display in Streamlit
    annotated_image = Image.fromarray(annotated_image_np.astype('uint8'), 'RGB')

    # Display the annotated image
    st.image(annotated_image, caption='Processed Image with Annotation', use_column_width=True)

    st.success("A Landslide Risk Analysis Report is generated.")
    # Expander for landslide risk analysis report
    with st.expander("View Landslide Risk Analysis Report", expanded=False):
        risk_analysis_text = static_risk_analysis()
        st.markdown(risk_analysis_text, unsafe_allow_html=True)
        
        # Adding a spacer
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

        # Add a button to download the report
        download_button_text = "Download Report"
        st.download_button(label=download_button_text, 
                           data=risk_analysis_text,
                           file_name="Landslide_Risk_Analysis_Report.txt",
                           mime="text/plain")
        
    # Create a data frame for the location and risk score
    map_data = pd.DataFrame({
        'lat': [latitude],
        'lon': [longitude],
        'risk_score': [risk_score],
        'risk_category': [risk_category]
    })

    # Set the viewport location for the map
    view_state = pdk.ViewState(
        latitude=latitude,
        longitude=longitude,
        zoom=11,
        pitch=50,
    )

    # Create the map layer
    risk_layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position='[lon, lat]',
        get_color='[200, 30, 0, 160]' if risk_category == 'High' else '[30, 200, 0, 160]',
        get_radius=100,  # Radius is given in meters
    )

    # Render the map with pydeck
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[risk_layer],
    ))

