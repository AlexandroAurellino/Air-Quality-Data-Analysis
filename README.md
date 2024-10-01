# Air Quality Data Analysis Dashboard 🌍✨

This dashboard provides insights into air quality measurements, including PM2.5, PM10, and weather-related factors across various monitoring stations. It includes interactive charts and a map that visualizes air pollution levels at different stations.

## Features
- 📊 Visualize trends of PM2.5 and PM10 levels over time.
- 📅 Filter data by station and time range.
- 📍 View stations' geographical locations with pollution levels on an interactive map.
- 🔍 Explore the correlation between pollutants and weather factors.

## Setup Environment - Anaconda
1. Create and activate the virtual environment:
    ```bash
    conda create --name air-quality-dashboard python=3.9
    conda activate air-quality-dashboard
    ```
2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Setup Environment - Shell/Terminal
1. Create a project directory and navigate to it:
    ```bash
    mkdir air_quality_dashboard
    cd air_quality_dashboard
    ```
2. Install the dependencies using `pipenv`:
    ```bash
    pipenv install
    pipenv shell
    pip install -r requirements.txt
    ```

## Run the Streamlit App
To start the dashboard locally:
```bash
streamlit run dashboard.py
