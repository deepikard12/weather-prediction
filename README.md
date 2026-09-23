# 🌦️ Real-Time Weather Rain Prediction

A Machine Learning based web application that provides real-time weather information for a selected location and predicts whether it will rain tomorrow.

## 🚀 Live Project

The application is deployed using Streamlit Community Cloud.

👉 Add your Streamlit app link here

## 📌 Project Overview

Weather conditions can change frequently, and rainfall prediction can be useful for planning daily activities.

This project combines:

- Machine Learning
- Real-time Weather API
- Python
- Streamlit

The application allows users to search and select a city, fetches its current weather information using the Open-Meteo API, and uses a trained Machine Learning model to predict whether rain is expected tomorrow.

## ✨ Features

- 📍 Search and select a city
- 🌡️ Real-time temperature
- 💧 Real-time humidity
- 🌬️ Wind speed
- 💨 Wind gust
- ☁️ Cloud cover
- 🌧️ Rainfall information
- 📊 Atmospheric pressure
- 🔮 Rain tomorrow prediction
- 🌐 Real-time weather data using Open-Meteo API
- 💻 Interactive Streamlit dashboard

## 🧠 Machine Learning

The model was trained using the WeatherAUS dataset.

### Input Features

The model uses the following weather features:

- MinTemp
- MaxTemp
- Rainfall
- Humidity3pm
- Pressure3pm
- Temp3pm
- WindGustSpeed

### Target

`RainTomorrow`

The target has two classes:

- `Yes` → Rain predicted tomorrow
- `No` → Rain not predicted tomorrow

## 🌳 Machine Learning Model

A Random Forest Classifier was used for rainfall prediction.

The model was trained using:

- Random Forest
- 100 estimators
- Maximum depth of 12
- Class balancing
- Train-test split with stratification

## 📊 Model Performance

The model was evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score

The model achieved approximately:

**Accuracy: 82.67%**

The project focuses not only on accuracy but also on identifying rainy days using precision, recall, and F1 score.

## 🌐 Real-Time Weather API

The application uses the **Open-Meteo API** to retrieve real-time weather information.

The application:

1. Takes the selected city
2. Finds its geographical coordinates
3. Fetches current weather data
4. Fetches daily and hourly weather information
5. Maps the required values to the Machine Learning model features
6. Generates the rain prediction

## 🔄 Project Workflow

```text
User selects location
        ↓
Open-Meteo Geocoding API
        ↓
Latitude & Longitude
        ↓
Open-Meteo Weather API
        ↓
Real-Time Weather Data
        ↓
Feature Preparation
        ↓
Random Forest Model
        ↓
Rain Tomorrow Prediction
        ↓
Streamlit Dashboard
