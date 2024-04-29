import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load dataset
df = pd.read_csv("water_data.csv")

# Initialize Label Encoders
le_Month = LabelEncoder()
le_Area = LabelEncoder()
le_Weather = LabelEncoder()
le_Festival = LabelEncoder()

# Encode categorical variables
df['Month'] = le_Month.fit_transform(df['Month'])
df['Area'] = le_Area.fit_transform(df['Area'])
df['Weather'] = le_Weather.fit_transform(df['Weather'])
df['Festival'] = le_Festival.fit_transform(df['Festival'])

# Selected features for the model
selected_features = ["Month", "Area", "Weather", "Festival", "No_Visitor_Area", "No_Residence_Area"]

# Separate features (X) and target variable (y)
X = df[selected_features]
y = df["Avg_Usage_Litre"]

# Initialize and fit the RandomForestRegressor model
random_forest_reg = RandomForestRegressor(random_state=0)
random_forest_reg.fit(X, y)

# Optional: Make predictions using the trained model
# y_pred = random_forest_reg.predict(X)

# Store the trained model and label encoders in a dictionary
model_data = {
    "model": random_forest_reg,
    "le_Month": le_Month,
    "le_Area": le_Area,
    "le_Weather": le_Weather,
    "le_Festival": le_Festival
}

# Save the dictionary to a file using pickle for later use
with open('water_model.pkl', 'wb') as file:
    pickle.dump(model_data, file)
