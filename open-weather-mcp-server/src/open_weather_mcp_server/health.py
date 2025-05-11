# Standard library imports
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route


# Health check endpoint
async def health_check(request: Request) -> PlainTextResponse:
    """
    Simple health check endpoint that returns 200 OK.
    Used by Docker healthcheck and Nginx to verify the service is running.

    Args:
        request (Request): The request object.

    Returns:
        PlainTextResponse: A 200 OK response.
    """

    # Return the response
    return PlainTextResponse("OK")


# Health routes
health_routes = [Route("/health", endpoint=health_check, methods=["GET"])]
