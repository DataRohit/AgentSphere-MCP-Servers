# OpenWeather MCP Server

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

A Model Control Protocol (MCP) server that provides AI systems with seamless access to weather data through the [OpenWeather API](https://openweathermap.org/). This server exposes standardized tools for querying current weather conditions, forecasts, and air pollution data, enabling AI agents to retrieve up-to-date meteorological information.

## What is MCP?

Model Control Protocol (MCP) is a standardized protocol for AI systems to interact with external tools and services. This server implements the MCP specification, allowing AI models to:

- Discover available tools through a standardized interface
- Call tools with structured inputs
- Receive structured outputs that can be easily processed

This creates a consistent way for AI systems to access real-time weather data without needing custom integration code for each weather data source.

## Features

- **Current Weather**: Get real-time weather conditions for any location
- **Hourly Forecast**: Access detailed hourly weather predictions
- **Daily Forecast**: Retrieve multi-day weather forecasts
- **Air Pollution**: Monitor current and forecasted air quality data
- **Standardized Protocol**: Implements the MCP specification for seamless AI integration
- **Containerized**: Ready to deploy with Docker
- **Async Processing**: Built with modern async Python for efficient request handling
- **Health Checks**: Includes health check endpoints for monitoring

## Technology Stack

- **Python 3.12+**: Built with modern Python features
- **MCP Framework**: Implements the Model Control Protocol specification
- **HTTPX**: Async HTTP client for efficient API requests
- **Starlette/Uvicorn**: High-performance ASGI server
- **Docker**: Containerized for easy deployment
- **Server-Sent Events (SSE)**: Real-time communication channel

## Prerequisites

- Python 3.12 or higher
- OpenWeather API key (get one at [openweathermap.org](https://openweathermap.org/api))
- Docker (optional, for containerized deployment)

## Installation

### From Source

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd open-weather-mcp-server
   ```

2. Install the package:

   ```bash
   pip install -e .
   ```

3. Create a `.env` file in the project root with your OpenWeather API key:

   ```plaintext
   OPEN_WEATHER_API_KEY=your_api_key_here
   ```

### Using Docker

If you prefer using Docker, you can skip the Python installation and use the provided Dockerfile.

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPEN_WEATHER_API_KEY` | Your OpenWeather API key | Yes | - |

### Command-Line Arguments

When starting the server, you can configure the following options:

| Argument | Description | Default |
|----------|-------------|---------|
| `--host` | Host to bind the server to | `0.0.0.0` |
| `--port` | Port to listen on | `8000` |
| `--debug` | Enable debug mode | `False` |

## Usage

### Running the Server

Start the server with default settings:

```bash
open-weather-mcp-server
```

Or customize the host, port, and debug mode:

```bash
open-weather-mcp-server --host 127.0.0.1 --port 8080 --debug True
```

### Connecting to the Server

The server exposes an SSE (Server-Sent Events) endpoint at:

```plaintext
http://{host}:{port}/sse
```

AI systems and clients that implement the MCP protocol can connect to this endpoint to discover and call the available tools.

### Health Check

The server provides a health check endpoint at:

```plaintext
http://{host}:{port}/health
```

This endpoint returns a 200 OK response when the server is running properly.

## API Documentation

### Available Tools

#### get-current-weather

Get the current weather conditions for a specific location.

**Input Schema:**

```json
{
  "lat": "number",  // Latitude, decimal (-90; 90)
  "lon": "number",  // Longitude, decimal (-180; 180)
  "units": "string"  // Units of measurement (standard, metric, imperial)
}
```

**Example Request:**

```json
{
  "lat": 40.7128,
  "lon": -74.0060,
  "units": "metric"
}
```

**Example Response:**

```json
{
  "coord": {
    "lon": -74.006,
    "lat": 40.7128
  },
  "weather": [
    {
      "id": 800,
      "main": "Clear",
      "description": "clear sky",
      "icon": "01d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 22.5,
    "feels_like": 21.8,
    "temp_min": 20.1,
    "temp_max": 24.3,
    "pressure": 1015,
    "humidity": 65
  },
  "visibility": 10000,
  "wind": {
    "speed": 3.6,
    "deg": 160
  },
  "clouds": {
    "all": 0
  },
  "dt": 1684930800,
  "sys": {
    "type": 2,
    "id": 2039034,
    "country": "US",
    "sunrise": 1684923464,
    "sunset": 1684976861
  },
  "timezone": -14400,
  "id": 5128581,
  "name": "New York",
  "cod": 200
}
```

#### get-hourly-forecast

Get hourly weather forecast for a specific location.

**Input Schema:**

```json
{
  "lat": "number",  // Latitude, decimal (-90; 90)
  "lon": "number",  // Longitude, decimal (-180; 180)
  "units": "string",  // Units of measurement (standard, metric, imperial)
  "cnt": "number"  // Number of hours to return (1-40)
}
```

**Example Request:**

```json
{
  "lat": 40.7128,
  "lon": -74.0060,
  "units": "metric",
  "cnt": 12
}
```

**Example Response:**

```json
{
  "cod": "200",
  "message": 0,
  "cnt": 12,
  "list": [
    {
      "dt": 1684936800,
      "main": {
        "temp": 22.8,
        "feels_like": 22.1,
        "temp_min": 22.8,
        "temp_max": 22.8,
        "pressure": 1015,
        "sea_level": 1015,
        "grnd_level": 1012,
        "humidity": 64,
        "temp_kf": 0
      },
      "weather": [
        {
          "id": 800,
          "main": "Clear",
          "description": "clear sky",
          "icon": "01d"
        }
      ],
      "clouds": {
        "all": 0
      },
      "wind": {
        "speed": 3.8,
        "deg": 165,
        "gust": 4.2
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2023-05-24 18:00:00"
    },
    // Additional hourly forecasts...
  ],
  "city": {
    "id": 5128581,
    "name": "New York",
    "coord": {
      "lat": 40.7128,
      "lon": -74.006
    },
    "country": "US",
    "population": 8175133,
    "timezone": -14400,
    "sunrise": 1684923464,
    "sunset": 1684976861
  }
}
```

#### get-daily-forecast

Get daily weather forecast for a specific location.

**Input Schema:**

```json
{
  "lat": "number",  // Latitude, decimal (-90; 90)
  "lon": "number",  // Longitude, decimal (-180; 180)
  "units": "string",  // Units of measurement (standard, metric, imperial)
  "cnt": "number"  // Number of days to return (1-16)
}
```

**Example Request:**

```json
{
  "lat": 40.7128,
  "lon": -74.0060,
  "units": "metric",
  "cnt": 7
}
```

**Example Response:**

```json
{
  "city": {
    "id": 5128581,
    "name": "New York",
    "coord": {
      "lon": -74.006,
      "lat": 40.7128
    },
    "country": "US",
    "population": 8175133,
    "timezone": -14400
  },
  "cod": "200",
  "message": 0,
  "cnt": 7,
  "list": [
    {
      "dt": 1684951200,
      "sunrise": 1684923464,
      "sunset": 1684976861,
      "temp": {
        "day": 24.2,
        "min": 18.5,
        "max": 25.1,
        "night": 19.3,
        "eve": 22.8,
        "morn": 18.7
      },
      "feels_like": {
        "day": 23.8,
        "night": 19.1,
        "eve": 22.5,
        "morn": 18.3
      },
      "pressure": 1015,
      "humidity": 55,
      "weather": [
        {
          "id": 800,
          "main": "Clear",
          "description": "clear sky",
          "icon": "01d"
        }
      ],
      "speed": 4.2,
      "deg": 170,
      "gust": 5.1,
      "clouds": 0,
      "pop": 0
    },
    // Additional daily forecasts...
  ]
}
```

#### get-current-air-pollution

Get current air pollution data for a specific location.

**Input Schema:**

```json
{
  "lat": "number",  // Latitude, decimal (-90; 90)
  "lon": "number"  // Longitude, decimal (-180; 180)
}
```

**Example Request:**

```json
{
  "lat": 40.7128,
  "lon": -74.0060
}
```

**Example Response:**

```json
{
  "coord": {
    "lon": -74.006,
    "lat": 40.7128
  },
  "list": [
    {
      "main": {
        "aqi": 2
      },
      "components": {
        "co": 250.34,
        "no": 0.89,
        "no2": 9.12,
        "o3": 100.14,
        "so2": 1.67,
        "pm2_5": 8.56,
        "pm10": 12.34,
        "nh3": 0.51
      },
      "dt": 1684936800
    }
  ]
}
```

#### get-forecast-air-pollution

Get forecast air pollution data for a specific location.

**Input Schema:**

```json
{
  "lat": "number",  // Latitude, decimal (-90; 90)
  "lon": "number"  // Longitude, decimal (-180; 180)
}
```

**Example Request:**

```json
{
  "lat": 40.7128,
  "lon": -74.0060
}
```

**Example Response:**

```json
{
  "coord": {
    "lon": -74.006,
    "lat": 40.7128
  },
  "list": [
    {
      "main": {
        "aqi": 2
      },
      "components": {
        "co": 250.34,
        "no": 0.89,
        "no2": 9.12,
        "o3": 100.14,
        "so2": 1.67,
        "pm2_5": 8.56,
        "pm10": 12.34,
        "nh3": 0.51
      },
      "dt": 1684936800
    },
    // Additional forecast data points...
  ]
}
```

### Error Handling

The server returns appropriate error messages when:

- Required parameters are missing
- Parameters are invalid
- The OpenWeather API returns an error
- The server encounters an internal error

Error responses include a descriptive message to help diagnose the issue.

## Docker Usage

### Building the Image

Build the Docker image:

```bash
docker build -t open-weather-mcp-server .
```

### Running the Container

Run the container with your OpenWeather API key:

```bash
docker run -p 8000:8000 -e OPEN_WEATHER_API_KEY=your_api_key_here open-weather-mcp-server
```

Or use a `.env` file:

```bash
docker run -p 8000:8000 --env-file .env open-weather-mcp-server
```

### Docker Compose

You can also use Docker Compose for easier management:

```yaml
version: '3'

services:
  open-weather-mcp-server:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Save this as `docker-compose.yml` and run:

```bash
docker-compose up -d
```

## Development

### Setting Up a Development Environment

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd open-weather-mcp-server
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:

   ```bash
   pip install -e .
   ```

4. Create a `.env` file with your OpenWeather API key:

   ```plaintext
   OPEN_WEATHER_API_KEY=your_api_key_here
   ```

## Security Considerations

### API Key Protection

- Never commit your OpenWeather API key to version control
- Use environment variables or `.env` files to store your API key
- When deploying, use secure methods to provide the API key (environment variables, secrets management)

### Rate Limiting

The OpenWeather API has rate limits. Be aware of these limits when using the server in production:

- Free plan: 60 calls/minute (1,000,000 calls/month)
- Paid plans: Higher limits available

Implement appropriate caching strategies if you expect high usage.

## Troubleshooting

### Common Issues

#### Server Won't Start

- Ensure Python 3.12+ is installed
- Check that all dependencies are installed correctly
- Verify that the port is not already in use

#### API Key Issues

- Ensure your OpenWeather API key is valid
- Check that the `OPEN_WEATHER_API_KEY` environment variable is set correctly
- Verify that your OpenWeather API subscription is active

#### API Rate Limiting Issues

- If you're receiving rate limit errors, check your OpenWeather API usage
- Consider implementing caching to reduce API calls
- Upgrade your OpenWeather API plan if necessary

### Getting Help

If you encounter issues not covered here, please open an issue on the repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenWeather API](https://openweathermap.org/) for providing the weather data API
- [MCP Framework](https://github.com/your-organization/mcp) for the Model Control Protocol implementation
- All contributors to this project
