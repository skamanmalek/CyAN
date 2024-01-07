import streamlit as st

# Streamlit app
st.title('Cyanobacteria Bloom Magnitude Estimation in Lake Apopka ')

# User Input
st.sidebar.title("User Input")
user_AVFST_Max = st.sidebar.number_input('Enter AVFST_Max value', min_value=67, max_value=106, value=initial_values['AVFST_Max'])

# Display user input for debugging
st.write("User Input:")
st.write(f"AVFST_Max: {user_AVFST_Max}")
