# Standard library imports
import argparse
import json
from typing import Dict, List, Optional, Union

# Third party imports
import mcp.types as types
import uvicorn
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route

# Import health routes
from open_weather_mcp_server.health import health_routes
from open_weather_mcp_server.tools import (
    get_current_air_pollution,
    get_current_weather,
    get_daily_forecast,
    get_forecast_air_pollution,
    get_hourly_forecast,
)

# Local imports
from open_weather_mcp_server.utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


# OpenWeather MCP Server
class OpenWeatherMCPServer:
    # Constructor
    def __init__(self):
        """Initialize the OpenWeather MCP Server."""

        # Initialize the server
        self.server = Server("open-weather-mcp-server")

        # Register handlers
        self._register_handlers()

    # Method to register handlers
    def _register_handlers(self):
        """Register the handlers for the OpenWeather MCP Server."""

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
                name="get-current-weather",
                description="Get the current weather for a given location",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "lat": {
                            "type": "number",
                            "description": "Latitude, decimal (-90; 90)",
                        },
                        "lon": {
                            "type": "number",
                            "description": "Longitude, decimal (-180; 180)",
                        },
                        "units": {
                            "type": "string",
                            "description": "Units of measurement (standard, metric, imperial)",
                            "enum": ["standard", "metric", "imperial"],
                        },
                    },
                    "required": ["lat", "lon", "units"],
                },
            ),
            types.Tool(
                name="get-hourly-forecast",
                description="Get hourly weather forecast for a given location",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "lat": {
                            "type": "number",
                            "description": "Latitude, decimal (-90; 90)",
                        },
                        "lon": {
                            "type": "number",
                            "description": "Longitude, decimal (-180; 180)",
                        },
                        "units": {
                            "type": "string",
                            "description": "Units of measurement (standard, metric, imperial)",
                            "enum": ["standard", "metric", "imperial"],
                        },
                        "cnt": {
                            "type": "number",
                            "description": "Number of hours to return [1-40]",
                        },
                    },
                    "required": ["lat", "lon", "units", "cnt"],
                },
            ),
            types.Tool(
                name="get-daily-forecast",
                description="Get daily weather forecast for a given location",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "lat": {
                            "type": "number",
                            "description": "Latitude, decimal (-90; 90)",
                        },
                        "lon": {
                            "type": "number",
                            "description": "Longitude, decimal (-180; 180)",
                        },
                        "units": {
                            "type": "string",
                            "description": "Units of measurement (standard, metric, imperial)",
                            "enum": ["standard", "metric", "imperial"],
                        },
                        "cnt": {
                            "type": "number",
                            "description": "Number of days to return [1-16]",
                        },
                    },
                    "required": ["lat", "lon", "units", "cnt"],
                },
            ),
            types.Tool(
                name="get-current-air-pollution",
                description="Get current air pollution data for a given location",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "lat": {
                            "type": "number",
                            "description": "Latitude, decimal (-90; 90)",
                        },
                        "lon": {
                            "type": "number",
                            "description": "Longitude, decimal (-180; 180)",
                        },
                    },
                    "required": ["lat", "lon"],
                },
            ),
            types.Tool(
                name="get-forecast-air-pollution",
                description="Get forecast air pollution data for a given location",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "lat": {
                            "type": "number",
                            "description": "Latitude, decimal (-90; 90)",
                        },
                        "lon": {
                            "type": "number",
                            "description": "Longitude, decimal (-180; 180)",
                        },
                    },
                    "required": ["lat", "lon"],
                },
            ),
        ]

    # Method to handle call tool
    async def handle_call_tool(
        self, name: str, arguments: Optional[Dict]
    ) -> Union[types.TextContent, types.ImageContent, types.EmbeddedResource]:
        """Handle the call tool request.

        Args:
            name (str): The name of the tool.
            arguments (Optional[Dict]): The arguments for the tool.

        Returns:
            Union[types.TextContent, types.ImageContent, types.EmbeddedResource]: The content item.
        """

        # Default to empty dict if arguments is None
        arguments = arguments or {}

        # Match the name of the tool
        match name:
            # Get current weather
            case "get-current-weather":
                # Extract required parameters
                lat = arguments.get("lat")
                lon = arguments.get("lon")

                # If the latitude is not provided
                if lat is None:
                    # Raise an error
                    raise ValueError("Latitude is required for get-current-weather")

                # If the longitude is not provided
                if lon is None:
                    # Raise an error
                    raise ValueError("Longitude is required for get-current-weather")

                # Extract optional parameters
                units = arguments.get("units", "standard")

                # Call the function with extracted parameters
                result = await get_current_weather(lat=lat, lon=lon, units=units)

                # Return the result
                return [types.TextContent(type="text", text=json.dumps(result))]

            # Get hourly forecast
            case "get-hourly-forecast":
                # Extract required parameters
                lat = arguments.get("lat")
                lon = arguments.get("lon")

                # If the latitude is not provided
                if lat is None:
                    # Raise an error
                    raise ValueError("Latitude is required for get-hourly-forecast")

                # If the longitude is not provided
                if lon is None:
                    # Raise an error
                    raise ValueError("Longitude is required for get-hourly-forecast")

                # Extract optional parameters
                units = arguments.get("units", "standard")
                cnt = int(arguments.get("cnt", 12))

                # Call the function with extracted parameters
                result = await get_hourly_forecast(
                    lat=lat, lon=lon, units=units, cnt=cnt
                )

                # Return the result
                return [types.TextContent(type="text", text=json.dumps(result))]

            # Get daily forecast
            case "get-daily-forecast":
                # Extract required parameters
                lat = arguments.get("lat")
                lon = arguments.get("lon")

                # If the latitude is not provided
                if lat is None:
                    # Raise an error
                    raise ValueError("Latitude is required for get-daily-forecast")

                # If the longitude is not provided
                if lon is None:
                    # Raise an error
                    raise ValueError("Longitude is required for get-daily-forecast")

                # Extract optional parameters
                units = arguments.get("units", "standard")
                cnt = int(arguments.get("cnt", 7))

                # Call the function with extracted parameters
                result = await get_daily_forecast(
                    lat=lat, lon=lon, units=units, cnt=cnt
                )

                # Return the result
                return [types.TextContent(type="text", text=json.dumps(result))]

            # Get current air pollution
            case "get-current-air-pollution":
                # Extract required parameters
                lat = arguments.get("lat")
                lon = arguments.get("lon")

                # If the latitude is not provided
                if lat is None:
                    # Raise an error
                    raise ValueError(
                        "Latitude is required for get-current-air-pollution"
                    )

                # If the longitude is not provided
                if lon is None:
                    # Raise an error
                    raise ValueError(
                        "Longitude is required for get-current-air-pollution"
                    )

                # Call the function with extracted parameters
                result = await get_current_air_pollution(lat=lat, lon=lon)

                # Return the result
                return [types.TextContent(type="text", text=json.dumps(result))]

            # Get forecast air pollution
            case "get-forecast-air-pollution":
                # Extract required parameters
                lat = arguments.get("lat")
                lon = arguments.get("lon")

                # If the latitude is not provided
                if lat is None:
                    # Raise an error
                    raise ValueError(
                        "Latitude is required for get-forecast-air-pollution"
                    )

                # If the longitude is not provided
                if lon is None:
                    # Raise an error
                    raise ValueError(
                        "Longitude is required for get-forecast-air-pollution"
                    )

                # Call the function with extracted parameters
                result = await get_forecast_air_pollution(lat=lat, lon=lon)

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
        parser = argparse.ArgumentParser(description="Run the OpenWeather MCP Server")

        # Add arguments
        parser.add_argument(
            "--host", type=str, default="0.0.0.0", help="Host to bind to"
        )
        parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
        parser.add_argument("--debug", type=bool, default=False, help="Debug mode")

        # Parse the arguments
        args = parser.parse_args()

        # Initialize the Starlette app
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


# Initialize the OpenWeather MCP Server
server = OpenWeatherMCPServer()
