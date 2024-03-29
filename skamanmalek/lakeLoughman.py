import streamlit as st
import pandas as pd
import numpy as np

# Display the title with blue color and centered text
title_markdown = "<h1 style='color: blue; text-align: center;'>Future Cyanobacteria Bloom Magnitude Estimation in Lake Loughman</h1>"
st.markdown(title_markdown, unsafe_allow_html=True)

# Initial values according to the baseline of 2022 for Lake Apopka
initial_values = {
    'Norm_CyAN': 4.549010771,
    'AVFST_Max': 86.36,
    'ARAIN_Average': 209.22,
    'HUC12_TN': 73.6433821,
    'HUC10_TP': 11.97515674,
    'HUC10_cropland_area_1': 0.300320475,
    'HUC12_developed_area_5': 23.06545779
}

# Coefficients for Lake Apopka
coefficients = {
    'intercept': -0.705691884,
    'AVFST_Max': -0.064113312,
    'ARAIN_Average': 0.013554092,
    'HUC12_TN': -2.636986212,
    'HUC10_TP': 3.251485488,
    'HUC10_cropland_area_1': -0.108026466,
    'HUC12_developed_area_5': 1.791915403
}

# Equations variables
b1, c1, d1, e1, f1, g1 = 82.04, 163.72, 14.37253718, 7.105387318, 0, 0.052616068
b2, c2, d2, e2, f2, g2 = 90.86, 223.83, 252.0831295, 24.93183214, 86.75640259, 79.36556518



# Sidebar for user inputs with icons
st.sidebar.markdown("<h2 style='font-size: 24px;'>🛠️ User Inputs:</h2>", unsafe_allow_html=True)
st.sidebar.write("The default values represent mean annual measurements derived from the 2022 baseline for Lake Loughman.")


# Slider variables:
b3, c3, d3, e3, f3, g3 = 82.04, 0.00, 0.00000000, 0.000000000, 0, 0.000000000
b4, c4, d4, e4, f4, g4 = 106.00, 450.00, 500.00, 50.00, 100.00, 100.00

# User Input in the sidebar with colorful labels
AVFST_Max_user = st.sidebar.slider("**🌡️ AVFST_Max_°F**", b3, b4, initial_values['AVFST_Max'], step=0.1, key="avfst_max", help="Adjust max air temperature.")
ARAIN_Average_user = st.sidebar.slider("**🌧️ ARAIN_Average_kg/m^2**", c3, c4, initial_values['ARAIN_Average'], step=0.1, key="arain_average", help="Adjust average rainfall.")
HUC12_TN_user = st.sidebar.slider("**🔍 HUC12_TN_mg/L**", d3, d4, initial_values['HUC12_TN'], step=0.1, key="huc12_tn", help="Adjust total nitrogen.")
HUC10_TP_user = st.sidebar.slider("**📊 HUC10_TP_mg/L**", e3, e4, initial_values['HUC10_TP'], step=0.1, key="huc10_tp", help="Adjust total phosphorus.")
HUC10_cropland_area_user = st.sidebar.slider("**🌱 HUC10_Cropland_Area_%**", float(f3), float(f4), initial_values['HUC10_cropland_area_1'], step=0.1, key="huc10_cropland", help="Adjust % cropland area.")
HUC12_developed_area_5_user = st.sidebar.slider("**🏡 HUC12_Developed_Area_%**", float(g3), float(g4), initial_values['HUC12_developed_area_5'], step=0.1, key="huc12_developed", help="Adjust % developed area.")


# Calculate Predicted Magnitude
Y = coefficients['intercept'] + \
    coefficients['AVFST_Max'] * (AVFST_Max_user - b1) / (b2 - b1) + \
    coefficients['ARAIN_Average'] * (ARAIN_Average_user - c1) / (c2 - c1) + \
    coefficients['HUC12_TN'] * (HUC12_TN_user - d1) / (d2 - d1) + \
    coefficients['HUC10_TP'] * (HUC10_TP_user - e1) / (e2 - e1) + \
    coefficients['HUC10_cropland_area_1'] * (HUC10_cropland_area_user - f1) / (f2 - f1) + \
    coefficients['HUC12_developed_area_5'] * (HUC12_developed_area_5_user - g1) / (g2 - g1)

final_bloom_magnitude = Y * 194.0458755
percentage_change = (final_bloom_magnitude - initial_values['Norm_CyAN']) / initial_values['Norm_CyAN'] * 100

# Main content to display the output with an icon
st.header("📈 Model Output")

# Bar chart data
chart_data = pd.DataFrame({
    'Magnitude Type': ['Initial Bloom Magnitude', 'Predicted Bloom Magnitude'],
    'Magnitude Value': [initial_values['Norm_CyAN'], final_bloom_magnitude]
})

# Display the final result with bold text
st.write(f"**Initial Cyanobacteria Bloom Magnitude with the Baseline of 2022:** {initial_values['Norm_CyAN']:.4f}")
st.write(f"**Predicted Cyanobacteria Bloom Magnitude:** {final_bloom_magnitude:.4f}")

# Display the percentage change with bold text
st.write(f"**Percentage Change:** {percentage_change:.2f}%")

# Display a message based on the change with color and bold text
threshold = 0.001

if abs(percentage_change) < threshold:
    st.info("**The estimated bloom magnitude remains the same.**")
elif percentage_change > 0:
    st.error("**The annual magnitude of cyanobacteria bloom is predicted to increase.**")
else:
    st.success("**The annual magnitude of cyanobacteria bloom is predicted to decrease.**")


# Bar chart
chart_data = pd.DataFrame({
    'Magnitude Type': ['Initial Bloom Magnitude', 'Predicted Bloom Magnitude'],
    'Magnitude Value': [initial_values['Norm_CyAN'], final_bloom_magnitude]
})

# Display the bar chart
st.bar_chart(chart_data, x='Magnitude Type', y='Magnitude Value')




