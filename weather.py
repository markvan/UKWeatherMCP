import sys
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import keys
import json

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
OPENWEATHER_API_BASE = "https://api.openweathermap.org/data/2.5/weather?"
USER_AGENT = "weather-app/1.0"

async def make_weather_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@mcp.tool()
async def get_weather(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    weather_url = f"{OPENWEATHER_API_BASE}lat={latitude}&lon={longitude}&units=metric&appid={keys.OPENWEATHER_API_KEY}"
    weather_data = await make_weather_request(weather_url)

    if not weather_data:
        return "Unable to fetch forecast data for this location."

    # Get the current weather
    weather_dict = await make_weather_request(weather_url)

    if not weather_dict:
        return "Unable to fetch detailed forecast."

    # Safely get the first weather entry
    weather_list = weather_dict.get("weather", [])
    if not weather_list:
        return "No weather information available."

    first_weather = weather_list[0]

    overall = first_weather.get("main", "Unknown")
    detail = first_weather.get("description", "no description")

    weather = overall + " more detail: " + detail
    weather += ' temperature '
    weather += str(weather_data['main']['temp'])
    weather += ' humidity '
    weather += str(weather_data['main']['humidity'])
    weather += ' wind '
    weather += str(weather_data['wind']['speed'])
    weather +=  ' using the weather station at '
    weather += weather_data['name']

    return weather


def main():
    # Initialize and run the server
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
