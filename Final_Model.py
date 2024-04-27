import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# read dataset
df = pd.read_csv("water_data.csv")

# encode categorical variables

# Label encode 'Month' column
le_Month = LabelEncoder()
df['Month'] = le_Month.fit_transform(df['Month'])
df['Month'].unique()

# Label encode 'Area' column
le_Area = LabelEncoder()
df['Area'] = le_Area.fit_transform(df['Area'])
df['Area'].unique()

# Label encode 'Weather' column
le_Weather = LabelEncoder()
df['Weather'] = le_Weather.fit_transform(df['Weather'])
df['Weather'].unique()

# Label encode 'Festival' column
le_Festival = LabelEncoder()
df['Festival'] = le_Festival.fit_transform(df['Festival'])
df['Festival'].unique()

# List of variables you want to include
selected_features = ["Month", "Area", "Weather","Festival","No_Visitor_Area","No_Residence_Area"]

# Separate features (X) and target variable (y)
X = df[selected_features]
y = df["Avg_Usage_Litre"]

# Import RandomForestRegressor and initialize it
from sklearn.ensemble import RandomForestRegressor
random_forest_reg = RandomForestRegressor(random_state=0)

# Fit the RandomForestRegressor model to the data
random_forest_reg.fit(X, y.values)

# Make predictions using the trained model
y_pred = random_forest_reg.predict(X)

# Import pickle module

import pickle

# Store the trained model and label encoders in a dictionary
data = {"model": random_forest_reg, "le_Month": le_Month, "le_Area": le_Area, "le_Weather": le_Weather, "le_Festival": le_Festival}

# Save the dictionary to a file using pickle
with open('water_model.pkl', 'wb') as file:
    pickle.dump(data, file)
