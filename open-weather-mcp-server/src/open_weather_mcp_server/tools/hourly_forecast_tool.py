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


# Function to get the hourly forecast
async def get_hourly_forecast(
    lat: float, lon: float, units: Optional[str] = "standard", cnt: int = 12    
) -> Dict[str, Any]:
    """Get the hourly weather forecast for a given location.

    Args:
        lat (float): Latitude, decimal (-90; 90)
        lon (float): Longitude, decimal (-180; 180)
        units (Optional[str]): Units of measurement (standard, metric, imperial). Defaults to standard.
        cnt (int): Number of hours to return. Defaults to 12.

    Raises:
        ValueError: Missing required argument 'lat'
        ValueError: Missing required argument 'lon'
        ValueError: Latitude must be between -90 and 90
        ValueError: Longitude must be between -180 and 180
        Exception: Failed to get hourly forecast

    Returns:
        Dict[str, Any]: The hourly forecast data.
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

    # If the cnt is not between 1 and 40
    if cnt < 1 or cnt > 40:
        # Raise an error
        raise ValueError("Count must be between 1 and 40")

    try:
        # Initialize the HTTP client
        async with httpx.AsyncClient() as client:
            # Make the request to the OpenWeather API
            response = await client.get(
                "https://pro.openweathermap.org/data/2.5/forecast/hourly",
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

            # Return the hourly forecast data
            return response.json()

    # Handle the HTTPStatusError exception
    except httpx.HTTPStatusError as e:
        # Raise an error
        raise Exception(f"Failed to get hourly forecast: {e}")

    # Handle any other exception
    except Exception as e:
        # Raise an error
        raise Exception(f"Failed to get hourly forecast: {e}")


# Exports
__all__ = ["get_hourly_forecast"]
