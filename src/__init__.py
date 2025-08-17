"""
Flashscore Sports Betting Arbitrage Detection System

A comprehensive system for monitoring Slovak betting sites and detecting arbitrage opportunities.
"""

__version__ = "1.0.0"
__author__ = "Christian Szeman"
__description__ = "Sports betting arbitrage detection system"

from .config import config
from .main import FlashscoreApp

__all__ = ['config', 'FlashscoreApp']
