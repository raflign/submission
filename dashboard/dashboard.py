import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

# Load the main data
url = 'https://raw.githubusercontent.com/raflign/submission/main/dashboard/main_data.csv'
data = pd.read_csv(url)

# Data Preprocessing (same as before)
data['dteday'] = pd.to_datetime(data['dteday'])
max_date = data['dteday'].max()
data['Recency'] = (max_date - data['dteday']).dt.days

# Frequency and Monetary calculations
frequency = data.groupby('instant')['cnt'].sum().reset_index()
frequency.rename(columns={'cnt': 'Frequency'}, inplace=True)

monetary = frequency.copy()
monetary['Monetary'] = frequency['Frequency']

rfm_data = frequency.merge(data[['instant', 'Recency']], on='instant', how='left').drop_duplicates()
rfm_data['Monetary'] = rfm_data['Frequency']

# Map the 'season' values to their corresponding names
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
data['season'] = data['season'].map(season_mapping)

# Define the correct season order
season_order = ['Spring', 'Summer', 'Fall', 'Winter']

# Group the data by 'season' and calculate the total 'cnt' for each season
season_cnt = data.groupby('season')['cnt'].sum().reindex(season_order)

# Streamlit Dashboard

# Project information
st.markdown("## Proyek Analisis Data: Bike Sharing Dataset")
st.markdown("### Nama: Muhamad Rafli Gunawan")
st.markdown("### Email: m010b4ky2655@bangkit.academy")
st.markdown("### ID Dicoding: rafli_gunawan20")

# Questions

st.markdown("### Pertanyaan 1 : How is temperature affecting bike sharing business?")
st.markdown("""
- The most optimal temperature for the bike sharing business is 25°C. The closer the temperature is to 25°C, the higher the count of bike rentals.
""")

st.markdown("### Pertanyaan 2 : What is the most profitable season for the bike sharing business?")
st.markdown("""
- The most profitable season for the bike sharing business is fall, followed by summer, winter, and spring in corresponding order from highest bike rental count to lowest.
""")

# Visualizations (Placed before the RFM section)

st.title('Bike Sharing Data Analysis Dashboard')

# Histogram for Bike Rental Count Distribution
st.subheader('Frequency Distribution')
plt.figure(figsize=(10, 6))
plt.hist(data['cnt'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Bike Rental Count')
plt.xlabel('Bike Rental Count')
plt.ylabel('Frequency')
st.pyplot(plt)

# Scatter plot: Temperature vs Bike Rentals
st.subheader('Effect of Temperature on Bike Rental Count')

# Convert normalized temperature to actual temperature in Celsius
data['temp_celsius'] = data['temp'] * 41

# Plot a scatter plot to show the relationship between actual temperature and cnt
plt.figure(figsize=(10, 6))
plt.scatter(data['temp_celsius'], data['cnt'], color='skyblue', alpha=0.6)
plt.xlabel('Temperature (°C)')
plt.ylabel('Count of Bike Rental')
plt.title('Effect of Temperature on Count of Bike Rental')
st.pyplot(plt)

# Add Insight after Temperature Visualization
st.markdown("### Insight:")
st.markdown("""
- The most optimal temperature for the bike sharing business is 25°C. The closer the temperature is to 25°C, the higher the count of bike rentals.
""")

# Bar Chart for Total Count by Season
st.subheader('Total Count by Season')

# Plot a bar chart for total counts by season
plt.figure(figsize=(10, 6))
season_cnt.plot(kind='bar', color='skyblue')
plt.xlabel('Season')
plt.ylabel('Total Count')
plt.title('Total Count by Season')
plt.xticks(rotation=0)
st.pyplot(plt)

# Add Insight after Season Visualization
st.markdown("### Insight:")
st.markdown("""
- The most profitable season for the bike sharing business is fall, followed by summer, winter, and spring in corresponding order from highest bike rental count to lowest.
""")

# RFM Analysis (Displayed Last)

st.title('RFM Analysis Dashboard')

# Display RFM Data
st.subheader('RFM Metrics')
st.write(rfm_data[['instant', 'Recency', 'Frequency', 'Monetary']])

# Summary Statistics for RFM Data
st.subheader('RFM Summary Statistics')
st.write(rfm_data.describe())

# Monetary Distribution Chart for RFM
st.subheader('Monetary Distribution')
st.bar_chart(rfm_data['Monetary'])

# Final display of the RFM Data
st.subheader('RFM Data Table')
st.write(rfm_data[['instant', 'Recency', 'Frequency', 'Monetary']])
