"""Basketball scraper for betting sites."""

from typing import Dict, List
from selenium.webdriver.common.by import By
from src.scrapers.base import BaseScraper
from src.utils.logging import scraper_logger


class BasketballScraper(BaseScraper):
    """Scraper for basketball matches from betting sites."""
    
    def __init__(self, site_name: str, sport: str = 'basketball'):
        super().__init__(site_name, sport)
    
    def scrape_matches(self, url: str) -> List[Dict]:
        """Scrape basketball matches from the specified URL."""
        if not self.get_page_with_retry(url):
            return []
        
        matches = []
        
        try:
            if 'tipsport' in self.site_name.lower():
                matches = self._scrape_tipsport()
            elif 'fortuna' in self.site_name.lower():
                matches = self._scrape_fortuna()
            elif 'nike' in self.site_name.lower():
                matches = self._scrape_nike()
            else:
                scraper_logger.warning(f"Unknown site for basketball scraping: {self.site_name}")
        
        except Exception as e:
            scraper_logger.error(f"Error scraping {self.site_name} basketball: {e}")
        
        return matches
    
    def _scrape_tipsport(self) -> List[Dict]:
        """Scrape basketball matches from Tipsport."""
        matches = []
        
        # Wait for matches to load
        if not self.wait_for_element(By.CSS_SELECTOR, ".o-matchRow", timeout=30):
            return matches
        
        match_elements = self.safe_find_elements(By.CSS_SELECTOR, ".o-matchRow")
        
        for match_element in match_elements:
            try:
                match_data = self._extract_tipsport_match(match_element)
                if match_data and self.is_match_valid(match_data):
                    matches.append(match_data)
            except Exception as e:
                scraper_logger.debug(f"Error extracting Tipsport match: {e}")
        
        scraper_logger.info(f"Scraped {len(matches)} basketball matches from Tipsport")
        return matches
    
    def _extract_tipsport_match(self, match_element) -> Dict:
        """Extract match data from Tipsport match element."""
        # Extract team names
        team_elements = match_element.find_elements(By.CSS_SELECTOR, ".o-matchRow__team")
        if len(team_elements) < 2:
            return {}
        
        home_team = team_elements[0].text.strip()
        away_team = team_elements[1].text.strip()
        
        # Extract match time
        time_element = self.safe_find_element(By.CSS_SELECTOR, ".o-matchRow__time")
        match_time = time_element.text.strip() if time_element else ""
        
        # Extract odds
        odds_elements = match_element.find_elements(By.CSS_SELECTOR, ".o-matchRow__odd")
        odds = {}
        
        if len(odds_elements) >= 2:
            home_odds = self.extract_odds(odds_elements[0].text)
            away_odds = self.extract_odds(odds_elements[1].text)
            
            if home_odds and away_odds:
                odds['home_away'] = {
                    'home': home_odds,
                    'away': away_odds
                }
        
        return {
            'home_team': home_team,
            'away_team': away_team,
            'match_time': match_time,
            'sport': self.sport,
            'site': self.site_name,
            'odds': odds
        }
    
    def _scrape_fortuna(self) -> List[Dict]:
        """Scrape basketball matches from Fortuna."""
        matches = []
        
        # Wait for matches to load
        if not self.wait_for_element(By.CSS_SELECTOR, ".market-row", timeout=30):
            return matches
        
        match_elements = self.safe_find_elements(By.CSS_SELECTOR, ".market-row")
        
        for match_element in match_elements:
            try:
                match_data = self._extract_fortuna_match(match_element)
                if match_data and self.is_match_valid(match_data):
                    matches.append(match_data)
            except Exception as e:
                scraper_logger.debug(f"Error extracting Fortuna match: {e}")
        
        scraper_logger.info(f"Scraped {len(matches)} basketball matches from Fortuna")
        return matches
    
    def _extract_fortuna_match(self, match_element) -> Dict:
        """Extract match data from Fortuna match element."""
        # Extract team names
        team_element = self.safe_find_element(By.CSS_SELECTOR, ".market-name")
        if not team_element:
            return {}
        
        team_text = team_element.text.strip()
        if ' - ' in team_text:
            teams = team_text.split(' - ')
            home_team = teams[0].strip()
            away_team = teams[1].strip()
        else:
            return {}
        
        # Extract match time
        time_element = self.safe_find_element(By.CSS_SELECTOR, ".market-time")
        match_time = time_element.text.strip() if time_element else ""
        
        # Extract odds
        odds_elements = match_element.find_elements(By.CSS_SELECTOR, ".market-odd")
        odds = {}
        
        if len(odds_elements) >= 2:
            home_odds = self.extract_odds(odds_elements[0].text)
            away_odds = self.extract_odds(odds_elements[1].text)
            
            if home_odds and away_odds:
                odds['home_away'] = {
                    'home': home_odds,
                    'away': away_odds
                }
        
        return {
            'home_team': home_team,
            'away_team': away_team,
            'match_time': match_time,
            'sport': self.sport,
            'site': self.site_name,
            'odds': odds
        }
    
    def _scrape_nike(self) -> List[Dict]:
        """Scrape basketball matches from Nike."""
        matches = []
        
        # Wait for matches to load
        if not self.wait_for_element(By.CSS_SELECTOR, ".event-row", timeout=30):
            return matches
        
        match_elements = self.safe_find_elements(By.CSS_SELECTOR, ".event-row")
        
        for match_element in match_elements:
            try:
                match_data = self._extract_nike_match(match_element)
                if match_data and self.is_match_valid(match_data):
                    matches.append(match_data)
            except Exception as e:
                scraper_logger.debug(f"Error extracting Nike match: {e}")
        
        scraper_logger.info(f"Scraped {len(matches)} basketball matches from Nike")
        return matches
    
    def _extract_nike_match(self, match_element) -> Dict:
        """Extract match data from Nike match element."""
        # Extract team names
        team_elements = match_element.find_elements(By.CSS_SELECTOR, ".team-name")
        if len(team_elements) < 2:
            return {}
        
        home_team = team_elements[0].text.strip()
        away_team = team_elements[1].text.strip()
        
        # Extract match time
        time_element = self.safe_find_element(By.CSS_SELECTOR, ".event-time")
        match_time = time_element.text.strip() if time_element else ""
        
        # Extract odds
        odds_elements = match_element.find_elements(By.CSS_SELECTOR, ".odd-value")
        odds = {}
        
        if len(odds_elements) >= 2:
            home_odds = self.extract_odds(odds_elements[0].text)
            away_odds = self.extract_odds(odds_elements[1].text)
            
            if home_odds and away_odds:
                odds['home_away'] = {
                    'home': home_odds,
                    'away': away_odds
                }
        
        return {
            'home_team': home_team,
            'away_team': away_team,
            'match_time': match_time,
            'sport': self.sport,
            'site': self.site_name,
            'odds': odds
        }
