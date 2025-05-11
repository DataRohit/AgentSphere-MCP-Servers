# Imports
import os
from typing import Any, Dict

# Third party imports
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")


# Function to get the current air pollution data
async def get_current_air_pollution(lat: float, lon: float) -> Dict[str, Any]:
    """Get the current air pollution data for a given location.

    Args:
        lat (float): Latitude, decimal (-90; 90)
        lon (float): Longitude, decimal (-180; 180)

    Raises:
        ValueError: Missing required argument 'lat'
        ValueError: Missing required argument 'lon'
        ValueError: Latitude must be between -90 and 90
        ValueError: Longitude must be between -180 and 180
        Exception: Failed to get current air pollution data

    Returns:
        Dict[str, Any]: The current air pollution data.
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

    try:
        # Initialize the HTTP client
        async with httpx.AsyncClient() as client:
            # Make the request to the OpenWeather API
            response = await client.get(
                "http://api.openweathermap.org/data/2.5/air_pollution",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": OPEN_WEATHER_API_KEY,
                },
            )

            # Raise an exception if the response status code is not successful
            response.raise_for_status()

            # Get the response data
            data = response.json()

            # Return the air pollution data
            return data

    # Handle the HTTPStatusError exception
    except httpx.HTTPStatusError as e:
        # Raise an error
        raise Exception(f"Failed to get current air pollution data: {e}")

    # Handle any other exception
    except Exception as e:
        # Raise an error
        raise Exception(f"Failed to get current air pollution data: {e}")


# Exports
__all__ = ["get_current_air_pollution"]
