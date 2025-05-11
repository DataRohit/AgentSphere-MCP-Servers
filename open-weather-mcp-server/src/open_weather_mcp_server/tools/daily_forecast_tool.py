# Imports
import os
from typing import Any, Dict, Optional

# Third party imports
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")


# Function to get the daily forecast
async def get_daily_forecast(
    lat: float, lon: float, units: Optional[str] = "standard", cnt: int = 7
) -> Dict[str, Any]:
    """Get the daily weather forecast for a given location.

    Args:
        lat (float): Latitude, decimal (-90; 90)
        lon (float): Longitude, decimal (-180; 180)
        units (Optional[str]): Units of measurement (standard, metric, imperial). Defaults to standard.
        cnt (int): Number of days to return. Defaults to 7.

    Raises:
        ValueError: Missing required argument 'lat'
        ValueError: Missing required argument 'lon'
        ValueError: Latitude must be between -90 and 90
        ValueError: Longitude must be between -180 and 180
        Exception: Failed to get daily forecast

    Returns:
        Dict[str, Any]: The daily forecast data.
    """

    # If the latitude is not provided
    if lat is None:
        # Raise an error
        raise ValueError("Missing required argument 'lat'")

    # If the longitude is not provided
    if lon is None:
        # Raise an error
        raise ValueError("Missing required argument 'lon'")

    # If the latitude is not between -90 and 90
    if lat < -90 or lat > 90:
        # Raise an error
        raise ValueError("Latitude must be between -90 and 90")

    # If the longitude is not between -180 and 180
    if lon < -180 or lon > 180:
        # Raise an error
        raise ValueError("Longitude must be between -180 and 180")
    
    # If the count is less than 1 or greater than 16
    if cnt < 1 or cnt > 16:
        # Raise an error
        raise ValueError("Count must be between 1 and 16")

    try:
        # Initialize the HTTP client
        async with httpx.AsyncClient() as client:
            # Make the request to the OpenWeather API
            response = await client.get(
                "https://api.openweathermap.org/data/2.5/forecast/daily",
                params={
                    "lat": lat,
                    "lon": lon,
                    "units": units,
                    "cnt": cnt,
                    "appid": OPEN_WEATHER_API_KEY,
                },
            )

            # Raise an exception if the response status code is not successful
            response.raise_for_status()

            # Return the daily forecast data
            return response.json()

    # Handle the HTTPStatusError exception
    except httpx.HTTPStatusError as e:
        # Raise an error
        raise Exception(f"Failed to get daily forecast: {e}")

    # Handle any other exception
    except Exception as e:
        # Raise an error
        raise Exception(f"Failed to get daily forecast: {e}")


# Exports
__all__ = ["get_daily_forecast"]
