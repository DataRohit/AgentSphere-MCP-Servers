# MCP Servers Collection

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

A collection of Model Control Protocol (MCP) servers that provide AI systems with standardized access to various data sources. This repository contains multiple MCP server implementations, each designed to expose different external APIs through a consistent interface for AI agents.

## What is MCP?

Model Control Protocol (MCP) is a standardized protocol for AI systems to interact with external tools and services. MCP servers implement this specification, allowing AI models to:

- Discover available tools through a standardized interface
- Call tools with structured inputs
- Receive structured outputs that can be easily processed

This creates a consistent way for AI systems to access external data without needing custom integration code for each data source.

## Included MCP Servers

This repository contains the following MCP server implementations:

### [News API MCP Server](./news-api-mcp-server)

Provides AI systems with access to news data through the [News API](https://newsapi.org/). This server exposes tools for:

- Searching news articles by topic
- Getting top headlines by country

[View News API MCP Server Documentation](./news-api-mcp-server/readme.md)

### [OpenWeather MCP Server](./open-weather-mcp-server)

Provides AI systems with access to weather data through the [OpenWeather API](https://openweathermap.org/). This server exposes tools for:

- Getting current weather conditions
- Retrieving hourly and daily forecasts
- Accessing air pollution data

[View OpenWeather MCP Server Documentation](./open-weather-mcp-server/readme.md)

### [SerpAPI Google MCP Server](./serpapi-google-mcp-server)

Provides AI systems with access to Google search data through [SerpAPI](https://serpapi.com/). This server exposes tools for:

- Searching for events
- Retrieving financial information
- Finding flights and hotels
- Searching for jobs, places, and products

[View SerpAPI Google MCP Server Documentation](./serpapi-google-mcp-server/readme.md)

## Common Features

All MCP servers in this collection share the following features:

- **Standardized Protocol**: Implements the MCP specification for seamless AI integration
- **Containerized**: Ready to deploy with Docker
- **Async Processing**: Built with modern async Python for efficient request handling
- **Health Checks**: Includes health check endpoints for monitoring
- **Server-Sent Events (SSE)**: Real-time communication channel

## Technology Stack

- **Python 3.12+**: Built with modern Python features
- **MCP Framework**: Implements the Model Control Protocol specification
- **HTTPX**: Async HTTP client for efficient API requests
- **Starlette/Uvicorn**: High-performance ASGI server
- **Docker**: Containerized for easy deployment

## Prerequisites

- Python 3.12 or higher
- API keys for the respective services:
  - News API key for the News API MCP Server
  - OpenWeather API key for the OpenWeather MCP Server
  - SerpAPI API key for the SerpAPI Google MCP Server
- Docker (optional, for containerized deployment)

## Installation and Setup

Each MCP server can be installed and run independently. Please refer to the individual server documentation for specific installation instructions.

### Common Installation Steps

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd MCPServers
   ```

2. Navigate to the specific server directory:

   ```bash
   cd <server-directory>  # e.g., news-api-mcp-server
   ```

3. Install the package:

   ```bash
   pip install -e .
   ```

4. Create a `.env` file with your API key:

   ```plaintext
   API_KEY=your_api_key_here  # Use the appropriate environment variable name
   ```

### Using Docker

Each server includes a Dockerfile for containerized deployment. You can build and run the Docker images individually or use Docker Compose to manage multiple servers.

#### Running Multiple Servers with Docker Compose

Create a `docker-compose.yml` file in the root directory:

```yaml
version: '3'

services:
  news-api-mcp-server:
    build: ./news-api-mcp-server
    ports:
      - "8001:8000"
    env_file:
      - ./news-api-mcp-server/.env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  open-weather-mcp-server:
    build: ./open-weather-mcp-server
    ports:
      - "8002:8000"
    env_file:
      - ./open-weather-mcp-server/.env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  serpapi-google-mcp-server:
    build: ./serpapi-google-mcp-server
    ports:
      - "8003:8000"
    env_file:
      - ./serpapi-google-mcp-server/.env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Run all servers:

```bash
docker-compose up -d
```

## Usage

### Connecting to the Servers

Each MCP server exposes an SSE (Server-Sent Events) endpoint at:

```plaintext
http://{host}:{port}/sse
```

AI systems and clients that implement the MCP protocol can connect to this endpoint to discover and call the available tools.

### Health Checks

Each server provides a health check endpoint at:

```plaintext
http://{host}:{port}/health
```

This endpoint returns a 200 OK response when the server is running properly.

## Security Considerations

### API Key Protection

- Never commit your API keys to version control
- Use environment variables or `.env` files to store your API keys
- When deploying, use secure methods to provide the API keys (environment variables, secrets management)

### Rate Limiting

Be aware of the rate limits for each external API:

- News API: Varies by subscription plan
- OpenWeather API: Varies by subscription plan
- SerpAPI: Varies by subscription plan

Implement appropriate caching strategies if you expect high usage.

## Contributing

Contributions are welcome! If you'd like to add a new MCP server or improve an existing one, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Add your changes
4. Submit a pull request

Please ensure your code follows the existing style and includes appropriate documentation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [News API](https://newsapi.org/) for providing the news data API
- [OpenWeather API](https://openweathermap.org/) for providing the weather data API
- [SerpAPI](https://serpapi.com/) for providing the Google search data API
- [MCP Framework](https://github.com/modelcontextprotocol/python-sdk) for the Model Control Protocol implementation
- All contributors to this project
