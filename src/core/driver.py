"""WebDriver management for web scraping."""

import threading
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.utils.logging import scraper_logger


class WebDriverManager:
    """Thread-safe WebDriver manager."""
    
    def __init__(self):
        self.thread_local = threading.local()
        self.chrome_options = self._setup_chrome_options()
    
    def _setup_chrome_options(self) -> Options:
        """Configure Chrome options for headless operation."""
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--start-maximized')
        options.add_argument('--start-fullscreen')
        options.add_argument('--disable-dev-shm-usage')
        return options
    
    def get_driver(self) -> webdriver.Chrome:
        """Get or create a WebDriver instance for the current thread."""
        driver_instance = getattr(self.thread_local, 'driver_instance', None)
        
        if driver_instance is None:
            scraper_logger.info("Creating new WebDriver instance")
            driver_instance = DriverInstance()
            self.thread_local.driver_instance = driver_instance
        
        return driver_instance.driver
    
    def cleanup(self):
        """Clean up WebDriver instances."""
        driver_instance = getattr(self.thread_local, 'driver_instance', None)
        if driver_instance:
            driver_instance.cleanup()
            self.thread_local.driver_instance = None


class DriverInstance:
    """Individual WebDriver instance wrapper."""
    
    def __init__(self):
        self.driver = webdriver.Chrome(options=WebDriverManager().chrome_options)
    
    def cleanup(self):
        """Clean up the WebDriver instance."""
        try:
            self.driver.quit()
            scraper_logger.info("WebDriver instance cleaned up successfully")
        except Exception as e:
            scraper_logger.error(f"Error cleaning up WebDriver: {e}")


# Global driver manager instance
driver_manager = WebDriverManager()
