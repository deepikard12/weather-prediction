
import streamlit as st
import requests
import pandas as pd
import joblib
import os
# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Real-Time Weather Rain Prediction",
    page_icon="🌦️",
    layout="wide"
)

# -----------------------------
# Load ML Model
# -----------------------------

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "weather_rain_prediction_model.pkl"
)

model = joblib.load(MODEL_PATH)

# -----------------------------
# Title
# -----------------------------

st.title("🌦️ Real-Time Weather Rain Prediction")

st.write(
    "Enter a location to get real-time weather information "
    "and predict whether it will rain tomorrow."
)

# -----------------------------
# Location Input
# -----------------------------

location = st.text_input(
    "📍 Enter Location",
    placeholder="Example: Coimbatore"
)

# -----------------------------
# Predict Button
# -----------------------------

if st.button("🔮 Get Weather & Predict"):

    if location.strip() == "":
        st.warning("⚠️ Please enter a location.")

    else:

        with st.spinner("Fetching real-time weather..."):

            try:

                # =============================
                # 1. Geocoding
                # =============================

                geo_url = "https://geocoding-api.open-meteo.com/v1/search"

                geo_params = {
                    "name": location,
                    "count": 1,
                    "language": "en",
                    "format": "json"
                }

                geo_response = requests.get(
                    geo_url,
                    params=geo_params,
                    timeout=10
                )

                geo_data = geo_response.json()

                if "results" not in geo_data:
                    st.error("❌ Location not found. Try another city.")
                    st.stop()

                latitude = geo_data["results"][0]["latitude"]
                longitude = geo_data["results"][0]["longitude"]
                city_name = geo_data["results"][0]["name"]
                country = geo_data["results"][0].get("country", "")

                # =============================
                # 2. Weather API
                # =============================

                weather_url = "https://api.open-meteo.com/v1/forecast"

                weather_params = {
                    "latitude": latitude,
                    "longitude": longitude,

                    "current": [
                        "temperature_2m",
                        "relative_humidity_2m",
                        "pressure_msl",
                        "wind_speed_10m",
                        "wind_gusts_10m",
                        "precipitation",
                        "cloud_cover"
                    ],

                    "hourly": [
                        "temperature_2m",
                        "relative_humidity_2m",
                        "pressure_msl",
                        "wind_gusts_10m"
                    ],

                    "daily": [
                        "temperature_2m_min",
                        "temperature_2m_max",
                        "precipitation_sum"
                    ],

                    "timezone": "auto",
                    "forecast_days": 2
                }

                weather_response = requests.get(
                    weather_url,
                    params=weather_params,
                    timeout=10
                )

                weather = weather_response.json()

                # =============================
                # 3. Current Weather
                # =============================

                current = weather["current"]

                temperature = current["temperature_2m"]
                humidity = current["relative_humidity_2m"]
                pressure = current["pressure_msl"]
                wind_speed = current["wind_speed_10m"]
                wind_gust = current["wind_gusts_10m"]
                rainfall = current["precipitation"]
                cloud_cover = current["cloud_cover"]

                # =============================
                # 4. Daily Weather
                # =============================

                min_temp = weather["daily"]["temperature_2m_min"][0]
                max_temp = weather["daily"]["temperature_2m_max"][0]
                daily_rainfall = weather["daily"]["precipitation_sum"][0]

                # =============================
                # 5. Find 3 PM values
                # =============================

                hourly_df = pd.DataFrame({
                    "time": weather["hourly"]["time"],
                    "temperature": weather["hourly"]["temperature_2m"],
                    "humidity": weather["hourly"]["relative_humidity_2m"],
                    "pressure": weather["hourly"]["pressure_msl"],
                    "wind_gust": weather["hourly"]["wind_gusts_10m"]
                })

                hourly_df["time"] = pd.to_datetime(
                    hourly_df["time"]
                )

                three_pm = hourly_df[
                    hourly_df["time"].dt.hour == 15
                ]

                if len(three_pm) > 0:

                    row = three_pm.iloc[0]

                    temp_3pm = row["temperature"]
                    humidity_3pm = row["humidity"]
                    pressure_3pm = row["pressure"]
                    wind_gust_speed = row["wind_gust"]

                else:

                    temp_3pm = temperature
                    humidity_3pm = humidity
                    pressure_3pm = pressure
                    wind_gust_speed = wind_gust

                # =============================
                # 6. ML Input
                # =============================

                input_data = pd.DataFrame([{
                    "MinTemp": min_temp,
                    "MaxTemp": max_temp,
                    "Rainfall": daily_rainfall,
                    "Humidity3pm": humidity_3pm,
                    "Pressure3pm": pressure_3pm,
                    "Temp3pm": temp_3pm,
                    "WindGustSpeed": wind_gust_speed
                }])

                # =============================
                # 7. Prediction
                # =============================

                prediction = model.predict(input_data)[0]

                # =============================
                # 8. Display Location
                # =============================

                st.success(
                    f"📍 {city_name}, {country}"
                )

                st.subheader("🌦️ Current Weather")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "🌡️ Temperature",
                        f"{temperature} °C"
                    )

                with col2:
                    st.metric(
                        "💧 Humidity",
                        f"{humidity} %"
                    )

                with col3:
                    st.metric(
                        "🌬️ Wind Speed",
                        f"{wind_speed} km/h"
                    )

                with col4:
                    st.metric(
                        "☁️ Cloud Cover",
                        f"{cloud_cover} %"
                    )

                col5, col6, col7, col8 = st.columns(4)

                with col5:
                    st.metric(
                        "🌧️ Rainfall",
                        f"{rainfall} mm"
                    )

                with col6:
                    st.metric(
                        "📊 Pressure",
                        f"{pressure} hPa"
                    )

                with col7:
                    st.metric(
                        "💨 Wind Gust",
                        f"{wind_gust} km/h"
                    )

                with col8:
                    st.metric(
                        "🌡️ Max Temperature",
                        f"{max_temp} °C"
                    )

                # =============================
                # 9. Prediction Result
                # =============================

                st.subheader("🔮 Rain Tomorrow Prediction")

                if prediction == 1:

                    st.error(
                        "🌧️ YES — Rain is predicted tomorrow!"
                    )

                else:

                    st.success(
                        "☀️ NO — Rain is not predicted tomorrow."
                    )

            except Exception as e:

                st.error(
                    f"❌ Something went wrong: {e}"
                )
