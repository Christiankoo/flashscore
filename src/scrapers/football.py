"""Football scraper for betting sites."""

from typing import Dict, List
from selenium.webdriver.common.by import By
from src.scrapers.base import BaseScraper
from src.utils.logging import scraper_logger


class FootballScraper(BaseScraper):
    """Scraper for football matches from betting sites."""
    
    def __init__(self, site_name: str, sport: str = 'football'):
        super().__init__(site_name, sport)
    
    def scrape_matches(self, url: str) -> List[Dict]:
        """Scrape football matches from the specified URL."""
        if not self.get_page_with_retry(url):
            return []
        
        matches = []
        
        try:
            if 'flashscore' in self.site_name.lower():
                matches = self._scrape_flashscore()
            elif 'tipsport' in self.site_name.lower():
                matches = self._scrape_tipsport()
            elif 'fortuna' in self.site_name.lower():
                matches = self._scrape_fortuna()
            elif 'nike' in self.site_name.lower():
                matches = self._scrape_nike()
            else:
                scraper_logger.warning(f"Unknown site for football scraping: {self.site_name}")
        
        except Exception as e:
            scraper_logger.error(f"Error scraping {self.site_name} football: {e}")
        
        return matches
    
    def _scrape_flashscore(self) -> List[Dict]:
        """Scrape football matches from Flashscore."""
        matches = []
        
        # Wait for matches to load
        if not self.wait_for_element(By.CSS_SELECTOR, ".event__match", timeout=30):
            return matches
        
        match_elements = self.safe_find_elements(By.CSS_SELECTOR, ".event__match")
        
        for match_element in match_elements:
            try:
                match_data = self._extract_flashscore_match(match_element)
                if match_data and self.is_match_valid(match_data):
                    matches.append(match_data)
            except Exception as e:
                scraper_logger.debug(f"Error extracting Flashscore match: {e}")
        
        scraper_logger.info(f"Scraped {len(matches)} football matches from Flashscore")
        return matches
    
    def _extract_flashscore_match(self, match_element) -> Dict:
        """Extract match data from Flashscore match element."""
        # Extract team names
        home_team_element = self.safe_find_element(By.CSS_SELECTOR, ".event__participant--home")
        away_team_element = self.safe_find_element(By.CSS_SELECTOR, ".event__participant--away")
        
        if not home_team_element or not away_team_element:
            return {}
        
        home_team = home_team_element.text.strip()
        away_team = away_team_element.text.strip()
        
        # Extract match time
        time_element = self.safe_find_element(By.CSS_SELECTOR, ".event__time")
        match_time = time_element.text.strip() if time_element else ""
        
        # Extract match status
        status_element = self.safe_find_element(By.CSS_SELECTOR, ".event__stage")
        status = status_element.text.strip() if status_element else ""
        
        return {
            'home_team': home_team,
            'away_team': away_team,
            'match_time': match_time,
            'status': status,
            'sport': self.sport,
            'site': self.site_name,
            'odds': {}  # Flashscore doesn't provide odds directly
        }
    
    def _scrape_tipsport(self) -> List[Dict]:
        """Scrape football matches from Tipsport."""
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
        
        scraper_logger.info(f"Scraped {len(matches)} football matches from Tipsport")
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
        
        # Extract odds (1X2 format for football)
        odds_elements = match_element.find_elements(By.CSS_SELECTOR, ".o-matchRow__odd")
        odds = {}
        
        if len(odds_elements) >= 3:
            home_odds = self.extract_odds(odds_elements[0].text)
            draw_odds = self.extract_odds(odds_elements[1].text)
            away_odds = self.extract_odds(odds_elements[2].text)
            
            if home_odds and draw_odds and away_odds:
                odds['1x2'] = {
                    'home': home_odds,
                    'draw': draw_odds,
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
        """Scrape football matches from Fortuna."""
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
        
        scraper_logger.info(f"Scraped {len(matches)} football matches from Fortuna")
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
        
        # Extract odds (1X2 format for football)
        odds_elements = match_element.find_elements(By.CSS_SELECTOR, ".market-odd")
        odds = {}
        
        if len(odds_elements) >= 3:
            home_odds = self.extract_odds(odds_elements[0].text)
            draw_odds = self.extract_odds(odds_elements[1].text)
            away_odds = self.extract_odds(odds_elements[2].text)
            
            if home_odds and draw_odds and away_odds:
                odds['1x2'] = {
                    'home': home_odds,
                    'draw': draw_odds,
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
        """Scrape football matches from Nike."""
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
        
        scraper_logger.info(f"Scraped {len(matches)} football matches from Nike")
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
        
        # Extract odds (1X2 format for football)
        odds_elements = match_element.find_elements(By.CSS_SELECTOR, ".odd-value")
        odds = {}
        
        if len(odds_elements) >= 3:
            home_odds = self.extract_odds(odds_elements[0].text)
            draw_odds = self.extract_odds(odds_elements[1].text)
            away_odds = self.extract_odds(odds_elements[2].text)
            
            if home_odds and draw_odds and away_odds:
                odds['1x2'] = {
                    'home': home_odds,
                    'draw': draw_odds,
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
