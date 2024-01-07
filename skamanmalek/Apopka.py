import streamlit as st
import pandas as pd

# Initial values according to the baseline of 2022 for Lake Apopka
initial_values = {
    'Norm_CyAN': 88.106000,
    'AVFST_Max': 88.106000,
    'ARAIN_Average': 184.16,
    'HUC12_TN': 119.289254,
    'HUC10_TP': 15.258894,
    'HUC10_cropland_area_1': 3.332722,
    'HUC12_developed_area_5': 27.275139
}

# Min and max values across all variables for normalization
min_values = {
    'AVFST_Max': 82.04,
    'ARAIN_Average': 163.72,
    'HUC12_TN': 14.37253718,
    'HUC10_TP': 7.105387318,
    'HUC10_cropland_area_1': 0,
    'HUC12_developed_area_5': 0.052616068
}

max_values = {
    'Norm_CyAN': 194.0458755,
    'AVFST_Max': 90.86,
    'ARAIN_Average': 223.83,
    'HUC12_TN': 252.0831295,
    'HUC10_TP': 24.93183214,
    'HUC10_cropland_area_1': 100,
    'HUC12_developed_area_5': 100
}

# Coefficients for Lake Apopka
coefficients = {
    'intercept': 2.485492847,
    'AVFST_Max': 0.360760140263049,
    'ARAIN_Average': -0.225355885697879,
    'HUC12_TN': -2.79949760100647,
    'HUC10_TP': -0.777649170971426,
    'HUC10_cropland_area_1': 0.156721981986119,
    'HUC12_developed_area_5': -0.744617972431082
}

# Streamlit app
st.title('Cyanobacteria Bloom Magnitude Estimation in Lake Apopka ')

# User Input
st.sidebar.title("User Input")
user_AVFST_Max = st.sidebar.slider('Enter AVFST_Max value', 67, 106, initial_values['AVFST_Max'])
user_ARAIN_Average = st.sidebar.slider('Enter ARAIN_Average value', 0, 450, initial_values['ARAIN_Average'])
user_HUC12_TN = st.sidebar.slider('Enter HUC12_TN value', 0, 500, initial_values['HUC12_TN'])
user_HUC10_TP = st.sidebar.slider('Enter HUC10_TP value', 0, 50, initial_values['HUC10_TP'])
user_HUC10_cropland_area_1 = st.sidebar.slider('Enter HUC10_cropland_area_1 value', 0, 100, initial_values['HUC10_cropland_area_1'])
user_HUC12_developed_area_5 = st.sidebar.slider('Enter HUC12_developed_area_5 value', 0, 100, initial_values['HUC12_developed_area_5'])

# Normalization
def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)

# Calculate normalized values
X1 = normalize(user_AVFST_Max, min_values['AVFST_Max'], max_values['AVFST_Max'])
X2 = normalize(user_ARAIN_Average, min_values['ARAIN_Average'], max_values['ARAIN_Average'])
X3 = normalize(user_HUC12_TN, min_values['HUC12_TN'], max_values['HUC12_TN'])
X4 = normalize(user_HUC10_TP, min_values['HUC10_TP'], max_values['HUC10_TP'])
X5 = normalize(user_HUC10_cropland_area_1, min_values['HUC10_cropland_area_1'], max_values['HUC10_cropland_area_1'])
X6 = normalize(user_HUC12_developed_area_5, min_values['HUC12_developed_area_5'], max_values['HUC12_developed_area_5'])

# Calculate predicted Cyanobacteria bloom magnitude
final_bloom_magnitude = coefficients['intercept'] + \
                        X1 * coefficients['AVFST_Max'] + \
                        X2 * coefficients['ARAIN_Average'] + \
                        X3 * coefficients['HUC12_TN'] + \
                        X4 * coefficients['HUC10_TP'] + \
                        X5 * coefficients['HUC10_cropland_area_1'] + \
                        X6 * coefficients['HUC12_developed_area_5']

# Calculate the percentage change
percentage_change = ((final_bloom_magnitude - initial_values['Norm_CyAN']) / initial_values['Norm_CyAN']) * 100

# Display the final result
st.write(f"Initial Cyanobacteria Bloom Magnitude with the Baseline of 2022: {initial_values['Norm_CyAN']:.4f}")
st.write(f"Predicted Cyanobacteria Bloom Magnitude: {final_bloom_magnitude:.4f}")
st.write(f"Percentage Change: {percentage_change:.2f}%")

# Display a message based on the change with color
threshold = 0.001  # Adjust this threshold as needed

if abs(percentage_change) < threshold:
    st.info("The estimated bloom magnitude remains the same.")
elif percentage_change > 0:
    st.error("The annual magnitude of cyanobacteria bloom is predicted to increase.")
else:
    st.success("The annual magnitude of cyanobacteria bloom is predicted to decrease.")

# Bar chart
chart_data = pd.DataFrame({
    'Magnitude Type': ['Initial Bloom Magnitude', 'Predicted Bloom Magnitude'],
    'Magnitude Value': [initial_values['Norm_CyAN'], final_bloom_magnitude]
})
st.bar_chart(chart_data, x='Magnitude Type', y='Magnitude Value')
