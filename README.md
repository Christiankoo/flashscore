# Flashscore Sports Betting Arbitrage Detection System

A comprehensive, production-ready system for monitoring multiple Slovak betting sites to identify profitable arbitrage opportunities in sports betting.

## Overview

This system automatically scrapes odds from major Slovak betting platforms (Tipsport, Fortuna, Nike) and uses mathematical analysis to detect arbitrage opportunities where the combined inverse odds guarantee profit regardless of match outcome.

## Architecture

### Project Structure
```
flashscore/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Main entry point with CLI
│   ├── config.py              # Centralized configuration
│   ├── core/                  # Core business logic
│   │   ├── __init__.py
│   │   ├── arbitrage.py       # Arbitrage calculation engine
│   │   ├── driver.py          # WebDriver management
│   │   └── notifications.py   # Notification system
│   ├── scrapers/              # Site-specific scrapers
│   │   ├── __init__.py
│   │   ├── base.py           # Base scraper class
│   │   ├── basketball.py     # Basketball scraper
│   │   ├── football.py       # Football scraper
│   │   ├── tennis.py         # Tennis scraper
│   │   ├── volleyball.py     # Volleyball scraper
│   │   ├── hockey.py         # Hockey scraper
│   │   └── handball.py       # Handball scraper
│   ├── data/                 # Data management
│   │   ├── __init__.py
│   │   └── match_tracker.py  # Match tracking & deduplication
│   └── utils/                # Utilities
│       ├── __init__.py
│       └── logging.py        # Logging configuration
├── data/                     # Data storage
├── logs/                     # Log files
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Multi-service orchestration
└── README.md               # This file
```

### Key Components

- **Arbitrage Engine**: Mathematical calculations for different bet types (1X2, Over/Under, Asian Handicap)
- **Web Scrapers**: Selenium-based scrapers for each betting site with error handling
- **Notification System**: Telegram bot and AWS Lambda integration for real-time alerts
- **Docker Integration**: Containerized deployment with VPN support
- **Match Tracking**: Deduplication system to prevent duplicate alerts

## Quick Start

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- NordVPN credentials (for VPN container)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd flashscore
```

2. **Set up environment variables**
```bash
# Create .env file
echo "NORDVPN_USER=your_nordvpn_username" > .env
echo "NORDVPN_PASSWORD=your_nordvpn_password" >> .env
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Usage

#### Command Line Interface

```bash
# Analyze basketball matches for today
python src/main.py --sport basketball --period today

# Monitor multiple sports continuously
python src/main.py --monitor basketball football --interval 30

# Test configuration
python src/main.py --config-test

# List available sports
python src/main.py --list-sports
```

#### Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# Start specific sport monitoring
docker-compose up flashscore-basketball

# Multi-sport monitoring
docker-compose --profile multi-sport up flashscore-multi
```

## Configuration

### Main Configuration (`src/config.py`)

- **Telegram Bot**: Configure token and chat ID for notifications
- **AWS Lambda**: Webhook URL for additional notifications  
- **Scraping Settings**: Timeouts, CPU count, profit thresholds
- **Betting Sites**: URLs and endpoints for each sport
- **Match Filters**: Regex patterns to exclude completed/invalid matches

### Environment Variables

- `NORDVPN_USER`: NordVPN username
- `NORDVPN_PASSWORD`: NordVPN password

## Sports Supported

- **Basketball** (`basketbal_new/`)
- **Football** (`futbalhokej/`, `futbaltenis_new/`)
- **Tennis** (`futbaltenis_new/`, `tenisbasketbal/`)
- **Volleyball** (`volejbalhadzana/`)
- **Hockey** (`futbalhokej/`)
- **Handball** (`handbal_new/`)

## Arbitrage Calculations

The system implements several arbitrage calculation methods:

### 1X2 Betting
```python
inverse_sum = (1/home_odds) + (1/draw_odds) + (1/away_odds)
if inverse_sum < 1:
    profit_margin = ((1 - inverse_sum) / inverse_sum) * 100
```

### Over/Under Betting
```python
inverse_sum = (1/over_odds) + (1/under_odds)
if inverse_sum < 1:
    profit_margin = ((1 - inverse_sum) / inverse_sum) * 100
```

### Asian Handicap
```python
inverse_sum = (1/home_handicap_odds) + (1/away_handicap_odds)
if inverse_sum < 1:
    profit_margin = ((1 - inverse_sum) / inverse_sum) * 100
```

## Notifications

### Telegram Bot
- Real-time alerts for arbitrage opportunities
- System status notifications
- Error alerts

### AWS Lambda
- Webhook integration for additional processing
- Data backup and analytics

## Docker Services

### VPN Service
- **Image**: `qmcgaw/gluetun`
- **Provider**: NordVPN
- **Region**: Slovakia
- **Purpose**: Ensures all scraping traffic goes through Slovak VPN

### Sport-Specific Services
- `flashscore-basketball`: Monitors basketball matches
- `flashscore-football`: Monitors football matches  
- `flashscore-tennis`: Monitors tennis matches
- `flashscore-volleyball`: Monitors volleyball matches
- `flashscore-hockey`: Monitors hockey matches
- `flashscore-handball`: Monitors handball matches
- `flashscore-multi`: Multi-sport monitoring (optional)

## Monitoring & Logging

### Log Files
- `logs/scraper.log`: Web scraping activities
- `logs/arbitrage.log`: Arbitrage calculations
- `logs/notification.log`: Notification sending
- `logs/main.log`: Main application events

### Health Checks
```bash
# Test system configuration
python src/main.py --config-test

# Check container status
docker-compose ps

# View logs
docker-compose logs flashscore-basketball
```

## Development

### Adding New Sports
1. Create scraper class inheriting from `BaseScraper`
2. Implement `scrape_matches()` method
3. Add sport configuration to `config.py`
4. Register scraper in `main.py`

### Adding New Betting Sites
1. Extend existing sport scrapers
2. Add site URLs to configuration
3. Implement site-specific parsing logic

## Security Considerations

- **VPN Usage**: All traffic routed through NordVPN
- **Credential Management**: Use environment variables
- **Container Security**: Seccomp profiles for syscall filtering
- **Rate Limiting**: Built-in delays and retry logic

## Performance

- **Concurrent Scraping**: Multi-threaded scraping across sites
- **Resource Management**: Configurable CPU usage limits
- **Memory Optimization**: Efficient pandas DataFrame operations
- **Caching**: Match deduplication to prevent redundant processing

## Troubleshooting

### Common Issues

1. **ChromeDriver Issues**
   ```bash
   # Update ChromeDriver in Dockerfile
   RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`
   ```

2. **VPN Connection Problems**
   ```bash
   # Check VPN container logs
   docker-compose logs vpn
   ```

3. **Notification Failures**
   ```bash
   # Test notifications
   python src/main.py --config-test
   ```

### Debug Mode
```bash
# Enable verbose logging
python src/main.py --sport basketball --verbose
```

## Maintenance

### Automated Tasks (Cron)
- **Hourly**: Cache updates (`cache.sh`)
- **Every 4 hours**: Service restarts (`restart.sh`)

### Manual Maintenance
```bash
# Clean up old logs
find logs/ -name "*.log" -mtime +7 -delete

# Update dependencies
pip install -r requirements.txt --upgrade

# Rebuild containers
docker-compose build --no-cache
```

## License

This project is for educational and research purposes. Please ensure compliance with betting site terms of service and local regulations.

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## Support

For issues and questions:
- Check logs in `logs/` directory
- Run configuration test: `python src/main.py --config-test`
- Review Docker container status: `docker-compose ps`