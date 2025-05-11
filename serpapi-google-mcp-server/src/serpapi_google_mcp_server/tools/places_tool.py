# Standard library imports
import os
from typing import Any, Dict, List, Optional

# Third party imports
from dotenv import load_dotenv
from serpapi import GoogleSearch

# Load environment variables
load_dotenv()

# Set constants
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


# Function to get places
async def get_places(
    query: str,
    location: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Get local place listings from SerpApi's Google Local engine.

    Args:
        query (str): Search query for places (e.g., "Coffee" or "Restaurants")
        location (Optional[str]): Location for place search (e.g., "Austin, Texas, United States")

    Returns:
        List[Dict[str, Any]]: A list of local place listings matching the criteria
    """

    # Prepare parameters
    params = {
        "engine": "google_local",
        "q": query,
        "api_key": SERPAPI_API_KEY,
    }

    # If location is provided
    if location:
        # Add location to parameters
        params["location"] = location

    # Get places
    results = GoogleSearch(params).get_dict()["local_results"]

    # Return places
    return results


# Exports
__all__ = ["get_places"]
