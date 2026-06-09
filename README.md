# Streamlit Weather App

A Python-based web application built with Streamlit that fetches and displays current weather data using the OpenWeatherMap API.

## Project Overview

This project demonstrates core concepts in web development and API integration:
- **Frontend**: Streamlit (Python-based UI framework)
- **Backend**: Python with requests library for API calls
- **API**: OpenWeatherMap Current Weather API
- **Configuration**: Environment variables via `.env` file
- **Data Format**: JSON response parsing

## Learning Objectives

As a CSE student, this project covers:
- RESTful API consumption and HTTP requests
- JSON data parsing and manipulation
- Environment-based configuration management
- Exception handling and error management
- UI development with Streamlit
- Python best practices (type hints, error handling)

## Project Structure

```
MyFirstWebApp/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env                   # API key (keep secret, not in git)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- OpenWeatherMap API key (free tier available)

## Setup Instructions

### 1. Clone/Download the Project
```bash
cd MyFirstWebApp
```

### 2. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies:**
- `streamlit`: Web framework for data apps
- `requests`: HTTP library for API calls
- `python-dotenv`: Environment variable management

### 4. Get OpenWeatherMap API Key
1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Create an API key in your account dashboard
4. Wait 10 minutes for activation

### 5. Configure Environment Variables

Create a `.env` file in the project root:
```
OPENWEATHER_API_KEY=your_api_key_here
```

**Important**: Never commit `.env` to git. It's already in `.gitignore`.

### 6. Run the Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Features

- **City Search**: Enter any city name to fetch weather
- **Unit Selection**: Toggle between Celsius and Fahrenheit
- **Weather Display**:
  - Current weather condition with icon
  - Temperature and "feels like" temperature
  - Humidity, pressure, wind speed, and cloud coverage
  - Sunrise and sunset times
  - Data timestamp
- **Error Handling**: Graceful error messages for invalid cities or API issues
- **API Key Management**: Secure loading from `.env` file

## Code Architecture

### Main Components

**`format_timestamp(timestamp, tz_offset)`**
- Converts Unix timestamps to readable date-time format
- Uses timezone-aware datetime objects (Python 3.9+ recommended)

**`get_api_error_message(response)`**
- Extracts error messages from API responses
- Handles JSON parsing errors gracefully

**`fetch_current_weather(city, api_key, units)`**
- Makes HTTP GET request to OpenWeatherMap API
- Returns parsed JSON response
- Raises HTTPError on API failures

**`main()`**
- Streamlit UI layout and logic
- Input handling (city name, unit selection)
- Weather data display and formatting

## API Documentation

### Endpoint Used
```
GET https://api.openweathermap.org/data/2.5/weather
```

### Required Parameters
- `q`: City name
- `appid`: API key
- `units`: metric or imperial
- `lang`: en (English)

### Sample Request
```
https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY&units=metric&lang=en
```

### Response Structure (JSON)
```json
{
  "name": "London",
  "sys": {"country": "GB", "sunrise": 1654..., "sunset": 1654...},
  "main": {"temp": 20.5, "feels_like": 19.2, "humidity": 65, "pressure": 1013},
  "weather": [{"main": "Clouds", "description": "overcast clouds", "icon": "04d"}],
  "wind": {"speed": 3.5},
  "clouds": {"all": 90},
  "dt": 1654...
}
```

## Troubleshooting

### Common Issues

**Error: `OPENWEATHER_API_KEY not found`**
- Ensure `.env` file exists in the project root
- Verify the key is formatted correctly
- Restart Streamlit after creating/modifying `.env`

**Error: `401 Unauthorized`**
- API key is invalid or not activated yet
- New keys take ~10 minutes to activate
- Double-check your key at https://openweathermap.org/api_keys

**Error: `404 City not found`**
- Enter a valid city name (e.g., London, not "Lndon")
- Some small towns may not be in the database

**Error: `Network error`**
- Check your internet connection
- Verify OpenWeatherMap API is not down

### Debugging Tips

1. **Enable verbose logging** (for development):
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Test API directly**:
   ```bash
   curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY&units=metric"
   ```

3. **Check environment variables**:
   ```python
   import os
   print(os.getenv("OPENWEATHER_API_KEY"))
   ```

## Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Deploy from repo
4. Set secrets in Streamlit Cloud dashboard (not `.env`)

### Docker (Advanced)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

## Further Learning

- **Streamlit Documentation**: https://docs.streamlit.io
- **Requests Library**: https://docs.python-requests.org
- **OpenWeatherMap API**: https://openweathermap.org/api
- **Python Typing**: https://docs.python.org/3/library/typing.html
- **Environment Variables**: https://12factor.net/config

## Security Considerations

1. **Never commit `.env` file** to version control
2. **Rotate API keys** periodically
3. **Use rate limiting** for production deployments
4. **Validate user input** (city names) before API calls
5. **Cache API responses** to reduce quota usage

## Performance Optimization Ideas

- Add caching with `@st.cache_data` decorator
- Implement async requests for multiple cities
- Add pagination for extended forecasts
- Store historical data in a database

## Contributors

Built as a learning project for CSE students.

## License

Open source - feel free to modify and learn from this code.
