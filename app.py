import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

OPENWEATHER_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"

# Load environment variables from a .env file located next to this script
dotenv_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=dotenv_path)


def format_timestamp(timestamp: int, tz_offset: int = 0) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(timezone(timedelta(seconds=tz_offset))).strftime("%Y-%m-%d %H:%M:%S")


def get_api_error_message(response: requests.Response) -> str:
    try:
        payload = response.json()
        return payload.get("message", response.text)
    except ValueError:
        return response.text


def fetch_current_weather(city: str, api_key: str, units: str) -> dict:
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
        "lang": "en",
    }
    response = requests.get(OPENWEATHER_CURRENT_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def main() -> None:
    st.set_page_config(page_title="Weather App", page_icon="cloud", layout="centered")
    st.title("Weather App")
    st.write("Enter a city name to get the current weather. The API key is loaded from the .env file.")

    api_key = os.getenv("OPENWEATHER_API_KEY")

    city = st.text_input("Enter city name", value="London", help="Type a city name like London, New York, or Tokyo.")
    units = st.radio("Units", ["metric", "imperial"], index=0, format_func=lambda x: "Celsius (C)" if x == "metric" else "Fahrenheit (F)")
    unit_symbol = "C" if units == "metric" else "F"

    if st.button("Get Weather"):
        if not api_key or not api_key.strip():
            st.error("Please enter your OpenWeatherMap API key. You can also set it in .env with OPENWEATHER_API_KEY.")
            return
        if not city.strip():
            st.error("Please enter a city name.")
            return

        try:
            with st.spinner(f"Fetching current weather for {city.strip()}..."):
                current = fetch_current_weather(city.strip(), api_key, units)

            source = "Current Weather API"
            weather = current.get('weather', [{}])[0]
            weather_main = weather.get('main', 'N/A')
            weather_desc = weather.get('description', '').title()
            icon_code = weather.get('icon')
            temp = current.get('main', {}).get('temp', 'N/A')
            feels_like = current.get('main', {}).get('feels_like', 'N/A')
            humidity = current.get('main', {}).get('humidity', 'N/A')
            wind_speed = current.get('wind', {}).get('speed', 'N/A')
            pressure = current.get('main', {}).get('pressure', 'N/A')
            clouds = current.get('clouds', {}).get('all', 'N/A')
            sunrise = current.get('sys', {}).get('sunrise', 0)
            sunset = current.get('sys', {}).get('sunset', 0)
            dt = current.get('dt', 0)
            tz_offset = current.get('timezone', 0)

            st.subheader(f"Current weather in {current.get('name', city.strip())}, {current.get('sys', {}).get('country', '')}")
            st.caption(f"Source: {source}")

            if icon_code:
                icon_url = f"https://openweathermap.org/img/wn/{icon_code}@4x.png"
                st.image(icon_url, width=120)

            st.markdown(f"**{weather_main}** - {weather_desc}")

            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{temp} {unit_symbol}")
            col2.metric("Feels like", f"{feels_like} {unit_symbol}")
            col3.metric("Humidity", f"{humidity} %")

            col4, col5, col6 = st.columns(3)
            col4.metric("Wind speed", f"{wind_speed} {'m/s' if units == 'metric' else 'mph'}")
            col5.metric("Pressure", f"{pressure} hPa")
            col6.metric("Clouds", f"{clouds} %")

            st.markdown("---")
            sun_col1, sun_col2, sun_col3 = st.columns(3)
            sun_col1.markdown(f"☀️ **Sunrise**  \n{format_timestamp(sunrise, tz_offset)}")
            sun_col2.markdown(f"🌇 **Sunset**  \n{format_timestamp(sunset, tz_offset)}")
            sun_col3.markdown(f"⏱️ **Data time**  \n{format_timestamp(dt, tz_offset)}")

        except requests.HTTPError as http_err:
            if http_err.response is not None:
                status_code = http_err.response.status_code
                api_message = get_api_error_message(http_err.response)
                if status_code == 401:
                    st.error("Unauthorized: your OpenWeatherMap API key is invalid or not activated.")
                    st.info(f"OpenWeather response: {api_message}")
                elif status_code == 404:
                    st.error("Location or endpoint not found. Please check your request.")
                else:
                    st.error(f"Failed to fetch weather data ({status_code}): {api_message}")
            else:
                st.error(f"Failed to fetch weather data: {http_err}")
        except ValueError as err:
            st.error(str(err))
        except requests.RequestException as err:
            st.error(f"Network error: {err}")
        except KeyError:
            st.error("Unexpected response structure from the weather service.")


if __name__ == "__main__":
    main()
