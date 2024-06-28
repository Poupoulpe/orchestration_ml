import streamlit as st
import requests
import pandas as pd
import time

# Define the API URL
API_URL = "https://weather-api-cv3s3i6o4q-od.a.run.app/predict/"

def fetch_temperature_data():
    """Fetches temperature data from the API."""
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from the API")
        return []

def main():
    st.title('Temperature Predictions for Today')

    # Fetching temperature data from the API
    temperatures = fetch_temperature_data().get('predictions')

    if temperatures:
        # Creating a DataFrame for visualization
        df = pd.DataFrame({
            'Hour': range(len(temperatures)),
            'Temperature': temperatures
        })

        # Displaying the temperature data as a line chart
        st.subheader('Line Chart of Temperatures')
        st.line_chart(df.set_index('Hour'))

        # Adding a bar chart
        st.subheader('Bar Chart of Temperatures')
        st.bar_chart(df.set_index('Hour'))


if __name__ == "__main__":
    main()
