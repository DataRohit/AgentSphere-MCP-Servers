# Import tools
from open_weather_mcp_server.tools.current_air_pollution_tool import (
    get_current_air_pollution,
)
from open_weather_mcp_server.tools.current_weather_tool import get_current_weather
from open_weather_mcp_server.tools.daily_forecast_tool import get_daily_forecast
from open_weather_mcp_server.tools.forecast_air_pollution_tool import (
    get_forecast_air_pollution,
)
from open_weather_mcp_server.tools.hourly_forecast_tool import get_hourly_forecast

# Export tools
__all__ = [
    "get_current_weather",
    "get_hourly_forecast",
    "get_daily_forecast",
    "get_current_air_pollution",
    "get_forecast_air_pollution",
]
