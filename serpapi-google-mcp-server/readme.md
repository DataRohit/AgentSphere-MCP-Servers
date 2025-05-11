# SerpAPI Google MCP Server

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

A Model Control Protocol (MCP) server that provides AI systems with seamless access to Google search data through [SerpAPI](https://serpapi.com/). This server exposes standardized tools for querying different Google data sources including events, finance information, flights, hotels, jobs, places, and shopping results, enabling AI agents to retrieve up-to-date information from across the web.

## What is MCP?

Model Control Protocol (MCP) is a standardized protocol for AI systems to interact with external tools and services. This server implements the MCP specification, allowing AI models to:

- Discover available tools through a standardized interface
- Call tools with structured inputs
- Receive structured outputs that can be easily processed

This creates a consistent way for AI systems to access Google search data without needing custom integration code for each data source.

## Features

- **Events Search**: Find events based on search queries
- **Finance Data**: Retrieve financial information for stocks and companies
- **Flight Search**: Search for flights with detailed filtering options
- **Hotel Search**: Find accommodations with comprehensive filtering
- **Job Search**: Search for job listings by query and location
- **Places Search**: Find local businesses and points of interest
- **Shopping Search**: Search for products across online retailers
- **Standardized Protocol**: Implements the MCP specification for seamless AI integration
- **Containerized**: Ready to deploy with Docker
- **Async Processing**: Built with modern async Python for efficient request handling
- **Health Checks**: Includes health check endpoints for monitoring

## Technology Stack

- **Python 3.12+**: Built with modern Python features
- **MCP Framework**: Implements the Model Control Protocol specification
- **SerpAPI Client**: Official Google Search Results API client
- **HTTPX**: Async HTTP client for efficient API requests
- **Starlette/Uvicorn**: High-performance ASGI server
- **Docker**: Containerized for easy deployment
- **Server-Sent Events (SSE)**: Real-time communication channel

## Prerequisites

- Python 3.12 or higher
- SerpAPI API key (get one at [serpapi.com](https://serpapi.com/))
- Docker (optional, for containerized deployment)

## Installation

### From Source

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd serpapi-google-mcp-server
   ```

2. Install the package:

   ```bash
   pip install -e .
   ```

3. Create a `.env` file in the project root with your SerpAPI API key:

   ```plaintext
   SERPAPI_API_KEY=your_api_key_here
   ```

### Using Docker

If you prefer using Docker, you can skip the Python installation and use the provided Dockerfile.

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SERPAPI_API_KEY` | Your SerpAPI API key | Yes | - |

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
serpapi-google-mcp-server
```

Or customize the host, port, and debug mode:

```bash
serpapi-google-mcp-server --host 127.0.0.1 --port 8080 --debug True
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

#### get-events

Search for events based on a query string.

**Input Schema:**

```json
{
  "query": "string",  // Query to search for
  "page": "number"    // Page number to return
}
```

**Example Request:**

```json
{
  "query": "concerts in new york",
  "page": 1
}
```

**Example Response:**

```json
[
  {
    "title": "Concert at Madison Square Garden",
    "date": "Tomorrow at 8 PM",
    "venue": {
      "name": "Madison Square Garden",
      "address": "4 Pennsylvania Plaza, New York, NY 10001"
    },
    "link": "https://example.com/event1",
    "description": "Live performance by popular artist",
    "ticket_info": {
      "price": "$50 - $150",
      "availability": "Limited seats available"
    }
  },
  // Additional events...
]
```

#### get-finance-data

Retrieve financial information for stocks and companies.

**Input Schema:**

```json
{
  "query": "string"  // Finance query to search for
}
```

**Example Request:**

```json
{
  "query": "AAPL"
}
```

**Example Response:**

```json
{
  "title": "Apple Inc (AAPL)",
  "price": {
    "amount": 182.63,
    "currency": "$"
  },
  "price_movement": {
    "movement": "up",
    "amount": 1.25,
    "percentage": "0.69%"
  },
  "market": {
    "name": "NASDAQ",
    "status": "Open",
    "time": "4:00 PM EDT"
  },
  "about": {
    "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide.",
    "headquarters": "Cupertino, California",
    "founded": "1976",
    "ceo": "Tim Cook"
  },
  "key_stats": {
    "market_cap": "2.85T",
    "pe_ratio": "30.21",
    "dividend_yield": "0.50%"
  }
}
```

#### get-flights

Search for flights with options for departure/arrival locations, dates, class, and more.

**Input Schema:**

```json
{
  "departure_id": "string",    // Departure airport ID
  "arrival_id": "string",      // Arrival airport ID
  "outbound_date": "string",   // Outbound date (YYYY-MM-DD)
  "return_date": "string",     // Return date (YYYY-MM-DD), optional
  "currency": "string",        // Currency code (default: USD)
  "flight_type": "number",     // 1 = Round trip, 2 = One way
  "travel_class": "number",    // 1 = Economy, 2 = Premium economy, 3 = Business, 4 = First
  "adults": "number",          // Number of adults
  "children": "number",        // Number of children
  "infants_in_seat": "number", // Number of infants in seat
  "infants_on_lap": "number",  // Number of infants on lap
  "sort_by": "number",         // Sorting order
  "stops": "number",           // Number of stops
  "bags": "number",            // Number of carry-on bags
  "max_price": "number"        // Maximum ticket price
}
```

**Example Request:**

```json
{
  "departure_id": "JFK",
  "arrival_id": "LAX",
  "outbound_date": "2023-12-15",
  "return_date": "2023-12-22",
  "currency": "USD",
  "flight_type": 1,
  "travel_class": 1,
  "adults": 1,
  "children": 0,
  "infants_in_seat": 0,
  "infants_on_lap": 0,
  "sort_by": 2,
  "stops": 0,
  "bags": 1,
  "max_price": 500
}
```

**Example Response:**

```json
[
  {
    "flight_id": "ABC123",
    "price": {
      "amount": 349.99,
      "currency": "USD"
    },
    "outbound": {
      "departure": {
        "airport": "JFK",
        "time": "07:30 AM",
        "date": "2023-12-15"
      },
      "arrival": {
        "airport": "LAX",
        "time": "10:45 AM",
        "date": "2023-12-15"
      },
      "duration": "6h 15m",
      "airline": "Delta",
      "flight_number": "DL123"
    },
    "return": {
      "departure": {
        "airport": "LAX",
        "time": "08:15 PM",
        "date": "2023-12-22"
      },
      "arrival": {
        "airport": "JFK",
        "time": "04:45 AM",
        "date": "2023-12-23"
      },
      "duration": "5h 30m",
      "airline": "Delta",
      "flight_number": "DL456"
    },
    "stops": 0,
    "bags_included": 1
  },
  // Additional flights...
]
```

#### get-hotels

Find accommodations with filters for dates, price range, ratings, and amenities.

**Input Schema:**

```json
{
  "query": "string",              // Search query for hotels
  "check_in_date": "string",      // Check-in date (YYYY-MM-DD)
  "check_out_date": "string",     // Check-out date (YYYY-MM-DD)
  "adults": "number",             // Number of adults
  "children": "number",           // Number of children
  "children_ages": "string",      // Ages of children, comma-separated
  "currency": "string",           // Currency code
  "sort_by": "number",            // Sorting order
  "min_price": "number",          // Lower bound of price range
  "max_price": "number",          // Upper bound of price range
  "rating": "number",             // Filter by rating
  "hotel_class": "string",        // Filter by hotel class
  "free_cancellation": "boolean", // Show only results with free cancellation
  "vacation_rentals": "boolean",  // Search for vacation rentals instead of hotels
  "bedrooms": "number",           // Minimum number of bedrooms
  "bathrooms": "number"           // Minimum number of bathrooms
}
```

**Example Request:**

```json
{
  "query": "hotels in miami",
  "check_in_date": "2023-12-15",
  "check_out_date": "2023-12-22",
  "adults": 2,
  "children": 0,
  "currency": "USD",
  "sort_by": 3,
  "min_price": 100,
  "max_price": 300,
  "rating": 8,
  "hotel_class": "4",
  "free_cancellation": true
}
```

**Example Response:**

```json
[
  {
    "name": "Oceanfront Resort & Spa",
    "address": "123 Beach Drive, Miami, FL 33139",
    "price": {
      "amount": 249,
      "currency": "USD",
      "period": "per night"
    },
    "rating": {
      "value": 4.5,
      "count": 1250
    },
    "class": "4-star hotel",
    "amenities": [
      "Free Wi-Fi",
      "Pool",
      "Spa",
      "Restaurant",
      "Fitness center"
    ],
    "images": [
      "https://example.com/hotel1-image1.jpg",
      "https://example.com/hotel1-image2.jpg"
    ],
    "free_cancellation": true,
    "availability": "Only 3 rooms left"
  },
  // Additional hotels...
]
```

#### get-jobs

Search for job listings by query and location.

**Input Schema:**

```json
{
  "query": "string",    // Job search query
  "location": "string"  // Location for job search
}
```

**Example Request:**

```json
{
  "query": "software engineer",
  "location": "San Francisco, CA"
}
```

**Example Response:**

```json
[
  {
    "title": "Senior Software Engineer",
    "company": "Tech Innovations Inc.",
    "location": "San Francisco, CA",
    "description": "We are looking for a Senior Software Engineer to join our team...",
    "salary": "$120,000 - $150,000 a year",
    "job_type": "Full-time",
    "posted_time": "3 days ago",
    "apply_link": "https://example.com/apply/job1",
    "requirements": [
      "5+ years of experience in software development",
      "Proficiency in Python and JavaScript",
      "Experience with cloud platforms"
    ]
  },
  // Additional jobs...
]
```

#### get-places

Find local businesses and points of interest.

**Input Schema:**

```json
{
  "query": "string",    // Search query for places
  "location": "string"  // Location for place search
}
```

**Example Request:**

```json
{
  "query": "coffee shops",
  "location": "Portland, OR"
}
```

**Example Response:**

```json
[
  {
    "name": "Artisan Coffee House",
    "address": "123 Main St, Portland, OR 97201",
    "phone": "(503) 555-1234",
    "website": "https://example.com/artisan-coffee",
    "hours": {
      "Monday": "7 AM - 7 PM",
      "Tuesday": "7 AM - 7 PM",
      "Wednesday": "7 AM - 7 PM",
      "Thursday": "7 AM - 7 PM",
      "Friday": "7 AM - 8 PM",
      "Saturday": "8 AM - 8 PM",
      "Sunday": "8 AM - 6 PM"
    },
    "rating": {
      "value": 4.7,
      "count": 342
    },
    "price_level": "$$",
    "categories": ["Coffee Shop", "Bakery", "Breakfast"],
    "images": [
      "https://example.com/coffee1-image1.jpg",
      "https://example.com/coffee1-image2.jpg"
    ]
  },
  // Additional places...
]
```

#### get-shopping

Search for products across online retailers.

**Input Schema:**

```json
{
  "query": "string"  // Search query for products
}
```

**Example Request:**

```json
{
  "query": "wireless headphones"
}
```

**Example Response:**

```json
[
  {
    "title": "Premium Wireless Headphones",
    "link": "https://example.com/product1",
    "source": "Major Electronics Retailer",
    "price": {
      "value": 149.99,
      "currency": "$"
    },
    "rating": {
      "value": 4.5,
      "count": 1250
    },
    "shipping": "Free shipping",
    "description": "Noise-cancelling wireless headphones with 30-hour battery life",
    "thumbnail": "https://example.com/headphones1-thumbnail.jpg"
  },
  // Additional products...
]
```

### Error Handling

The server returns appropriate error messages when:

- Required parameters are missing
- Parameters are invalid
- The SerpAPI returns an error
- The server encounters an internal error

Error responses include a descriptive message to help diagnose the issue.

## Docker Usage

### Building the Image

Build the Docker image:

```bash
docker build -t serpapi-google-mcp-server .
```

### Running the Container

Run the container with your SerpAPI API key:

```bash
docker run -p 8000:8000 -e SERPAPI_API_KEY=your_api_key_here serpapi-google-mcp-server
```

Or use a `.env` file:

```bash
docker run -p 8000:8000 --env-file .env serpapi-google-mcp-server
```

### Docker Compose

You can also use Docker Compose for easier management:

```yaml
version: '3'

services:
  serpapi-google-mcp-server:
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
   cd serpapi-google-mcp-server
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

4. Create a `.env` file with your SerpAPI API key:

   ```plaintext
   SERPAPI_API_KEY=your_api_key_here
   ```

## Security Considerations

### API Key Protection

- Never commit your SerpAPI API key to version control
- Use environment variables or `.env` files to store your API key
- When deploying, use secure methods to provide the API key (environment variables, secrets management)

### Rate Limiting

SerpAPI has rate limits based on your subscription plan. Be aware of these limits when using the server in production:

- Free plan: 100 searches per month
- Basic plan: 5,000 searches per month
- Business plan: 20,000 searches per month
- Enterprise plan: Custom limits

Implement appropriate caching strategies if you expect high usage.

## Troubleshooting

### Common Issues

#### Server Won't Start

- Ensure Python 3.12+ is installed
- Check that all dependencies are installed correctly
- Verify that the port is not already in use

#### API Key Issues

- Ensure your SerpAPI API key is valid
- Check that the `SERPAPI_API_KEY` environment variable is set correctly
- Verify that your SerpAPI subscription is active

#### API Rate Limiting Issues

- If you're receiving rate limit errors, check your SerpAPI usage
- Consider implementing caching to reduce API calls
- Upgrade your SerpAPI plan if necessary

### Getting Help

If you encounter issues not covered here, please open an issue on the repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Rohit Ingole

## Acknowledgments

- [SerpAPI](https://serpapi.com/) for providing the Google search data API
- [MCP Framework](https://github.com/your-organization/mcp) for the Model Control Protocol implementation
- All contributors to this project
