# Standard library imports
import os
from typing import Any, Dict, List

# Third party imports
from dotenv import load_dotenv
from serpapi import GoogleSearch

# Load environment variables
load_dotenv()

# Set constants
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


# Function to get shopping results
async def get_shopping(
    query: str,
) -> List[Dict[str, Any]]:
    """
    Get shopping results from SerpApi's Google Shopping engine.

    Args:
        query (str): Search query for products (e.g., "Macbook M3" or "Nike shoes")

    Returns:
        List[Dict[str, Any]]: A list of shopping results matching the query
    """

    # Prepare parameters
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SERPAPI_API_KEY,
    }

    # Get shopping results
    results = GoogleSearch(params).get_dict()["shopping_results"]

    # Return shopping results
    return results


# Exports
__all__ = ["get_shopping"]
