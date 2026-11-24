import requests
from pydantic import BaseModel, Field


def get_temperature(city: str) -> str:
    """Get the current weather in a given city using the free Open-Meteo API."""
    try:
        # Step 1: Convert city name to latitude & longitude
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_res = requests.get(
            geo_url,
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        geo_res.raise_for_status()
        geo_data = geo_res.json()

        if not geo_data.get("results"):
            return f"Could not find location data for '{city}'."

        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        resolved_name = f"{location['name']}, {location.get('country', '')}".strip(", ")

        # Step 2: Fetch current weather using the coordinates
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_res = requests.get(
            weather_url,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
                "temperature_unit": "celsius",
            },
            timeout=10,
        )
        weather_res.raise_for_status()
        current = weather_res.json().get("current", {})

        temp = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        wind = current.get("wind_speed_10m")

        return (
            f"Current weather in {resolved_name}: "
            f"{temp}°C, Humidity: {humidity}%, Wind Speed: {wind} km/h."
        )

    except requests.RequestException as e:
        return f"Error fetching weather data: {e}"


# Pydantic argument schema
class GetTemperatureArgs(BaseModel):
    city: str = Field(..., description="The city to get the current weather for.")


# JSON schema expected by Ollama
get_temperature_schema = {
    "type": "function",
    "function": {
        "name": "get_temperature",
        "description": "Get the current temperature and weather conditions in a given city.",
        "parameters": GetTemperatureArgs.model_json_schema(),
    },
}

TOOL_SCHEMAS = [get_temperature_schema]

TOOL_REGISTRY = {
    "get_temperature": get_temperature,
}