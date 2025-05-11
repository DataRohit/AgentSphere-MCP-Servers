# Standard library imports
import argparse
import json
from typing import Dict, List, Optional, Union

# Third party imports
import mcp.types as types
import uvicorn
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route

# Import health routes
from serpapi_google_mcp_server.health import health_routes
from serpapi_google_mcp_server.tools import (
    get_events,
    get_finance_data,
    get_flights,
    get_hotels,
    get_jobs,
    get_places,
    get_shopping,
)

# Local imports
from serpapi_google_mcp_server.utils.logger import get_logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = get_logger(__name__)


# SerpAPI Google MCP Server
class SerpAPIGoogleMCPServer:
    # Constructor
    def __init__(self):
        """Initialize the SerpAPI Google MCP Server."""

        # Initialize the server
        self.server = Server("serpapi-google-mcp-server")

        # Register handlers
        self._register_handlers()

    # Method to register handlers
    def _register_handlers(self):
        """Register the handlers for the Weather MCP Server."""

        # Tools handlers
        self.server.list_tools()(self.handle_list_tools)
        self.server.call_tool()(self.handle_call_tool)

    # Method to handle list tools
    async def handle_list_tools(self) -> List[types.Tool]:
        """Handle the list tools request.

        Returns:
            List[types.Tool]: The list of tools.
        """

        # Return the list of tools
        return [
            types.Tool(
                name="get-events",
                description="Get events from SerpApi",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Query to search for",
                        },
                        "page": {
                            "type": "number",
                            "description": "Page number to return",
                        },
                    },
                    "required": ["query", "page"],
                },
            ),
            types.Tool(
                name="get-finance-data",
                description="Get finance data from SerpApi",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Query to search for",
                        },
                    },
                    "required": ["query"],
                },
            ),
            types.Tool(
                name="get-flights",
                description="Get flights from SerpApi",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "departure_id": {
                            "type": "string",
                            "description": "Departure ID",
                        },
                        "arrival_id": {
                            "type": "string",
                            "description": "Arrival ID",
                        },
                        "outbound_date": {
                            "type": "string",
                            "description": "Outbound date YYYY-MM-DD",
                        },
                        "currency": {
                            "type": "string",
                            "description": "Currency",
                        },
                        "flight_type": {
                            "type": "string",
                            "description": "Flight type",
                            "enum": [
                                "round_trip",
                                "one_way",
                            ],
                        },
                        "travel_class": {
                            "type": "string",
                            "description": "Travel class",
                            "enum": [
                                "economy",
                                "premium_economy",
                                "business",
                                "first",
                            ],
                        },
                        "adults": {
                            "type": "number",
                            "description": "Number of adults",
                        },
                        "return_date": {
                            "type": "string",
                            "description": "Return date YYYY-MM-DD",
                        },
                        "children": {
                            "type": "number",
                            "description": "Number of children",
                        },
                        "infants_in_seat": {
                            "type": "number",
                            "description": "Number of infants in seat",
                        },
                        "infants_on_lap": {
                            "type": "number",
                            "description": "Number of infants on lap",
                        },
                        "sort_by": {
                            "type": "string",
                            "description": "Sort by",
                            "enum": [
                                "top_flights",
                                "price",
                                "departure_time",
                                "arrival_time",
                                "duration",
                            ],
                        },
                        "stops": {
                            "type": "string",
                            "description": "Number of stops",
                            "enum": [
                                "any",
                                "nonstop",
                                "one_stop",
                                "two_stops",
                            ],
                        },
                        "bags": {
                            "type": "number",
                            "description": "Number of bags",
                        },
                        "max_price": {
                            "type": "number",
                            "description": "Maximum price",
                        },
                    },
                    "required": [
                        "departure_id",
                        "arrival_id",
                        "outbound_date",
                        "currency",
                        "flight_type",
                        "travel_class",
                        "adults",
                        "return_date",
                        "children",
                        "infants_in_seat",
                        "infants_on_lap",
                        "sort_by",
                        "stops",
                        "bags",
                        "max_price",
                    ],
                },
            ),
            types.Tool(
                name="get-hotels",
                description="Get hotels from SerpApi",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Query to search for",
                        },
                        "check_in_date": {
                            "type": "string",
                            "description": "Check in date YYYY-MM-DD",
                        },
                        "check_out_date": {
                            "type": "string",
                            "description": "Check out date YYYY-MM-DD",
                        },
                        "adults": {
                            "type": "number",
                            "description": "Number of adults",
                        },
                        "currency": {
                            "type": "string",
                            "description": "Currency",
                        },
                        "children": {
                            "type": "number",
                            "description": "Number of children",
                        },
                        "children_ages": {
                            "type": "string",
                            "description": "Children ages",
                        },
                        "sort_by": {
                            "type": "string",
                            "description": "Sort by",
                            "enum": [
                                "lowest_price",
                                "highest_rating",
                                "most_reviews",
                            ],
                        },
                        "min_price": {
                            "type": "number",
                            "description": "Minimum price",
                        },
                        "max_price": {
                            "type": "number",
                            "description": "Maximum price",
                        },
                        "rating": {
                            "type": "string",
                            "description": "Rating",
                            "enum": [
                                "3.5+",
                                "4.0+",
                                "4.5+",
                            ],
                        },
                        "hotel_class": {
                            "type": "string",
                            "description": "Hotel class",
                            "enum": [
                                "2",
                                "3",
                                "4",
                                "5",
                            ],
                        },
                        "free_cancellation": {
                            "type": "boolean",
                            "description": "Free cancellation",
                        },
                        "vacation_rentals": {
                            "type": "boolean",
                            "description": "Vacation rentals",
                        },
                        "bedrooms": {
                            "type": "number",
                            "description": "Number of bedrooms",
                        },
                        "bathrooms": {
                            "type": "number",
                            "description": "Number of bathrooms",
                        },
                    },
                    "required": [
                        "query",
                        "check_in_date",
                        "check_out_date",
                        "adults",
                        "currency",
                        "children",
                        "children_ages",
                        "sort_by",
                        "min_price",
                        "max_price",
                        "rating",
                        "hotel_class",
                        "free_cancellation",
                        "vacation_rentals",
                        "bedrooms",
                        "bathrooms",
                    ],
                },
            ),
            types.Tool(
                name="get-jobs",
                description="Get jobs from SerpApi",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Query to search for",
                        },
                        "location": {
                            "type": "string",
                            "description": "Location",
                        },
                    },
                    "required": ["query", "location"],
                },
            ),
            types.Tool(
                name="get-places",
                description="Get places from SerpApi",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Query to search for",
                        },
                        "location": {
                            "type": "string",
                            "description": "Location",
                        },
                    },
                    "required": ["query", "location"],
                },
            ),
            types.Tool(
                name="get-shopping",
                description="Get shopping from SerpApi",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Query to search for",
                        },
                    },
                    "required": ["query"],
                },
            ),
        ]

    # Method to handle call tool
    async def handle_call_tool(
        self, name: str, arguments: Optional[Dict]
    ) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
        """Handle the call tool request.

        Args:
            name (str): The name of the tool.
            arguments (Optional[Dict]): The arguments for the tool.

        Returns:
            List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]: The list of content items.
        """
        # Default to empty dict if arguments is None
        arguments = arguments or {}

        # Match the name of the tool
        match name:
            # Get events
            case "get-events":
                # Extract required parameters
                query = arguments.get("query")
                if not query:
                    raise ValueError("Query is required for get-events")

                # Extract optional parameters
                page = arguments.get("page", 1)

                # Call the function with extracted parameters
                result = await get_events(query=query, page=page)

                # Return the result
                return [types.TextContent(type="text", text=json.dumps(result))]

            # Get finance data
            case "get-finance-data":
                # Extract required parameters
                query = arguments.get("query")

                # If the query is not provided
                if not query:
                    # Raise an error
                    raise ValueError("Query is required for get-finance-data")

                # Call the function with extracted parameters
                result = await get_finance_data(query=query)

                # Return the result
                return [types.TextContent(type="text", text=json.dumps(result))]

            # Get flights
            case "get-flights":
                # Extract required parameters
                departure_id = arguments.get("departure_id")
                arrival_id = arguments.get("arrival_id")
                outbound_date = arguments.get("outbound_date")
                currency = arguments.get("currency", "USD")

                # If the required parameters are not provided
                if not all([departure_id, arrival_id, outbound_date]):
                    # Raise an error
                    raise ValueError(
                        "departure_id, arrival_id, and outbound_date are required for get-flights"
                    )

                # Extract optional parameters
                return_date = arguments.get("return_date")
                flight_type = arguments.get("flight_type", 1)
                travel_class = arguments.get("travel_class", 1)
                adults = arguments.get("adults", 1)
                children = arguments.get("children", 0)
                infants_in_seat = arguments.get("infants_in_seat", 0)
                infants_on_lap = arguments.get("infants_on_lap", 0)
                sort_by = arguments.get("sort_by", 1)
                stops = arguments.get("stops", 0)
                bags = arguments.get("bags", 0)
                max_price = arguments.get("max_price")

                # Call the function with extracted parameters
                result = await get_flights(
                    departure_id=departure_id,
                    arrival_id=arrival_id,
                    outbound_date=outbound_date,
                    return_date=return_date,
                    currency=currency,
                    flight_type=flight_type,
                    travel_class=travel_class,
                    adults=adults,
                    children=children,
                    infants_in_seat=infants_in_seat,
                    infants_on_lap=infants_on_lap,
                    sort_by=sort_by,
                    stops=stops,
                    bags=bags,
                    max_price=max_price,
                )
                return [types.TextContent(type="text", text=json.dumps(result))]

            # Get hotels
            case "get-hotels":
                # Extract required parameters
                query = arguments.get("query")
                check_in_date = arguments.get("check_in_date")
                check_out_date = arguments.get("check_out_date")
                adults = arguments.get("adults", 2)
                currency = arguments.get("currency", "USD")

                # If the required parameters are not provided
                if not all([query, check_in_date, check_out_date]):
                    # Raise an error
                    raise ValueError(
                        "query, check_in_date, and check_out_date are required for get-hotels"
                    )

                # Extract optional parameters
                children = arguments.get("children", 0)
                children_ages = arguments.get("children_ages")
                sort_by = arguments.get("sort_by")
                min_price = arguments.get("min_price")
                max_price = arguments.get("max_price")
                rating = arguments.get("rating")
                hotel_class = arguments.get("hotel_class")
                free_cancellation = arguments.get("free_cancellation")
                vacation_rentals = arguments.get("vacation_rentals")
                bedrooms = arguments.get("bedrooms")
                bathrooms = arguments.get("bathrooms")

                # Call the function with extracted parameters
                result = await get_hotels(
                    query=query,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    adults=adults,
                    currency=currency,
                    children=children,
                    children_ages=children_ages,
                    sort_by=sort_by,
                    min_price=min_price,
                    max_price=max_price,
                    rating=rating,
                    hotel_class=hotel_class,
                    free_cancellation=free_cancellation,
                    vacation_rentals=vacation_rentals,
                    bedrooms=bedrooms,
                    bathrooms=bathrooms,
                )
                return [types.TextContent(type="text", text=json.dumps(result))]

            # Get jobs
            case "get-jobs":
                # Extract required parameters
                query = arguments.get("query")

                # If the query is not provided
                if not query:
                    # Raise an error
                    raise ValueError("Query is required for get-jobs")

                # Extract optional parameters
                location = arguments.get("location")

                # Call the function with extracted parameters
                result = await get_jobs(query=query, location=location)

                # Return the result
                return [types.TextContent(type="text", text=json.dumps(result))]

            # Get places
            case "get-places":
                # Extract required parameters
                query = arguments.get("query")

                # If the query is not provided
                if not query:
                    # Raise an error
                    raise ValueError("Query is required for get-places")

                # Extract optional parameters
                location = arguments.get("location")

                # Call the function with extracted parameters
                result = await get_places(query=query, location=location)

                # Return the result
                return [types.TextContent(type="text", text=json.dumps(result))]

            # Get shopping
            case "get-shopping":
                # Extract required parameters
                query = arguments.get("query")

                # If the query is not provided
                if not query:
                    # Raise an error
                    raise ValueError("Query is required for get-shopping")

                # Call the function with extracted parameters
                result = await get_shopping(query=query)

                # Return the result
                return [types.TextContent(type="text", text=json.dumps(result))]

            # Default
            case _:
                raise ValueError(f"Tool {name} not found")

    # Method to run the server
    def run(self):
        """Run the server."""

        # Initialize the server
        sse = SseServerTransport("/messages/")

        # Function to handle the SSE
        async def handle_sse(request: Request) -> None:
            async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,
            ) as (read_stream, write_stream):
                # Run the server
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options(),
                )

        # Initialize the parser
        parser = argparse.ArgumentParser(
            description="Run the SerpAPI Google MCP Server"
        )

        # Add arguments
        parser.add_argument(
            "--host", type=str, default="0.0.0.0", help="Host to bind to"
        )
        parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
        parser.add_argument("--debug", type=bool, default=False, help="Debug mode")

        # Parse the arguments
        args = parser.parse_args()

        # Initiailze the Starlette app
        starlette_app = Starlette(
            debug=args.debug,
            routes=[
                # SSE route
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
                # Add health routes
                *health_routes,
            ],
        )

        # Run the server
        uvicorn.run(starlette_app, host=args.host, port=args.port)


# Initialize the SerpAPI Google MCP Server
server = SerpAPIGoogleMCPServer()
