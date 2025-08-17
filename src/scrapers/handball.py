"""Handball scraper for betting sites."""

from typing import Dict, List
from selenium.webdriver.common.by import By
from src.scrapers.base import BaseScraper
from src.utils.logging import scraper_logger


class HandballScraper(BaseScraper):
    """Scraper for handball matches from betting sites."""
    
    def __init__(self, site_name: str, sport: str = 'handball'):
        super().__init__(site_name, sport)
    
    def scrape_matches(self, url: str) -> List[Dict]:
        """Scrape handball matches from the specified URL."""
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
                scraper_logger.warning(f"Unknown site: {self.site_name}")
                
        except Exception as e:
            scraper_logger.error(f"Error scraping {self.site_name}: {e}")
        
        scraper_logger.info(f"Scraped {len(matches)} handball matches from {self.site_name}")
        return matches
    
    def _scrape_tipsport(self) -> List[Dict]:
        """Scrape handball matches from Tipsport."""
        matches = []
        
        try:
            # Handle cookie consent
            self.handle_cookie_consent()
            
            # Wait for matches to load
            match_elements = self.wait_for_elements(By.CSS_SELECTOR, ".o-matchRow")
            
            for match_element in match_elements:
                match_data = self._extract_tipsport_match(match_element)
                if match_data:
                    matches.append(match_data)
                    
        except Exception as e:
            scraper_logger.error(f"Error scraping Tipsport handball: {e}")
            
        return matches
    
    def _scrape_fortuna(self) -> List[Dict]:
        """Scrape handball matches from Fortuna."""
        matches = []
        
        try:
            # Handle cookie consent
            self.handle_cookie_consent()
            
            # Wait for matches to load
            match_elements = self.wait_for_elements(By.CSS_SELECTOR, ".market")
            
            for match_element in match_elements:
                match_data = self._extract_fortuna_match(match_element)
                if match_data:
                    matches.append(match_data)
                    
        except Exception as e:
            scraper_logger.error(f"Error scraping Fortuna handball: {e}")
            
        return matches
    
    def _scrape_nike(self) -> List[Dict]:
        """Scrape handball matches from Nike."""
        matches = []
        
        try:
            # Handle cookie consent
            self.handle_cookie_consent()
            
            # Wait for matches to load
            match_elements = self.wait_for_elements(By.CSS_SELECTOR, ".event-row")
            
            for match_element in match_elements:
                match_data = self._extract_nike_match(match_element)
                if match_data:
                    matches.append(match_data)
                    
        except Exception as e:
            scraper_logger.error(f"Error scraping Nike handball: {e}")
            
        return matches
    
    def _extract_tipsport_match(self, match_element) -> Dict:
        """Extract match data from Tipsport match element."""
        try:
            # Extract team names
            team_element = self.safe_find_element(By.CSS_SELECTOR, ".o-matchRow__participantNames", match_element)
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
            time_element = self.safe_find_element(By.CSS_SELECTOR, ".o-matchRow__time", match_element)
            match_time = time_element.text.strip() if time_element else ""
            
            # Extract odds (1X2 format for handball)
            odds_elements = match_element.find_elements(By.CSS_SELECTOR, ".o-matchRow__odd")
            odds = {}
            
            if len(odds_elements) >= 3:
                home_odds = self.extract_odds(odds_elements[0].text)
                draw_odds = self.extract_odds(odds_elements[1].text)
                away_odds = self.extract_odds(odds_elements[2].text)
                
                if home_odds and draw_odds and away_odds:
                    odds = {
                        'home': home_odds,
                        'draw': draw_odds,
                        'away': away_odds
                    }
            
            if not odds:
                return {}
            
            return {
                'home_team': self.normalize_team_name(home_team),
                'away_team': self.normalize_team_name(away_team),
                'match_time': match_time,
                'odds': odds,
                'site': self.site_name,
                'sport': self.sport,
                'bet_type': '1X2'
            }
            
        except Exception as e:
            scraper_logger.error(f"Error extracting Tipsport handball match: {e}")
            return {}
    
    def _extract_fortuna_match(self, match_element) -> Dict:
        """Extract match data from Fortuna match element."""
        try:
            # Extract team names
            team_element = self.safe_find_element(By.CSS_SELECTOR, ".market-name", match_element)
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
            time_element = self.safe_find_element(By.CSS_SELECTOR, ".market-time", match_element)
            match_time = time_element.text.strip() if time_element else ""
            
            # Extract odds (1X2 format for handball)
            odds_elements = match_element.find_elements(By.CSS_SELECTOR, ".market-odd")
            odds = {}
            
            if len(odds_elements) >= 3:
                home_odds = self.extract_odds(odds_elements[0].text)
                draw_odds = self.extract_odds(odds_elements[1].text)
                away_odds = self.extract_odds(odds_elements[2].text)
                
                if home_odds and draw_odds and away_odds:
                    odds = {
                        'home': home_odds,
                        'draw': draw_odds,
                        'away': away_odds
                    }
            
            if not odds:
                return {}
            
            return {
                'home_team': self.normalize_team_name(home_team),
                'away_team': self.normalize_team_name(away_team),
                'match_time': match_time,
                'odds': odds,
                'site': self.site_name,
                'sport': self.sport,
                'bet_type': '1X2'
            }
            
        except Exception as e:
            scraper_logger.error(f"Error extracting Fortuna handball match: {e}")
            return {}
    
    def _extract_nike_match(self, match_element) -> Dict:
        """Extract match data from Nike match element."""
        try:
            # Extract team names
            team_element = self.safe_find_element(By.CSS_SELECTOR, ".event-name", match_element)
            if not team_element:
                return {}
            
            team_text = team_element.text.strip()
            if ' vs ' in team_text:
                teams = team_text.split(' vs ')
                home_team = teams[0].strip()
                away_team = teams[1].strip()
            else:
                return {}
            
            # Extract match time
            time_element = self.safe_find_element(By.CSS_SELECTOR, ".event-time", match_element)
            match_time = time_element.text.strip() if time_element else ""
            
            # Extract odds (1X2 format for handball)
            odds_elements = match_element.find_elements(By.CSS_SELECTOR, ".odd-value")
            odds = {}
            
            if len(odds_elements) >= 3:
                home_odds = self.extract_odds(odds_elements[0].text)
                draw_odds = self.extract_odds(odds_elements[1].text)
                away_odds = self.extract_odds(odds_elements[2].text)
                
                if home_odds and draw_odds and away_odds:
                    odds = {
                        'home': home_odds,
                        'draw': draw_odds,
                        'away': away_odds
                    }
            
            if not odds:
                return {}
            
            return {
                'home_team': self.normalize_team_name(home_team),
                'away_team': self.normalize_team_name(away_team),
                'match_time': match_time,
                'odds': odds,
                'site': self.site_name,
                'sport': self.sport,
                'bet_type': '1X2'
            }
            
        except Exception as e:
            scraper_logger.error(f"Error extracting Nike handball match: {e}")
            return {}
