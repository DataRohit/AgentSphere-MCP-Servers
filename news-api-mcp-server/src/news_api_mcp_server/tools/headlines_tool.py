# Imports
import os
from typing import Any, Dict, List

# Third party imports
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# Function to get the headlines
async def get_headlines(country: str, page_size: int = 5) -> List[Dict[str, Any]]:
    """Get the latest headlines for a given country.

    Args:
        country (str): The country code (2 letters) to get headlines for.
        page_size (int, optional): Number of results to return. Defaults to 5.

    Raises:
        ValueError: Missing required argument 'country'
        ValueError: Country code must be two letters
        ValueError: Page size must be between 1 and 25
        Exception: Failed to get headlines

    Returns:
        List[Dict[str, Any]]: The list of headlines.
    """

    # If the country is not provided
    if not country:
        # Raise an error
        raise ValueError("Missing required argument 'country'")

    # If the country code is not two letters
    if len(country) != 2:
        # Raise an error
        raise ValueError("Country code must be two letters")

    # If the page size is not between 1 and 25
    if page_size < 1 or page_size > 25:
        # Raise an error
        raise ValueError("Page size must be between 1 and 25")

    try:
        # Initialize the HTTP client
        async with httpx.AsyncClient() as client:
            # Make the request to the News API
            response = await client.get(
                "https://newsapi.org/v2/top-headlines",
                headers={"X-Api-Key": NEWS_API_KEY},
                params={"country": country.lower(), "pageSize": page_size, "language": "en"},
            )

            # Raise an exception if the response status code is not successful
            response.raise_for_status()

            # Return the list of headlines
            return response.json()["articles"]

    # Handle the HTTPStatusError exception
    except httpx.HTTPStatusError as e:
        # Raise an error
        raise Exception(f"Failed to get headlines: {e.response.json()['message']}")

    # Handle any other exception
    except Exception as e:
        # Raise an error
        raise Exception(f"Failed to get headlines: {e}")


# Exports
__all__ = ["get_headlines"]
