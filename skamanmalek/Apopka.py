import streamlit as st

# Initial values according to baseline of 2022 for Lake Apopka
initial_values = {
    'Norm_CyAN': 147.180229,  # Initial value for Bloom Magnitude
    'AVFST_Max': 304.32,
    'ARAIN_Average': 184.16,
    'HUC12_TN': 119.289254,
    'HUC10_TP': 15.258894,
    'HUC10_cropland_area_1': 3.332722,
    'HUC12_developed_area_5': 27.275139
}

# Min and max values across all variables for normalization
min_values = {
    'Norm_CyAN': 0,
    'AVFST_Max': 300.95,
    'ARAIN_Average': 163.72,
    'HUC12_TN': 14.37253718,
    'HUC10_TP': 7.105387318,
    'HUC10_cropland_area_1': 0,
    'HUC12_developed_area_5': 0.052616068
}

max_values = {
    'Norm_CyAN': 194.0458755,
    'AVFST_Max': 305.85,
    'ARAIN_Average': 223.83,
    'HUC12_TN': 252.0831295,
    'HUC10_TP': 24.93183214,
    'HUC10_cropland_area_1': 86.75640259,
    'HUC12_developed_area_5': 79.36556518
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
final_bloom_magnitude = predicted_y1 * max_values['Norm_CyAN']

# Display results
st.write(f"Initial Bloom Magnitude: {initial_values['Norm_CyAN']:.4f}")
st.write(f"Predicted Cyanobacteria annual bloom magnitude_Normalized (Y1): {predicted_y1:.4f}")
st.write(f"Final Cyanobacteria Bloom Magnitude: {final_bloom_magnitude:.4f}")

# Compare with the initial value
percentage_change = ((final_bloom_magnitude - initial_values['Norm_CyAN']) / initial_values['Norm_CyAN']) * 100
st.write(f"Percentage Change: {percentage_change:.4f}%")

# Display a message based on the change
if percentage_change > 0:
    st.success("The estimated bloom magnitude has increased.")
elif percentage_change < 0:
    st.error("The estimated bloom magnitude has decreased.")
else:
    st.info("The estimated bloom magnitude remains the same.")
