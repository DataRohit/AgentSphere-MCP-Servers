"""
Custom logger module for serpapi-google-mcp-server.
Provides colored logging functionality using colorama.
"""

# Standard library imports
import logging
import sys
from typing import Optional

# Third party imports
from colorama import Back, Fore, Style, init

# Initialize colorama
init(autoreset=True)


# Custom formatter that adds colors to log messages based on their level
class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds colors to log messages based on their level.

    Inherits:
        logging.Formatter

    Attributes:
        COLORS (dict[str, str]): Dictionary mapping log levels to colorama color codes

    Methods:
        format(record: logging.LogRecord) -> str: Format the log record with appropriate colors
    """

    # Dictionary mapping log levels to colorama color codes
    COLORS = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.RED + Back.WHITE + Style.BRIGHT,
    }

    # Format the log record with appropriate colors
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with appropriate colors.

        Args:
            record (logging.LogRecord): The log record to format

        Returns:
            str: The formatted log message with color codes
        """

        # Get the log level name
        levelname = record.levelname

        # If the log level name is in the COLORS dictionary
        if levelname in self.COLORS:
            # Colorize the log level name
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"

            # Colorize the log message
            record.msg = f"{self.COLORS[levelname]}{record.msg}{Style.RESET_ALL}"

        # Return the formatted log message
        return super().format(record)


# Get a configured logger with colored output
def get_logger(name: str, level: Optional[int] = logging.INFO) -> logging.Logger:
    """
    Get a configured logger with colored output.

    Args:
        name (str): The name of the logger
        level (Optional[int]): The logging level (default: INFO)

    Returns:
        logging.Logger: A configured logger instance
    """

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers if any
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Create formatter
    formatter = ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    # Return the logger
    return logger
