"""Core business logic modules for the flashscore system."""

from .arbitrage import ArbitrageCalculator
from .driver import WebDriverManager
from .notifications import NotificationManager

# Create global instances
arbitrage_calculator = ArbitrageCalculator()
driver_manager = WebDriverManager()
notification_manager = NotificationManager()

__all__ = [
    'ArbitrageCalculator',
    'WebDriverManager', 
    'NotificationManager',
    'arbitrage_calculator',
    'driver_manager',
    'notification_manager'
]
