import streamlit as st

# Initial values according to the baseline of 2022 for Lake Apopka
initial_values = {
    'Norm_CyAN': 158.3693646,
    'AVFST_Max': 88.106000,
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

# Equations variables
b1, c1, d1, e1, f1, g1 = 82.04, 163.72, 14.37253718, 7.105387318, 0, 0.052616068
b2, c2, d2, e2, f2, g2 = 90.86, 223.83, 252.0831295, 24.93183214, 86.75640259, 79.36556518

# Streamlit App
st.title("Lake Apopka Predicted Magnitude Calculator")

# User Input
AVFST_Max_user = st.slider("AVFST_Max User Input", b1, b2, initial_values['AVFST_Max'])
ARAIN_Average_user = st.slider("ARAIN_Average User Input", c1, c2, initial_values['ARAIN_Average'])
HUC12_TN_user = st.slider("HUC12_TN User Input", d1, d2, initial_values['HUC12_TN'])
HUC10_TP_user = st.slider("HUC10_TP User Input", e1, e2, initial_values['HUC10_TP'])
HUC10_cropland_area_user = st.slider("HUC10_cropland_area User Input", float(f1), float(f2), initial_values['HUC10_cropland_area_1'])
HUC12_developed_area_5_user = st.slider("HUC12_developed_area_5 User Input", float(g1), float(g2), initial_values['HUC12_developed_area_5'])


# Calculate Predicted Magnitude
Y = coefficients['intercept'] + \
    coefficients['AVFST_Max'] * (AVFST_Max_user - b1) / (b2 - b1) + \
    coefficients['ARAIN_Average'] * (ARAIN_Average_user - c1) / (c2 - c1) + \
    coefficients['HUC12_TN'] * (HUC12_TN_user - d1) / (d2 - d1) + \
    coefficients['HUC10_TP'] * (HUC10_TP_user - e1) / (e2 - e1) + \
    coefficients['HUC10_cropland_area_1'] * (HUC10_cropland_area_user - f1) / (f2 - f1) + \
    coefficients['HUC12_developed_area_5'] * (HUC12_developed_area_5_user - g1) / (g2 - g1)

predicted_magnitude = Y * 194.0458755
percent_change = 100 * (predicted_magnitude - initial_values['Norm_CyAN']) / initial_values['Norm_CyAN']

# Display Results
st.subheader("Predicted Magnitude:")
st.write(predicted_magnitude)

st.subheader("Percent Change:")
st.write(percent_change)
