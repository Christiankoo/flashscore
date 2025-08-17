"""Configuration management for the flashscore system."""

import os
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime, timedelta


@dataclass
class TelegramConfig:
    """Telegram bot configuration."""
    token: str = "5717884327:AAG1XYqDvCJMB1cpE3PlnjipwZv2rzOS8ns"
    chat_id: str = "-1001695455818"


@dataclass
class AWSConfig:
    """AWS Lambda configuration."""
    lambda_url: str = "https://cdyvrd8716.execute-api.eu-central-1.amazonaws.com/dev/new"


@dataclass
class ScrapingConfig:
    """Web scraping configuration."""
    cpu_count: int = 4
    request_timeout: int = 20
    max_wait_time: int = 60
    profit_threshold: float = 1.0  # Minimum profit percentage to trigger alerts


@dataclass
class BettingSiteConfig:
    """Configuration for betting sites."""
    base_urls: Dict[str, str]
    endpoints: Dict[str, Dict[str, str]]


class Config:
    """Main configuration class."""
    
    def __init__(self):
        self.telegram = TelegramConfig()
        self.aws = AWSConfig()
        self.scraping = ScrapingConfig()
        
        # Date configuration
        today = datetime.today().strftime('%Y-%m-%d')
        tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Betting site configurations
        self.betting_sites = {
            'basketball': BettingSiteConfig(
                base_urls={
                    'fortuna': f'https://www.ifortuna.sk/stavkovanie/basketbal?selectDates=1&date={today}',
                    'fortuna_tomorrow': f'https://www.ifortuna.sk/stavkovanie/basketbal?selectDates=1&date={tomorrow}',
                    'nike': 'https://www.nike.sk/tipovanie/basketbal?dnes',
                    'nike_tomorrow': 'https://www.nike.sk/tipovanie/basketbal?zajtra',
                    'tipsport': 'https://www.tipsport.sk/kurzy/basketbal-7?timeFilter=form.period.today&limit=1000',
                    'tipsport_tomorrow': 'https://www.tipsport.sk/kurzy/basketbal-7?timeFilter=form.period.tomorrow&limit=1000',
                    'flashscore': 'https://www.flashscore.sk/basketbal/'
                },
                endpoints={}
            ),
            'football': BettingSiteConfig(
                base_urls={
                    'fortuna': f'https://www.ifortuna.sk/stavkovanie/futbal?selectDates=1&date={today}',
                    'fortuna_tomorrow': f'https://www.ifortuna.sk/stavkovanie/futbal?selectDates=1&date={tomorrow}',
                    'nike': 'https://www.nike.sk/tipovanie/futbal?dnes',
                    'nike_tomorrow': 'https://www.nike.sk/tipovanie/futbal?zajtra',
                    'tipsport': 'https://www.tipsport.sk/kurzy/futbal-1?timeFilter=form.period.today&limit=1000',
                    'tipsport_tomorrow': 'https://www.tipsport.sk/kurzy/futbal-1?timeFilter=form.period.tomorrow&limit=1000',
                    'flashscore': 'https://www.flashscore.sk/futbal/'
                },
                endpoints={}
            ),
            'tennis': BettingSiteConfig(
                base_urls={
                    'fortuna': f'https://www.ifortuna.sk/stavkovanie/tenis?selectDates=1&date={today}',
                    'fortuna_tomorrow': f'https://www.ifortuna.sk/stavkovanie/tenis?selectDates=1&date={tomorrow}',
                    'nike': 'https://www.nike.sk/tipovanie/tenis?dnes',
                    'nike_tomorrow': 'https://www.nike.sk/tipovanie/tenis?zajtra',
                    'tipsport': 'https://www.tipsport.sk/kurzy/tenis-2?timeFilter=form.period.today&limit=1000',
                    'tipsport_tomorrow': 'https://www.tipsport.sk/kurzy/tenis-2?timeFilter=form.period.tomorrow&limit=1000',
                },
                endpoints={}
            ),
            'volleyball': BettingSiteConfig(
                base_urls={
                    'fortuna': f'https://www.ifortuna.sk/stavkovanie/volejbal?selectDates=1&date={today}',
                    'fortuna_tomorrow': f'https://www.ifortuna.sk/stavkovanie/volejbal?selectDates=1&date={tomorrow}',
                    'nike': 'https://www.nike.sk/tipovanie/volejbal?dnes',
                    'nike_tomorrow': 'https://www.nike.sk/tipovanie/volejbal?zajtra',
                    'tipsport': 'https://www.tipsport.sk/kurzy/volejbal-9?timeFilter=form.period.today&limit=1000',
                    'tipsport_tomorrow': 'https://www.tipsport.sk/kurzy/volejbal-9?timeFilter=form.period.tomorrow&limit=1000',
                },
                endpoints={}
            ),
            'hockey': BettingSiteConfig(
                base_urls={
                    'fortuna': f'https://www.ifortuna.sk/stavkovanie/hokej?selectDates=1&date={today}',
                    'fortuna_tomorrow': f'https://www.ifortuna.sk/stavkovanie/hokej?selectDates=1&date={tomorrow}',
                    'nike': 'https://www.nike.sk/tipovanie/hokej?dnes',
                    'nike_tomorrow': 'https://www.nike.sk/tipovanie/hokej?zajtra',
                    'tipsport': 'https://www.tipsport.sk/kurzy/hokej-3?timeFilter=form.period.today&limit=1000',
                    'tipsport_tomorrow': 'https://www.tipsport.sk/kurzy/hokej-3?timeFilter=form.period.tomorrow&limit=1000',
                },
                endpoints={}
            ),
            'handball': BettingSiteConfig(
                base_urls={
                    'fortuna': f'https://www.ifortuna.sk/stavkovanie/hadzana?selectDates=1&date={today}',
                    'fortuna_tomorrow': f'https://www.ifortuna.sk/stavkovanie/hadzana?selectDates=1&date={tomorrow}',
                    'nike': 'https://www.nike.sk/tipovanie/hadzana?dnes',
                    'nike_tomorrow': 'https://www.nike.sk/tipovanie/hadzana?zajtra',
                    'tipsport': 'https://www.tipsport.sk/kurzy/hadzana-8?timeFilter=form.period.today&limit=1000',
                    'tipsport_tomorrow': 'https://www.tipsport.sk/kurzy/hadzana-8?timeFilter=form.period.tomorrow&limit=1000',
                },
                endpoints={}
            )
        }
        
        # Sport-specific configurations
        self.sport_mappings = {
            'basketball': {
                'time_periods': {
                    'first_half': ['1.polčas', '1. polčas', '1.pol', '1. pol', '1. polčasu', '1.polčasu', '1. polčase', '1.polčase'],
                    'second_half': ['2.polčas', '2. polčas', '2.pol', '2. pol', '2. polčasu', '2.polčasu', '2. polčase', '2.polčasu'],
                    'first_quarter': ['1. štvrtiny', '1. štvrtina', '1. štvrtine', '1.štvrtiny', '1.štvrtina', '1.štvrtine']
                },
                'bet_categories': {
                    'tipsport': {
                        'Víťaz zápasu': 'Víťaz zápasu',
                        '1X2': '1X2',
                        'Počet bodov': 'Počet bodov',
                        'Handicap': 'Handicap',
                    },
                    'fortuna': {
                        'Víťaz': 'Víťaz',
                        'Celkový počet bodov': 'Celkový počet bodov',
                    }
                }
            },
            'football': {
                'bet_categories': {
                    'tipsport': {
                        'Víťaz zápasu': 'Víťaz zápasu',
                        '1X2': '1X2',
                        'Počet gólov': 'Počet gólov',
                        'Handicap': 'Handicap',
                    }
                }
            },
            'tennis': {
                'bet_categories': {
                    'tipsport': {
                        'Víťaz zápasu': 'Víťaz zápasu',
                        'Počet setov': 'Počet setov',
                        'Handicap': 'Handicap',
                    }
                }
            },
            'volleyball': {
                'bet_categories': {
                    'tipsport': {
                        'Víťaz zápasu': 'Víťaz zápasu',
                        'Počet setov': 'Počet setov',
                        'Handicap': 'Handicap',
                    }
                }
            },
            'hockey': {
                'bet_categories': {
                    'tipsport': {
                        'Víťaz zápasu': 'Víťaz zápasu',
                        '1X2': '1X2',
                        'Počet gólov': 'Počet gólov',
                        'Handicap': 'Handicap',
                    }
                }
            }
        }
        
        # Excluded bookmakers
        self.excluded_bookmakers = ['Unibet', 'bet365']
        
        # Match status filters (regex patterns)
        self.match_status_filters = [
            "Koniec.*",
            "Postup bez boja.*", 
            "Zrušené.*",
            "[0-9]. set.*",
            "[0-9]. štvrtina.*",
            "Live.*",
            "Prestávka.*",
            "Čakáme aktualizáciu.*",
            "Odložené.*",
            "Po predĺžení.*",
            "Predĺženie.*"
        }


# Global configuration instance
config = Config()
