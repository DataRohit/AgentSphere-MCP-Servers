# Standard library imports
import os
from typing import Any, Dict

# Third party imports
from dotenv import load_dotenv
from serpapi import GoogleSearch

# Load environment variables
load_dotenv()

# Set constants
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


# Function to get finance data
async def get_finance_data(query: str) -> Dict[str, Any]:
    """
    Get finance data from SerpApi.

    Args:
        query (str): The finance query to search for

    Returns:
        Dict[str, Any]: Finance summary data
    """

    # Prepare parameters
    params = {
        "engine": "google_finance",
        "q": query,
        "api_key": SERPAPI_API_KEY,
    }

    # Get finance data
    results = GoogleSearch(params).get_dict()["summary"]

    # Return finance data
    return results


# Exports
__all__ = ["get_finance_data"]
