import streamlit as st

# Initial values according to baseline of 2022 for Lake Apopka
initial_values = {
    'Bloom_Magnitude': 147.180228904029,
    'AVFST_Max': 303.12,
    'ARAIN_Average': 184.47,
    'TN_HUC12': 132.57559,
    'TP_HUC10': 16.330554,
    'Cropland_HUC10': 9.385451904,
    'Developed_HUC12': 20.06372067
}

# Min and max values across all variables
min_values = {
    'AVFST_Max': 300.95,
    'ARAIN_Average': 163.72,
    'TN_HUC12': 14.37253718,
    'TP_HUC10': 7.1053873,
    'Cropland_HUC10': 0,
    'Developed_HUC12': 0.052616068
}

max_values = {
    'AVFST_Max': 305.85,
    'ARAIN_Average': 223.83,
    'TN_HUC12': 252.0831295,
    'TP_HUC10': 24.931832,
    'Cropland_HUC10': 86.75640259,
    'Developed_HUC12': 79.36556518
}

# Coefficients for Lake Apopka
coefficients = {
    'intercept': 2.485492847,
    'AVFST_Max': 0.360760140263049,
    'ARAIN_Average': -0.225355885697879,
    'TN_HUC12': -2.79949760100647,
    'TP_HUC10': -0.777649170971426,
    'Cropland_HUC10': 0.156721981986119,
    'Developed_HUC12': -0.744617972431082
}

# Max of Bloom Magnitude
max_bloom_magnitude = 194.0458755

# Streamlit app
st.title('Cyanobacteria Bloom Magnitude Estimation')

# Input fields for user to change initial values
user_inputs = {}
for var in initial_values.keys():
    try:
        min_val = float(min_values.get(var, 0))
        max_val = float(max_values.get(var, 1))
        user_inputs[var] = st.slider(f'Enter {var} value', min_value=min_val, max_value=max_val, value=float(initial_values.get(var, 0)))
    except Exception as e:
        st.write(f"Error: {e}")
        st.write(f"Variable {var} caused an error.")

# Normalize input values
normalized_inputs = {}
for var in initial_values.keys():
    try:
        normalized_inputs[var] = (user_inputs.get(var, 0) - min_values.get(var, 0)) / (max_values.get(var, 1) - min_values.get(var, 0))
        # Ensure values are between 0 and 1
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
final_bloom_magnitude = predicted_y1 * max_bloom_magnitude

# Display results
st.write(f"Initial Bloom Magnitude: {initial_values['Bloom_Magnitude']:.4f}")
st.write(f"Predicted Cyanobacteria annual bloom magnitude_Normalized (Y1): {predicted_y1:.4f}")
st.write(f"Final Cyanobacteria Bloom Magnitude: {final_bloom_magnitude:.4f}")

# Compare with the initial value
percentage_change = ((final_bloom_magnitude - initial_values['Bloom_Magnitude']) / initial_values['Bloom_Magnitude']) * 100
st.write(f"Percentage Change: {percentage_change:.2f}%")
