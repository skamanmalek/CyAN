import streamlit as st
import pandas as pd

# Initial values according to the baseline of 2022 for Lake Apopka
initial_values = {
    'Norm_CyAN': 158.3694,
    'AVFST_Max': 304.32,
    'ARAIN_Average': 184.16,
    'HUC12_TN': 119.289254,
    'HUC10_TP': 15.258894,
    'HUC10_cropland_area_1': 3.332722,
    'HUC12_developed_area_5': 27.275139
}

# Streamlit app
st.title('Cyanobacteria Bloom Magnitude Estimation in Lake Apopka')

# Input fields for the user to change initial values
user_inputs = {}
normalized_inputs = {}
for var in initial_values.keys():
    if var != 'Norm_CyAN':
        try:
            min_val = float(initial_values[var] * 0.8)
            max_val = float(initial_values[var] * 1.2)
            user_inputs[var] = st.slider(f'Enter {var} value', min_value=min_val, max_value=max_val, value=initial_values[var])

            # Add input box for percentage change
            percentage_change_input = st.text_input(f'Enter % change for {var}', value="0.0")

            try:
                # Parse percentage change input
                percentage_change = float(percentage_change_input)
                # Adjust user input based on percentage change
                user_inputs[var] *= (1 + percentage_change / 100)
            except ValueError:
                st.warning(f"Please enter a valid numerical value for % change for {var}. Using default value.")
        except Exception as e:
            st.write(f"Error: {e}")
            st.write(f"Variable {var} caused an error.")

        try:
            # Normalize input values and ensure they are between 0 and 1
            normalized_inputs[var] = (user_inputs.get(var, 0) - min_values.get(var, 0)) / (max_values.get(var, 1) - min_values.get(var, 0))
            normalized_inputs[var] = max(0, min(1, normalized_inputs[var]))
        except Exception as e:
            st.write(f"Error: {e}")
            st.write(f"Variable {var} caused an error.")

# Calculate Predicted Cyanobacteria annual bloom magnitude_Normalized (Y1)
predicted_y1 = coefficients['intercept']
for var, coef in coefficients.items():
    if var != 'intercept' and var != 'Norm_CyAN':
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
