pip install pandas

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Initial values according to baseline of 2022 for Lake Apopka
initial_values = {
    'Norm_CyAN': 158.3693646,  # Initial value for Bloom Magnitude
    'AVFST_Max': 304.32,
    'ARAIN_Average': 184.16,
    'HUC12_TN': 119.289254,
    'HUC10_TP': 15.258894,
    'HUC10_cropland_area_1': 3.332722,
    'HUC12_developed_area_5': 27.275139
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

# Input fields for user to change initial values
user_inputs = {}
for var in initial_values.keys():
    try:
        user_inputs[var] = st.slider(f'Enter {var} value', min_value=0.0, max_value=initial_values[var] * 2, value=initial_values[var])
    except Exception as e:
        st.write(f"Error: {e}")
        st.write(f"Variable {var} caused an error.")

# Normalize input values
normalized_inputs = {var: user_inputs.get(var, 0) / initial_values[var] for var in initial_values.keys()}

# Calculate Predicted Cyanobacteria annual bloom magnitude_Normalized (Y1)
predicted_y1 = coefficients['intercept'] + sum(coef * normalized_inputs.get(var, 0) for var, coef in coefficients.items() if var != 'intercept')
predicted_y1 = max(0, min(1, predicted_y1))

# Calculate Cyanobacteria annual bloom magnitude
final_bloom_magnitude = predicted_y1 * initial_values['Norm_CyAN']

# Calculate the percentage change
percentage_change = ((final_bloom_magnitude - initial_values['Norm_CyAN']) / initial_values['Norm_CyAN']) * 100

# Display a message based on the change with color
if percentage_change < 0:
    st.error("The annual magnitude of cyanobacteria bloom is predicted to decrease.")
else:
    st.success("The annual magnitude of cyanobacteria bloom is predicted to increase.")

# Bar chart
chart_data = pd.DataFrame({'Initial Bloom Magnitude': [initial_values['Norm_CyAN']], 'Predicted Bloom Magnitude': [final_bloom_magnitude]})
st.bar_chart(chart_data)
