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


# Function to get events
async def get_events(query: str, page: Optional[int] = 1) -> List[Dict[str, Any]]:
    """
    Get events from SerpApi.

    Args:
        query (str): The query to search for
        page (Optional[int]): The page number to return. Defaults to 1.

    Returns:
        List[Dict[str, Any]]: A list of events
    """

    # Prepare parameters
    params = {
        "engine": "google_events",
        "q": query,
        "start": (page - 1) * 10,
        "api_key": SERPAPI_API_KEY,
    }

    # Get events
    results = GoogleSearch(params).get_dict()["events_results"]

    # Return events
    return results


# Exports
__all__ = ["get_events"]
