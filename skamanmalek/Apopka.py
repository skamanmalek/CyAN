
import streamlit as st

st.title('CyAN in Lake Apopka')
streamlit run Apopka.py

# Your regression coefficients
coefficients = {
    'intercept': 2.485492847,
    'AVFST_Max': 0.360760140263049,
    'ARAIN_Average': -0.225355885697879,
    'HUC12_TN': -2.79949760100647,
    'HUC10_TP': -0.777649170971426,
    'HUC10_cropland': 0.156721981986119,
    'HUC12_developed': -0.744617972431082
}

# Initial values
initial_values = {
    'HUC10_cropland_area_1_N': 0.038415,
    'HUC10_TP_N': 0.457383,
    'HUC12_developed_area_5_N': 0.343229,
    'HUC12_TN_N': 0.441363,
    'ARAIN_Average_N': 0.340043,
    'AVFST_Max_N': 0.687755
}

# Calculate the initial result
initial_result = coefficients['intercept']
for var, coef in coefficients.items():
    if var != 'intercept':
        initial_result += coef * initial_values[f'{var}_N']

# Streamlit app
st.title("Cyanobacteria Concentrations Estimation")

# Input fields for user to change values
user_values = {}
for var in initial_values.keys():
    user_values[var] = st.number_input(f'Enter {var}', value=initial_values[var])

# Calculate the result based on user input
user_result = coefficients['intercept']
for var, coef in coefficients.items():
    if var != 'intercept':
        user_result += coef * user_values[var]

# Display the initial and user results
st.write(f"Initial Cyanobacteria Concentration: {initial_result:.4f}")
st.write(f"User's Estimated Cyanobacteria Concentration: {user_result:.4f}")

# Compare with the initial value
if user_result > initial_result:
    st.success("The estimated concentration has increased.")
elif user_result < initial_result:
    st.error("The estimated concentration has decreased.")
else:
    st.info("The estimated concentration remains the same.")

streamlit run Apopka_app.py

