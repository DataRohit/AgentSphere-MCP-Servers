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
from news_api_mcp_server.health import health_routes
from news_api_mcp_server.tools import get_headlines, get_news

# Local imports
from news_api_mcp_server.utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


# News API MCP Server
class NewsAPIMCPServer:
    # Constructor
    def __init__(self):
        """Initialize the News API MCP Server."""

        # Initialize the server
        self.server = Server("news-api-mcp-server")

        # Register handlers
        self._register_handlers()

    # Method to register handlers
    def _register_handlers(self):
        """Register the handlers for the News API MCP Server."""

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
                name="get-news",
                description="Get the latest news for a given topic",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "Topic to search for",
                        },
                        "page_size": {
                            "type": "number",
                            "description": "Number of results to return (1-25)",
                        },
                    },
                    "required": ["topic", "page_size"],
                },
            ),
            types.Tool(
                name="get-headlines",
                description="Get the latest headlines for a given country",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "country": {
                            "type": "string",
                            "description": "Country code (2 letters)",
                        },
                        "page_size": {
                            "type": "number",
                            "description": "Number of results to return (1-25)",
                        },
                    },
                    "required": ["country", "page_size"],
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
            # Get news
            case "get-news":
                # Extract required parameters
                topic = arguments.get("topic")

                # If the topic is not provided
                if not topic:
                    # Raise an error
                    raise ValueError("Topic is required for get-news")

                # Extract optional parameters
                page_size = int(arguments.get("page_size", 5))

                # Call the function with extracted parameters
                result = await get_news(topic=topic, page_size=page_size)
                
                # Return the result
                return [types.TextContent(type="text", text=json.dumps(result))]

            # Get headlines
            case "get-headlines":
                # Extract required parameters
                country = arguments.get("country")

                # If the country is not provided
                if not country:
                    # Raise an error
                    raise ValueError("Country is required for get-headlines")

                # Extract optional parameters
                page_size = int(arguments.get("page_size", 5))

                # Call the function with extracted parameters
                result = await get_headlines(country=country, page_size=page_size)
                
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
        parser = argparse.ArgumentParser(description="Run the News API MCP Server")

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


# Initialize the News API MCP Server
server = NewsAPIMCPServer()
