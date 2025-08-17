"""Scraper modules for different betting sites and sports."""

from .base import BaseScraper
from .basketball import BasketballScraper
from .football import FootballScraper
from .tennis import TennisScraper
from .volleyball import VolleyballScraper
from .hockey import HockeyScraper
from .handball import HandballScraper

__all__ = [
    'BaseScraper',
    'BasketballScraper',
    'FootballScraper', 
    'TennisScraper',
    'VolleyballScraper',
    'HockeyScraper',
    'HandballScraper'
]
