import streamlit as st

# Function to normalize input values
def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)

# Function to calculate predicted bloom magnitude
def calculate_bloom_magnitude(user_values, coefficients, min_max_values):
    normalized_values = [normalize(user_values[i], min_max_values[i][0], min_max_values[i][1]) for i in range(len(user_values))]
    predicted_y1 = coefficients['intercept']
    for i in range(len(coefficients) - 1):
        predicted_y1 += coefficients[f'X{i+1}'] * normalized_values[i]
    
    return predicted_y1 * min_max_values[-1][1]

# Initial values according to baseline of 2022 for Lake Apopka
initial_values = {
    'Bloom Magnitude': 147.180228904029,
    'AVFST_Max': 303.12,
    'ARAIN_Average': 184.47,
    'TN_HUC12': 132.57559,
    'TP_HUC10': 16.330554,
    'Cropland_HUC10': 9.385451904,
    'Developed_HUC12': 20.06372067,
}

# Min and max across all
min_max_values = {
    'AVFST_Max': (67, 106),
    'ARAIN_Average': (163.72, 223.83),
    'TN_HUC12': (14.37253718, 252.0831295),
    'TP_HUC10': (7.1053873, 24.931832),
    'Cropland_HUC10': (0, 86.75640259),
    'Developed_HUC12': (0.052616068, 79.36556518),
    'Bloom_Magnitude': (0, 194.0458755),
}

# Coefficients for Lake Apopka
coefficients = {
    'intercept': 2.485492847,
    'X1': 0.360760140263049,
    'X2': -0.225355885697879,
    'X3': -2.79949760100647,
    'X4': -0.777649170971426,
    'X5': 0.156721981986119,
    'X6': -0.744617972431082,
}

# Streamlit app
st.title("Cyanobacteria Bloom Magnitude Estimation")

# Input sliders for user to change initial values
user_values = {
    'HUC10_cropland_area_1': st.slider("Enter HUC10 Cropland Area (%)", 0, 100, initial_values['Cropland_HUC10']),
    'HUC12_developed_area_5': st.slider("Enter HUC12 Developed Area (%)", 0, 100, initial_values['Developed_HUC12']),
    'HUC10_TP': st.slider("Enter HUC10 TP Value", 0, 50, initial_values['TP_HUC10']),
    'HUC12_TN': st.slider("Enter HUC12 TN Value", 0, 500, initial_values['TN_HUC12']),
    'ARAIN': st.slider("Enter ARAIN Value", 0, 450, initial_values['ARAIN_Average']),
    'AVFST_Max': st.slider("Enter AVFST_Max Value", 67, 106, initial_values['AVFST_Max']),
}

# Calculate predicted bloom magnitude
predicted_bloom_magnitude = calculate_bloom_magnitude(
    [user_values['AVFST_Max'], user_values['ARAIN'], user_values['HUC12_TN'],
     user_values['HUC10_TP'], user_values['HUC10_cropland_area_1'],
     user_values['HUC12_developed_area_5']],
    coefficients,
    [(min_max_values['AVFST_Max'][0], min_max_values['AVFST_Max'][1]),
     (min_max_values['ARAIN_Average'][0], min_max_values['ARAIN_Average'][1]),
     (min_max_values['TN_HUC12'][0], min_max_values['TN_HUC12'][1]),
     (min_max_values['TP_HUC10'][0], min_max_values['TP_HUC10'][1]),
     (min_max_values['Cropland_HUC10'][0], min_max_values['Cropland_HUC10'][1]),
     (min_max_values['Developed_HUC12'][0], min_max_values['Developed_HUC12'][1]),
     (min_max_values['Bloom_Magnitude'][0], min_max_values['Bloom_Magnitude'][1])]
)

# Display predicted bloom magnitude
st.subheader("Predicted Cyanobacteria Bloom Magnitude (Normalized):")
st.write(predicted_bloom_magnitude)

# Calculate actual bloom magnitude
initial_bloom_magnitude = initial_values['Bloom Magnitude']
actual_bloom_magnitude = predicted_bloom_magnitude * min_max_values['Bloom_Magnitude'][1]

# Display actual bloom magnitude
st.subheader("Actual Cyanobacteria Bloom Magnitude:")
st.write(actual_bloom_magnitude)

# Compare and display percentage change
percentage_change = ((actual_bloom_magnitude - initial_bloom_magnitude) / initial_bloom_magnitude) * 100
st.subheader("Percentage Change:")
st.write(f"{percentage_change:.2f}%")
