"""Base scraper class with common functionality for all betting sites."""

import re
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from src.core.driver import driver_manager
from src.utils.logging import scraper_logger
from src.config import config


class BaseScraper(ABC):
    """Base class for all betting site scrapers."""
    
    def __init__(self, site_name: str, sport: str):
        self.site_name = site_name
        self.sport = sport
        self.driver = None
        self.wait_timeout = config.scraping.max_wait_time
    
    def __enter__(self):
        """Context manager entry."""
        self.driver = driver_manager.get_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if exc_type:
            scraper_logger.error(f"Error in {self.site_name} scraper: {exc_val}")
    
    @abstractmethod
    def scrape_matches(self, url: str) -> List[Dict]:
        """Scrape matches from the betting site."""
        pass
    
    def wait_for_element(self, by: By, value: str, timeout: Optional[int] = None) -> bool:
        """Wait for an element to be present."""
        try:
            wait_time = timeout or self.wait_timeout
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            scraper_logger.warning(f"Element {value} not found within {wait_time} seconds")
            return False
    
    def safe_find_element(self, by: By, value: str) -> Optional[any]:
        """Safely find an element without throwing exceptions."""
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            return None
    
    def safe_find_elements(self, by: By, value: str) -> List[any]:
        """Safely find elements without throwing exceptions."""
        try:
            return self.driver.find_elements(by, value)
        except NoSuchElementException:
            return []
    
    def extract_odds(self, odds_text: str) -> Optional[float]:
        """Extract and validate odds from text."""
        try:
            # Remove any non-numeric characters except decimal point
            cleaned_odds = re.sub(r'[^\d.]', '', odds_text.strip())
            if cleaned_odds:
                odds = float(cleaned_odds)
                # Basic validation - odds should be positive and reasonable
                if 1.0 <= odds <= 1000.0:
                    return odds
        except (ValueError, AttributeError):
            pass
        return None
    
    def normalize_team_name(self, team_name: str) -> str:
        """Normalize team names for better matching."""
        if not team_name:
            return ""
        
        # Remove common prefixes/suffixes and normalize
        normalized = team_name.strip()
        normalized = re.sub(r'\s+', ' ', normalized)  # Multiple spaces to single
        normalized = re.sub(r'[^\w\s]', '', normalized)  # Remove special chars
        
        return normalized.lower()
    
    def calculate_similarity(self, name1: str, name2: str) -> float:
        """Calculate similarity between two team names."""
        norm1 = self.normalize_team_name(name1)
        norm2 = self.normalize_team_name(name2)
        
        return SequenceMatcher(None, norm1, norm2).ratio()
    
    def is_match_valid(self, match_data: Dict) -> bool:
        """Check if match data is valid and should be processed."""
        # Check for required fields
        required_fields = ['home_team', 'away_team']
        if not all(match_data.get(field) for field in required_fields):
            return False
        
        # Check match status against filters
        match_status = match_data.get('status', '')
        for pattern in config.match_status_filters:
            if re.match(pattern, match_status, re.IGNORECASE):
                scraper_logger.debug(f"Match filtered out by status: {match_status}")
                return False
        
        return True
    
    def handle_cookie_consent(self):
        """Handle cookie consent popups if present."""
        cookie_selectors = [
            "button[id*='cookie']",
            "button[class*='cookie']",
            "button[id*='consent']",
            "button[class*='consent']",
            ".cookie-accept",
            "#cookie-accept",
            "[data-testid*='cookie']"
        ]
        
        for selector in cookie_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed():
                    element.click()
                    scraper_logger.info(f"Clicked cookie consent button: {selector}")
                    time.sleep(1)
                    break
            except NoSuchElementException:
                continue
    
    def scroll_to_load_content(self, scroll_pause_time: float = 2.0):
        """Scroll down to load dynamic content."""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new content to load
            time.sleep(scroll_pause_time)
            
            # Calculate new scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
            last_height = new_height
    
    def get_page_with_retry(self, url: str, max_retries: int = 3) -> bool:
        """Load page with retry logic."""
        for attempt in range(max_retries):
            try:
                scraper_logger.info(f"Loading {self.site_name} page (attempt {attempt + 1}): {url}")
                self.driver.get(url)
                
                # Handle cookie consent
                self.handle_cookie_consent()
                
                # Wait a bit for page to stabilize
                time.sleep(2)
                
                return True
                
            except Exception as e:
                scraper_logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)  # Wait before retry
                else:
                    scraper_logger.error(f"Failed to load {url} after {max_retries} attempts")
                    return False
        
        return False
