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


# Function to get flights
async def get_flights(
    departure_id: str,
    arrival_id: str,
    outbound_date: str,
    return_date: Optional[str] = None,
    currency: str = "USD",
    flight_type: Optional[int] = 1,
    travel_class: Optional[int] = 1,
    adults: Optional[int] = 1,
    children: Optional[int] = 0,
    infants_in_seat: Optional[int] = 0,
    infants_on_lap: Optional[int] = 0,
    sort_by: Optional[int] = 1,
    stops: Optional[int] = 0,
    bags: Optional[int] = 0,
    max_price: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Get flight information from SerpApi.

    Args:
        departure_id (str): Departure airport ID (e.g., "CDG,ORY" for Paris airports)
        arrival_id (str): Arrival airport ID (e.g., "LAX" for Los Angeles)
        outbound_date (str): Outbound date in YYYY-MM-DD format
        return_date (Optional[str]): Return date in YYYY-MM-DD format. Required for round trips.
        currency (str): Currency code. Defaults to "USD".
        flight_type (Optional[int]): Type of flight. 1 = Round trip (default), 2 = One way
        travel_class (Optional[int]): Travel class. 1 = Economy (default), 2 = Premium economy, 3 = Business, 4 = First
        adults (Optional[int]): Number of adults. Defaults to 1.
        children (Optional[int]): Number of children. Defaults to 0.
        infants_in_seat (Optional[int]): Number of infants in seat. Defaults to 0.
        infants_on_lap (Optional[int]): Number of infants on lap. Defaults to 0.
        sort_by (Optional[int]): Sorting order. 1 = Top flights (default), 2 = Price, 3 = Departure time,
                                 4 = Arrival time, 5 = Duration, 6 = Emissions
        stops (Optional[int]): Number of stops. 0 = Any number of stops (default), 1 = Nonstop only,
                               2 = 1 stop or fewer, 3 = 2 stops or fewer
        bags (Optional[int]): Number of carry-on bags. Defaults to 0.
        max_price (Optional[int]): Maximum ticket price. Default is unlimited.

    Returns:
        List[Dict[str, Any]]: A list of best flights matching the criteria
    """

    # Prepare parameters
    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "currency": currency,
        "api_key": SERPAPI_API_KEY,
        "type": 1 if flight_type == "round_trip" else 2,
        "travel_class": {
            "economy": 1,
            "premium_economy": 2,
            "business": 3,
            "first": 4,
        }.get(travel_class, 1),
        "adults": adults,
    }

    # Define optional parameters with their conditions
    optional_params = {
        "return_date": return_date,
        "children": children if children > 0 else None,
        "infants_in_seat": infants_in_seat if infants_in_seat > 0 else None,
        "infants_on_lap": infants_on_lap if infants_on_lap > 0 else None,
        "sort_by": {
            "top_flights": 1,
            "price": 2,
            "departure_time": 3,
            "arrival_time": 4,
            "duration": 5,
        }.get(sort_by, 1),
        "stops": {
            "any": 0,
            "nonstop": 1,
            "one_stop": 2,
            "two_stops": 3,
        }.get(stops, 0),
        "bags": bags if bags > 0 else None,
        "max_price": max_price,
    }

    # Add non-None optional parameters to the params dictionary
    params.update({k: v for k, v in optional_params.items() if v is not None})

    # Get flights
    results = GoogleSearch(params).get_dict()["best_flights"]

    # Return flights
    return results


# Exports
__all__ = ["get_flights"]
