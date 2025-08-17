"""Arbitrage calculation engine for sports betting."""

from typing import Dict, List, Tuple, Optional
import pandas as pd
from src.utils.logging import arbitrage_logger
from src.config import config


class ArbitrageCalculator:
    """Handles arbitrage calculations for different bet types."""
    
    @staticmethod
    def calculate_1x2_double_chance(odds_data: Dict) -> Optional[Dict]:
        """Calculate arbitrage for 1X2 and double chance betting."""
        try:
            # Extract odds
            home_odds = float(odds_data.get('home', 0))
            draw_odds = float(odds_data.get('draw', 0))
            away_odds = float(odds_data.get('away', 0))
            
            if not all([home_odds, draw_odds, away_odds]):
                return None
            
            # Calculate inverse odds sum
            inverse_sum = (1/home_odds) + (1/draw_odds) + (1/away_odds)
            
            if inverse_sum < 1:
                profit_margin = ((1 - inverse_sum) / inverse_sum) * 100
                
                if profit_margin >= config.scraping.profit_threshold:
                    return {
                        'type': '1X2',
                        'profit_margin': profit_margin,
                        'home_odds': home_odds,
                        'draw_odds': draw_odds,
                        'away_odds': away_odds,
                        'inverse_sum': inverse_sum
                    }
            
            return None
            
        except (ValueError, ZeroDivisionError) as e:
            arbitrage_logger.error(f"Error calculating 1X2 arbitrage: {e}")
            return None
    
    @staticmethod
    def calculate_over_under(odds_data: Dict) -> Optional[Dict]:
        """Calculate arbitrage for Over/Under betting."""
        try:
            over_odds = float(odds_data.get('over', 0))
            under_odds = float(odds_data.get('under', 0))
            
            if not all([over_odds, under_odds]):
                return None
            
            inverse_sum = (1/over_odds) + (1/under_odds)
            
            if inverse_sum < 1:
                profit_margin = ((1 - inverse_sum) / inverse_sum) * 100
                
                if profit_margin >= config.scraping.profit_threshold:
                    return {
                        'type': 'Over/Under',
                        'profit_margin': profit_margin,
                        'over_odds': over_odds,
                        'under_odds': under_odds,
                        'inverse_sum': inverse_sum
                    }
            
            return None
            
        except (ValueError, ZeroDivisionError) as e:
            arbitrage_logger.error(f"Error calculating Over/Under arbitrage: {e}")
            return None
    
    @staticmethod
    def calculate_asian_handicap(odds_data: Dict) -> Optional[Dict]:
        """Calculate arbitrage for Asian Handicap betting."""
        try:
            home_odds = float(odds_data.get('home_handicap', 0))
            away_odds = float(odds_data.get('away_handicap', 0))
            handicap = odds_data.get('handicap', 0)
            
            if not all([home_odds, away_odds]):
                return None
            
            inverse_sum = (1/home_odds) + (1/away_odds)
            
            if inverse_sum < 1:
                profit_margin = ((1 - inverse_sum) / inverse_sum) * 100
                
                if profit_margin >= config.scraping.profit_threshold:
                    return {
                        'type': 'Asian Handicap',
                        'profit_margin': profit_margin,
                        'home_odds': home_odds,
                        'away_odds': away_odds,
                        'handicap': handicap,
                        'inverse_sum': inverse_sum
                    }
            
            return None
            
        except (ValueError, ZeroDivisionError) as e:
            arbitrage_logger.error(f"Error calculating Asian Handicap arbitrage: {e}")
            return None
    
    @staticmethod
    def calculate_home_away(odds_data: Dict) -> Optional[Dict]:
        """Calculate arbitrage for Home/Away betting."""
        try:
            home_odds = float(odds_data.get('home', 0))
            away_odds = float(odds_data.get('away', 0))
            
            if not all([home_odds, away_odds]):
                return None
            
            inverse_sum = (1/home_odds) + (1/away_odds)
            
            if inverse_sum < 1:
                profit_margin = ((1 - inverse_sum) / inverse_sum) * 100
                
                if profit_margin >= config.scraping.profit_threshold:
                    return {
                        'type': 'Home/Away',
                        'profit_margin': profit_margin,
                        'home_odds': home_odds,
                        'away_odds': away_odds,
                        'inverse_sum': inverse_sum
                    }
            
            return None
            
        except (ValueError, ZeroDivisionError) as e:
            arbitrage_logger.error(f"Error calculating Home/Away arbitrage: {e}")
            return None
    
    def find_arbitrage_opportunities(self, matches_data: List[Dict]) -> List[Dict]:
        """Find all arbitrage opportunities in the provided matches data."""
        opportunities = []
        
        for match in matches_data:
            # Try different bet types
            for bet_type, odds_data in match.get('odds', {}).items():
                if bet_type == '1x2':
                    result = self.calculate_1x2_double_chance(odds_data)
                elif bet_type == 'over_under':
                    result = self.calculate_over_under(odds_data)
                elif bet_type == 'asian_handicap':
                    result = self.calculate_asian_handicap(odds_data)
                elif bet_type == 'home_away':
                    result = self.calculate_home_away(odds_data)
                else:
                    continue
                
                if result:
                    result.update({
                        'match_id': match.get('id'),
                        'home_team': match.get('home_team'),
                        'away_team': match.get('away_team'),
                        'match_time': match.get('match_time'),
                        'sport': match.get('sport')
                    })
                    opportunities.append(result)
        
        return opportunities


# Global arbitrage calculator instance
arbitrage_calculator = ArbitrageCalculator()
