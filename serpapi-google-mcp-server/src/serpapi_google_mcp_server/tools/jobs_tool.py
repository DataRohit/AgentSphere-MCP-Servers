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


# Function to get jobs
async def get_jobs(
    query: str,
    location: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Get job listings from SerpApi's Google Jobs engine.

    Args:
        query (str): Job search query (e.g., "barista new york" or "software engineer")
        location (Optional[str]): Location for job search (e.g., "New York, NY")

    Returns:
        List[Dict[str, Any]]: A list of job listings matching the criteria
    """

    # Prepare parameters
    params = {
        "engine": "google_jobs",
        "q": query,
        "api_key": SERPAPI_API_KEY,
    }

    # If location is provided
    if location:
        # Add location to parameters
        params["location"] = location

    # Get jobs
    results = GoogleSearch(params).get_dict()["jobs_results"]

    # Return jobs
    return results


# Exports
__all__ = ["get_jobs"]
