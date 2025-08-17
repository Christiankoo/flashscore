#!/usr/bin/env python3
"""
Flashscore Sports Betting Arbitrage Detection System

Main entry point for the application with CLI interface.
"""

import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict

from src.config import config
from src.core import arbitrage_calculator, notification_manager
from src.utils.logging import main_logger
from src.scrapers.basketball import BasketballScraper
from src.scrapers.football import FootballScraper
from src.scrapers.tennis import TennisScraper
from src.scrapers.volleyball import VolleyballScraper
from src.scrapers.hockey import HockeyScraper
from src.scrapers.handball import HandballScraper
from src.data.match_tracker import MatchTracker


class FlashscoreApp:
    """Main application class."""
    
    def __init__(self):
        self.match_tracker = MatchTracker()
        self.scrapers = {
            'basketball': BasketballScraper,
            'football': FootballScraper,
            'tennis': TennisScraper,
            'volleyball': VolleyballScraper,
            'hockey': HockeyScraper,
            'handball': HandballScraper
        }
    
    def run_sport_analysis(self, sport: str, time_period: str = 'today') -> List[Dict]:
        """Run arbitrage analysis for a specific sport."""
        main_logger.info(f"Starting {sport} analysis for {time_period}")
        
        if sport not in self.scrapers:
            main_logger.error(f"Unsupported sport: {sport}")
            return []
        
        scraper_class = self.scrapers[sport]
        all_matches = []
        
        # Get URLs for the sport and time period
        sport_config = config.betting_sites.get(sport, {})
        urls = self._get_urls_for_period(sport_config.base_urls, time_period)
        
        # Scrape all betting sites concurrently
        with ThreadPoolExecutor(max_workers=config.scraping.cpu_count) as executor:
            futures = []
            
            for site_name, url in urls.items():
                scraper = scraper_class(site_name, sport)
                future = executor.submit(self._scrape_site, scraper, url)
                futures.append((site_name, future))
            
            # Collect results
            for site_name, future in futures:
                try:
                    matches = future.result(timeout=300)  # 5 minute timeout
                    all_matches.extend(matches)
                    main_logger.info(f"Scraped {len(matches)} matches from {site_name}")
                except Exception as e:
                    main_logger.error(f"Failed to scrape {site_name}: {e}")
        
        # Find arbitrage opportunities
        opportunities = arbitrage_calculator.find_arbitrage_opportunities(all_matches)
        
        # Filter out already processed opportunities
        new_opportunities = self.match_tracker.filter_new_opportunities(opportunities)
        
        # Send notifications for new opportunities
        for opportunity in new_opportunities:
            try:
                notification_manager.send_arbitrage_alert(opportunity)
                self.match_tracker.mark_opportunity_sent(opportunity)
            except Exception as e:
                main_logger.error(f"Failed to send notification: {e}")
        
        main_logger.info(f"Found {len(opportunities)} total opportunities, {len(new_opportunities)} new")
        return new_opportunities
    
    def _get_urls_for_period(self, base_urls: Dict[str, str], time_period: str) -> Dict[str, str]:
        """Get URLs filtered by time period."""
        if time_period == 'today':
            return {k: v for k, v in base_urls.items() if 'tomorrow' not in k}
        elif time_period == 'tomorrow':
            return {k: v for k, v in base_urls.items() if 'tomorrow' in k}
        else:
            return base_urls
    
    def _scrape_site(self, scraper, url: str) -> List[Dict]:
        """Scrape a single betting site."""
        try:
            with scraper:
                return scraper.scrape_matches(url)
        except Exception as e:
            main_logger.error(f"Error scraping {scraper.site_name}: {e}")
            return []
    
    def run_continuous_monitoring(self, sports: List[str], interval_minutes: int = 30):
        """Run continuous monitoring for specified sports."""
        import time
        
        main_logger.info(f"Starting continuous monitoring for {sports} (interval: {interval_minutes}min)")
        
        while True:
            try:
                for sport in sports:
                    self.run_sport_analysis(sport, 'today')
                    self.run_sport_analysis(sport, 'tomorrow')
                
                main_logger.info(f"Monitoring cycle completed. Sleeping for {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                main_logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                main_logger.error(f"Error in monitoring cycle: {e}")
                time.sleep(60)  # Wait 1 minute before retrying


def create_cli_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Flashscore Sports Betting Arbitrage Detection System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --sport basketball --period today
  %(prog)s --sport football --period tomorrow
  %(prog)s --monitor basketball football --interval 30
  %(prog)s --list-sports
        """
    )
    
    parser.add_argument(
        '--sport',
        choices=['basketball', 'football', 'tennis', 'volleyball', 'hockey', 'handball'],
        help='Sport to analyze'
    )
    
    parser.add_argument(
        '--period',
        choices=['today', 'tomorrow', 'both'],
        default='today',
        help='Time period to analyze (default: today)'
    )
    
    parser.add_argument(
        '--monitor',
        nargs='+',
        choices=['basketball', 'football', 'tennis', 'volleyball', 'hockey', 'handball'],
        help='Sports to monitor continuously'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=30,
        help='Monitoring interval in minutes (default: 30)'
    )
    
    parser.add_argument(
        '--list-sports',
        action='store_true',
        help='List available sports'
    )
    
    parser.add_argument(
        '--config-test',
        action='store_true',
        help='Test configuration and connections'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser


def test_configuration():
    """Test system configuration and connections."""
    main_logger.info("Testing system configuration...")
    
    # Test Telegram connection
    try:
        success = notification_manager.send_telegram_message("🧪 Configuration test message")
        if success:
            main_logger.info("✅ Telegram connection: OK")
        else:
            main_logger.error("❌ Telegram connection: FAILED")
    except Exception as e:
        main_logger.error(f"❌ Telegram connection error: {e}")
    
    # Test AWS Lambda connection
    try:
        success = notification_manager.send_aws_lambda_notification({
            'type': 'config_test',
            'message': 'Configuration test'
        })
        if success:
            main_logger.info("✅ AWS Lambda connection: OK")
        else:
            main_logger.error("❌ AWS Lambda connection: FAILED")
    except Exception as e:
        main_logger.error(f"❌ AWS Lambda connection error: {e}")
    
    main_logger.info("Configuration test completed")


def main():
    """Main entry point."""
    parser = create_cli_parser()
    args = parser.parse_args()
    
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    app = FlashscoreApp()
    
    try:
        if args.list_sports:
            print("Available sports:")
            for sport in app.scrapers.keys():
                print(f"  - {sport}")
            return 0
        
        if args.config_test:
            test_configuration()
            return 0
        
        if args.monitor:
            app.run_continuous_monitoring(args.monitor, args.interval)
            return 0
        
        if args.sport:
            if args.period == 'both':
                periods = ['today', 'tomorrow']
            else:
                periods = [args.period]
            
            total_opportunities = 0
            for period in periods:
                opportunities = app.run_sport_analysis(args.sport, period)
                total_opportunities += len(opportunities)
            
            print(f"Analysis completed. Found {total_opportunities} arbitrage opportunities.")
            return 0
        
        # No specific command provided
        parser.print_help()
        return 1
        
    except KeyboardInterrupt:
        main_logger.info("Application interrupted by user")
        return 0
    except Exception as e:
        main_logger.error(f"Application error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
