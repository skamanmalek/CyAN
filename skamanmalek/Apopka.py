import streamlit as st
import pandas as pd

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

# Input fields for the user to change initial values
user_inputs = {}
percentage_changes = {}
normalized_inputs = {}

for var in coefficients.keys():
    if var != 'intercept':
        try:
            min_val = float(min_values.get(var, 0))
            max_val = float(max_values.get(var, 1))

            # Define specific ranges for each variable
            if var == 'HUC10_cropland_area_1':
                min_val, max_val = 0, 100
            elif var == 'HUC12_developed_area_5':
                min_val, max_val = 0, 100
            elif var == 'HUC10_TP':
                min_val, max_val = 0, 50
            elif var == 'HUC12_TN':
                min_val, max_val = 0, 500
            elif var == 'ARAIN_Average':
                min_val, max_val = 0, 450
            elif var == 'AVFST_Max':
                min_val, max_val = 67, 106

            # Input box for user to add +/- percentage change
            percentage_changes[var] = st.number_input(f'Enter percentage change for {var}', min_value=-100.0, max_value=100.0, step=1.0, key=f"{var}_percentage")

            # Calculate user input based on percentage change
            user_inputs[var] = initial_values[var] * (1 + percentage_changes[var] / 100)

            # Ensure user input is within the specified range
            user_inputs[var] = max(min_val, min(max_val, user_inputs[var]))

            # Normalize input values and ensure they are between 0 and 1
            normalized_inputs[var] = (user_inputs[var] - min_val) / (max_val - min_val)
            normalized_inputs[var] = max(0, min(1, normalized_inputs[var]))

        except Exception as e:
            st.write(f"Error: {e}")
            st.write(f"Variable {var} caused an error.")

# Calculate Predicted Cyanobacteria annual bloom magnitude_Normalized (Y1)
predicted_y1 = coefficients['intercept']

for var, coef in coefficients.items():
    if var != 'intercept':
        try:
            predicted_y1 += coef * normalized_inputs.get(var, 0)
        except Exception as e:
            st.write(f"Error: {e}")
            st.write(f"Variable {var} caused an error.")

# Ensure values of X1 to X6 are between 0 and 1
predicted_y1 = max(0, min(1, predicted_y1))

# Calculate Cyanobacteria annual bloom magnitude
final_bloom_magnitude = predicted_y1 * max_values['Norm_CyAN']

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
