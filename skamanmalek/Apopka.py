import streamlit as st
import pandas as pd
import numpy as np

# Display the title with blue color and centered text
title_markdown = "<h1 style='color: blue; text-align: center;'>Future Cyanobacteria Bloom Magnitude Estimation in Lake Apopka</h1>"
st.markdown(title_markdown, unsafe_allow_html=True)

# Initial values according to the baseline of 2022 for Lake Apopka
initial_values = {
    'Norm_CyAN': 141.348473,
    'AVFST_Max': 88.106,
    'ARAIN_Average': 184.16,
    'HUC12_forest_and_shrubland_4': 4.511227711,
    'HUC10_grassland_and_pasture_3': 12.92275406,
    'HUC10_cropland_area_1': 3.332721843,
    'HUC12_developed_area_5': 27.27513883
}

# Coefficients for Lake Apopka
coefficients = {
    'intercept': 2.707261329,
    'AVFST_Max': 0.057913537,
    'ARAIN_Average': -0.112755289,
    'HUC12_forest_and_shrubland_4': -0.363781812,
    'HUC10_grassland_and_pasture_3': -5.514615137,
    'HUC10_cropland_area_1': -2.882319595,
    'HUC12_developed_area_5': -2.836429498
}

# Equations variables
b1, c1, d1, e1, f1, g1 = 82.04, 163.72, 0, 0, 0, 0.052616068
b2, c2, d2, e2, f2, g2 = 90.86, 223.83, 80.3992991, 81.38497115, 86.75640259, 79.36556518

# Sidebar for user inputs with icons
st.sidebar.markdown("<h2 style='font-size: 24px;'>🛠️ User Inputs:</h2>", unsafe_allow_html=True)
st.sidebar.write("The default values represent mean annual measurements derived from the 2022 baseline for Lake Apopka.")

# Slider variables:
b3, c3, d3, e3, f3, g3 = 82.04, 0.00, 0.00000000, 0.000000000, 0, 0.000000000
b4, c4, d4, e4, f4, g4 = 106.00, 450.00, 100.00, 100.00, 100.00, 100.00

# User Input in the sidebar with colorful labels
AVFST_Max_user = st.sidebar.slider("**🌡️ AVFST_Max_°F**", b3, b4, initial_values['AVFST_Max'], step=0.1, key="avfst_max", help="Adjust the annual maximum air temperature.")
ARAIN_Average_user = st.sidebar.slider("**🌧️ ARAIN_Average_kg/m^2**", c3, c4, initial_values['ARAIN_Average'], step=0.1, key="arain_average", help="Adjust the annual average rainfall.")
HUC12_forest_and_shrubland_4_user = st.sidebar.slider("**🌲 HUC12_Forest_and_Shrubland_%**", d3, d4, initial_values['HUC12_forest_and_shrubland_4'], step=0.1, key="huc12_forest_shrubland", help="Modify the percentage of forest and shrubland within the HUC12 watershed enclosing the lake.")
HUC10_grassland_and_pasture_3_user = st.sidebar.slider("**🌾 HUC10_Grassland_and_Pasture_%**", e3, e4, initial_values['HUC10_grassland_and_pasture_3'], step=0.1, key="huc10_grassland_pasture", help="Modify the percentage of grassland and pasture within the HUC10 watershed enclosing the lake.")
HUC10_cropland_area_user = st.sidebar.slider("**🌱 HUC10_Cropland_Area_%**", float(f3), float(f4), initial_values['HUC10_cropland_area_1'], step=0.1, key="huc10_cropland", help="Modify the percentage of cropland within the HUC10 watershed enclosing the lake.")
HUC12_developed_area_5_user = st.sidebar.slider("**🏡 HUC12_Developed_Area_%**", float(g3), float(g4), initial_values['HUC12_developed_area_5'], step=0.1, key="huc12_developed", help="Modify the percentage of developed area within the HUC12 watershed enclosing the lake.")

# Calculate Predicted Magnitude
Y = coefficients['intercept'] + \
    coefficients['AVFST_Max'] * (AVFST_Max_user - b1) / (b2 - b1) + \
    coefficients['ARAIN_Average'] * (ARAIN_Average_user - c1) / (c2 - c1) + \
    coefficients['HUC12_forest_and_shrubland_4'] * (HUC12_forest_and_shrubland_4_user - d1) / (d2 - d1) + \
    coefficients['HUC10_grassland_and_pasture_3'] * (HUC10_grassland_and_pasture_3_user - e1) / (e2 - e1) + \
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

chart_data = pd.DataFrame({
    'Magnitude Type': ['Initial Bloom Magnitude', 'Predicted Bloom Magnitude'],
    'Magnitude Value': [initial_values['Norm_CyAN'], final_bloom_magnitude]
})

# Set color based on change direction
bar_colors = ['green' if final_bloom_magnitude < initial_values['Norm_CyAN'] else 'red']

# Display the bar chart with custom styling using Matplotlib
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(chart_data['Magnitude Type'], chart_data['Magnitude Value'], color=bar_colors)

# Customize the appearance of the chart
ax.set_ylabel('Magnitude Value')
ax.set_xlabel('Magnitude Type')
ax.set_title('Bloom Magnitude Comparison')
ax.tick_params(axis='both', which='major', labelsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Add data labels to the bars
for bar, value in zip(bars, chart_data['Magnitude Value']):
    yval = value + 0.02 if value >= 0 else value - 0.02
    ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{value:.2f}', ha='center', va='bottom', fontsize=12)

# Show the chart using st.pyplot
st.pyplot(fig)
