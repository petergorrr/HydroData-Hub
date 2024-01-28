import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import folium
import webbrowser

# Fixed location for Penang Hill
PENANG_HILL_COORDINATES = [5.4085, 100.2773]


# Function to create a folium map centered on Penang Hill
def create_penang_hill_map():
    m = folium.Map(location=PENANG_HILL_COORDINATES, zoom_start=15)
    folium.Marker(PENANG_HILL_COORDINATES, popup='Penang Hill').add_to(m)
    return m

# Function to create a circle marker with color intensity based on landslide risk
def create_circle_marker(lat, lon, result):
    color_intensity = int(result)
    return folium.CircleMarker(
        [lat, lon],
        radius=8,
        popup=f'Landslide Risk: {result:.2f}%',
        color=f'#{color_intensity:02x}0000',
        fill=True,
        fill_color=f'#{color_intensity:02x}0000',
        fill_opacity=0.7
    )

# Function to visualize the results on a map
def visualize_on_map(result):
    penang_hill_map = create_penang_hill_map()

    # Take input values from the user (excluding location as it's fixed to Penang Hill)
    rainfall_input = float(input("Enter rainfall value (0-100): "))
    soil_saturation_input = float(input("Enter soil saturation value (0-100): "))
    terrain_steepness_input = float(input("Enter terrain steepness value (0-100): "))

    # Compute the result using fuzzy logic
    landslide_sim.input['rainfall'] = rainfall_input
    landslide_sim.input['soil_saturation'] = soil_saturation_input
    landslide_sim.input['terrain_steepness'] = terrain_steepness_input
    landslide_sim.compute()

    result = landslide_sim.output['landslide_risk']

    # Print the result
    print(f"Landslide Risk: {result:.2f}")

    # Add a circle marker to the map based on the computed result
    circle_marker = create_circle_marker(PENANG_HILL_COORDINATES[0], PENANG_HILL_COORDINATES[1], result)
    circle_marker.add_to(penang_hill_map)

    # Save the map as an HTML file
    map_filename = 'landslide_map.html'
    penang_hill_map.save(map_filename)

    # Open the map in the default web browser
    webbrowser.open(map_filename)

# Create input variables
rainfall = ctrl.Antecedent(np.arange(0, 101, 1), 'rainfall')
soil_saturation = ctrl.Antecedent(np.arange(0, 101, 1), 'soil_saturation')
terrain_steepness = ctrl.Antecedent(np.arange(0, 101, 1), 'terrain_steepness')

# Create output variable
landslide_risk = ctrl.Consequent(np.arange(0, 101, 1), 'landslide_risk')

# Define membership functions
rainfall['low'] = fuzz.trimf(rainfall.universe, [0, 0, 50])
rainfall['moderate'] = fuzz.trimf(rainfall.universe, [0, 50, 100])
rainfall['high'] = fuzz.trimf(rainfall.universe, [50, 100, 100])

soil_saturation['low'] = fuzz.trimf(soil_saturation.universe, [0, 0, 50])
soil_saturation['medium'] = fuzz.trimf(soil_saturation.universe, [0, 50, 100])
soil_saturation['high'] = fuzz.trimf(soil_saturation.universe, [50, 100, 100])

terrain_steepness['gentle'] = fuzz.trimf(terrain_steepness.universe, [0, 0, 50])
terrain_steepness['moderate'] = fuzz.trimf(terrain_steepness.universe, [0, 50, 100])
terrain_steepness['steep'] = fuzz.trimf(terrain_steepness.universe, [50, 100, 100])

landslide_risk['low'] = fuzz.trimf(landslide_risk.universe, [0, 0, 50])
landslide_risk['moderate'] = fuzz.trimf(landslide_risk.universe, [0, 50, 100])
landslide_risk['high'] = fuzz.trimf(landslide_risk.universe, [50, 100, 100])

# Define rules
rule1 = ctrl.Rule(antecedent=((rainfall['low'] & soil_saturation['low'])),
                  consequent=landslide_risk['low'])

rule2 = ctrl.Rule(antecedent=((rainfall['high'] | soil_saturation['high'] | terrain_steepness['steep'])),
                  consequent=landslide_risk['high'])

rule3 = ctrl.Rule(antecedent=((rainfall['moderate'] & soil_saturation['medium'])),
                  consequent=landslide_risk['moderate'])

rule4 = ctrl.Rule(antecedent=(terrain_steepness['gentle']),
                  consequent=landslide_risk['low'])

rule5 = ctrl.Rule(antecedent=((rainfall['high'] & terrain_steepness['moderate'])),
                  consequent=landslide_risk['moderate'])

rule6 = ctrl.Rule(antecedent=((soil_saturation['high'] & terrain_steepness['gentle'])),
                  consequent=landslide_risk['moderate'])

rule7 = ctrl.Rule(antecedent=((rainfall['moderate'] & terrain_steepness['steep'])),
                  consequent=landslide_risk['high'])

# Create the control system
landslide_ctrl = ctrl.ControlSystem(rules=[rule1, rule2, rule3, rule4, rule5, rule6, rule7])
landslide_sim = ctrl.ControlSystemSimulation(landslide_ctrl)

# Visualize the result on a map and open it in the default web browser
visualize_on_map(0)