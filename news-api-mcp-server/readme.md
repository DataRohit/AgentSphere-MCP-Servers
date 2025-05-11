# News API MCP Server

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

A Model Control Protocol (MCP) server that provides AI systems with seamless access to news data through the [News API](https://newsapi.org/). This server exposes standardized tools for querying the latest news articles and headlines, enabling AI agents to retrieve up-to-date news information.

## What is MCP?

Model Control Protocol (MCP) is a standardized protocol for AI systems to interact with external tools and services. This server implements the MCP specification, allowing AI models to:

- Discover available tools through a standardized interface
- Call tools with structured inputs
- Receive structured outputs that can be easily processed

This creates a consistent way for AI systems to access real-time news data without needing custom integration code for each news source.

## Features

- **News Search**: Find news articles based on specific topics or keywords
- **Headlines**: Get top headlines for specific countries
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
- News API key (get one at [newsapi.org](https://newsapi.org/))
- Docker (optional, for containerized deployment)

## Installation

### From Source

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd news-api-mcp-server
   ```

2. Install the package:

   ```bash
   pip install -e .
   ```

3. Create a `.env` file in the project root with your News API key:

   ```plaintext
   NEWS_API_KEY=your_api_key_here
   ```

### Using Docker

If you prefer using Docker, you can skip the Python installation and use the provided Dockerfile.

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `NEWS_API_KEY` | Your News API key | Yes | - |

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
news-api-mcp-server
```

Or customize the host, port, and debug mode:

```bash
news-api-mcp-server --host 127.0.0.1 --port 8080 --debug True
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

#### get-news

Search for news articles based on a topic or keyword.

**Input Schema:**

```json
{
  "topic": "string",  // Topic to search for
  "page_size": "number"  // Number of results to return (1-25)
}
```

**Example Request:**

```json
{
  "topic": "artificial intelligence",
  "page_size": 5
}
```

**Example Response:**

```json
[
  {
    "source": {
      "id": "source-id",
      "name": "Source Name"
    },
    "author": "Author Name",
    "title": "Article Title",
    "description": "Article description...",
    "url": "https://article-url.com",
    "urlToImage": "https://image-url.com",
    "publishedAt": "2023-05-01T12:00:00Z",
    "content": "Article content..."
  },
  // Additional articles...
]
```

#### get-headlines

Get top headlines for a specific country.

**Input Schema:**

```json
{
  "country": "string",  // Country code (2 letters)
  "page_size": "number"  // Number of results to return (1-25)
}
```

**Example Request:**

```json
{
  "country": "us",
  "page_size": 5
}
```

**Example Response:**

```json
[
  {
    "source": {
      "id": "source-id",
      "name": "Source Name"
    },
    "author": "Author Name",
    "title": "Headline Title",
    "description": "Headline description...",
    "url": "https://headline-url.com",
    "urlToImage": "https://image-url.com",
    "publishedAt": "2023-05-01T12:00:00Z",
    "content": "Headline content..."
  },
  // Additional headlines...
]
```

### Error Handling

The server returns appropriate error messages when:

- Required parameters are missing
- Parameters are invalid
- The News API returns an error
- The server encounters an internal error

Error responses include a descriptive message to help diagnose the issue.

## Docker Usage

### Building the Image

Build the Docker image:

```bash
docker build -t news-api-mcp-server .
```

### Running the Container

Run the container with your News API key:

```bash
docker run -p 8000:8000 -e NEWS_API_KEY=your_api_key_here news-api-mcp-server
```

Or use a `.env` file:

```bash
docker run -p 8000:8000 --env-file .env news-api-mcp-server
```

### Docker Compose

You can also use Docker Compose for easier management:

```yaml
version: '3'

services:
  news-api-mcp-server:
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
   cd news-api-mcp-server
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

4. Create a `.env` file with your News API key:

   ```plaintext
   NEWS_API_KEY=your_api_key_here
   ```

## Security Considerations

### API Key Protection

- Never commit your News API key to version control
- Use environment variables or `.env` files to store your API key
- When deploying, use secure methods to provide the API key (environment variables, secrets management)

### Rate Limiting

The News API has rate limits. Be aware of these limits when using the server in production:

- Developer plan: 100 requests per day
- Standard plan: 500 requests per day
- Premium plans: Higher limits available

Implement appropriate caching strategies if you expect high usage.

## Troubleshooting

### Common Issues

#### Server Won't Start

- Ensure Python 3.12+ is installed
- Check that all dependencies are installed correctly
- Verify that the port is not already in use

#### API Key Issues

- Ensure your News API key is valid
- Check that the `NEWS_API_KEY` environment variable is set correctly
- Verify that your News API subscription is active

#### API Rate Limiting Issues

- If you're receiving rate limit errors, check your News API usage
- Consider implementing caching to reduce API calls
- Upgrade your News API plan if necessary

### Getting Help

If you encounter issues not covered here, please open an issue on the repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [News API](https://newsapi.org/) for providing the news data API
- [MCP Framework](https://github.com/your-organization/mcp) for the Model Control Protocol implementation
- All contributors to this project
