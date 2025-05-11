# Standard library imports
import os
from typing import Any, Dict, List, Optional, Union

# Third party imports
from dotenv import load_dotenv
from serpapi import GoogleSearch

# Load environment variables
load_dotenv()

# Set constants
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


# Function to get hotels
async def get_hotels(
    query: str,
    check_in_date: str,
    check_out_date: str,
    adults: int = 2,
    children: Optional[int] = 0,
    children_ages: Optional[str] = None,
    currency: str = "USD",
    sort_by: Optional[int] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    rating: Optional[int] = None,
    hotel_class: Optional[Union[int, str]] = None,
    free_cancellation: Optional[bool] = None,
    vacation_rentals: Optional[bool] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Get hotel information from SerpApi.

    Args:
        query (str): Search query for hotels (e.g., "Bali Resorts")
        check_in_date (str): Check-in date in YYYY-MM-DD format
        check_out_date (str): Check-out date in YYYY-MM-DD format
        adults (int): Number of adults. Defaults to 2.
        children (Optional[int]): Number of children. Defaults to 0.
        children_ages (Optional[str]): Ages of children, comma-separated (e.g., "5,8,10")
        currency (str): Currency code. Defaults to "USD".
        sort_by (Optional[int]): Sorting order. 3 = Lowest price, 8 = Highest rating, 13 = Most reviewed
        min_price (Optional[int]): Lower bound of price range
        max_price (Optional[int]): Upper bound of price range
        rating (Optional[int]): Filter by rating. 7 = 3.5+, 8 = 4.0+, 9 = 4.5+
        hotel_class (Optional[Union[int, str]]): Filter by hotel class. Single (e.g., 4) or multiple (e.g., "2,3,4")
        free_cancellation (Optional[bool]): Show only results with free cancellation
        vacation_rentals (Optional[bool]): Search for vacation rentals instead of hotels
        bedrooms (Optional[int]): Minimum number of bedrooms (vacation rentals only)
        bathrooms (Optional[int]): Minimum number of bathrooms (vacation rentals only)

    Returns:
        List[Dict[str, Any]]: A list of hotel properties matching the criteria
    """

    # Prepare required parameters
    params = {
        "engine": "google_hotels",
        "q": query,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": adults,
        "currency": currency,
        "api_key": SERPAPI_API_KEY,
    }

    # Define optional parameters with their conditions
    optional_params = {
        "children": children if children > 0 else None,
        "children_ages": children_ages,
        "sort_by": {
            "lowest_price": 3,
            "highest_rating": 8,
            "most_reviews": 13,
        }.get(sort_by, 3),
        "min_price": min_price,
        "max_price": max_price,
        "rating": {
            "3.5+": 7,
            "4.0+": 8,
            "4.5+": 9,
        }.get(rating, None),
        "hotel_class": {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
        }.get(hotel_class, None),
        "free_cancellation": free_cancellation,
        "vacation_rentals": vacation_rentals,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
    }

    # Add non-None optional parameters to the params dictionary
    params.update({k: v for k, v in optional_params.items() if v is not None})

    # Get hotels
    results = GoogleSearch(params).get_dict()["properties"]

    # Return hotels
    return results


# Exports
__all__ = ["get_hotels"]
