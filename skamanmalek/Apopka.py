import streamlit as st

# Streamlit app
st.title('Cyanobacteria Bloom Magnitude Estimation in Lake Apopka ')

# User Input
st.sidebar.title("User Input")
user_AVFST_Max = st.sidebar.number_input('Enter AVFST_Max value', min_value=67, max_value=106, value=initial_values['AVFST_Max'])
user_ARAIN_Average = st.sidebar.number_input('Enter ARAIN_Average value', min_value=0, max_value=450, value=initial_values['ARAIN_Average'])
user_HUC12_TN = st.sidebar.number_input('Enter HUC12_TN value', min_value=0, max_value=500, value=initial_values['HUC12_TN'])
user_HUC10_TP = st.sidebar.number_input('Enter HUC10_TP value', min_value=0, max_value=50, value=initial_values['HUC10_TP'])
user_HUC10_cropland_area_1 = st.sidebar.number_input('Enter HUC10_cropland_area_1 value', min_value=0, max_value=100, value=initial_values['HUC10_cropland_area_1'])
user_HUC12_developed_area_5 = st.sidebar.number_input('Enter HUC12_developed_area_5 value', min_value=0, max_value=100, value=initial_values['HUC12_developed_area_5'])

# Display user input for debugging
st.write("User Input:")
st.write(f"AVFST_Max: {user_AVFST_Max}")
st.write(f"ARAIN_Average: {user_ARAIN_Average}")
st.write(f"HUC12_TN: {user_HUC12_TN}")
st.write(f"HUC10_TP: {user_HUC10_TP}")
st.write(f"HUC10_cropland_area_1: {user_HUC10_cropland_area_1}")
st.write(f"HUC12_developed_area_5: {user_HUC12_developed_area_5}")
