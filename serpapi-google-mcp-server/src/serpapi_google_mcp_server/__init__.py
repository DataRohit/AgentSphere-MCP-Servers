# Imports
from serpapi_google_mcp_server.server import server


# Main function
def main():
    # Run the server
    server.run()


# Export main function and server
__all__ = ["main", "server"]
