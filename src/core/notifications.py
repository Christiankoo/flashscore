"""Notification system for sending alerts about arbitrage opportunities."""

import requests
from typing import Dict, List, Optional
from src.config import config
from src.utils.logging import notification_logger


class NotificationManager:
    """Handles sending notifications via various channels."""
    
    def __init__(self):
        self.telegram_config = config.telegram
        self.aws_config = config.aws
    
    def send_telegram_message(self, message: str) -> bool:
        """Send message via Telegram bot."""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_config.token}/sendMessage"
            payload = {
                'chat_id': self.telegram_config.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            notification_logger.info("Telegram message sent successfully")
            return True
            
        except requests.RequestException as e:
            notification_logger.error(f"Failed to send Telegram message: {e}")
            return False
    
    def send_aws_lambda_notification(self, data: Dict) -> bool:
        """Send notification via AWS Lambda webhook."""
        try:
            response = requests.post(
                self.aws_config.lambda_url,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            
            notification_logger.info("AWS Lambda notification sent successfully")
            return True
            
        except requests.RequestException as e:
            notification_logger.error(f"Failed to send AWS Lambda notification: {e}")
            return False
    
    def format_arbitrage_message(self, opportunity: Dict) -> str:
        """Format arbitrage opportunity into a readable message."""
        message_parts = [
            f"🚨 <b>Arbitrage Opportunity Found!</b>",
            f"",
            f"<b>Match:</b> {opportunity.get('home_team', 'N/A')} vs {opportunity.get('away_team', 'N/A')}",
            f"<b>Sport:</b> {opportunity.get('sport', 'N/A')}",
            f"<b>Time:</b> {opportunity.get('match_time', 'N/A')}",
            f"<b>Bet Type:</b> {opportunity.get('type', 'N/A')}",
            f"<b>Profit Margin:</b> {opportunity.get('profit_margin', 0):.2f}%",
            f""
        ]
        
        # Add odds information based on bet type
        bet_type = opportunity.get('type', '')
        
        if bet_type == '1X2':
            message_parts.extend([
                f"<b>Odds:</b>",
                f"• Home: {opportunity.get('home_odds', 'N/A')}",
                f"• Draw: {opportunity.get('draw_odds', 'N/A')}",
                f"• Away: {opportunity.get('away_odds', 'N/A')}"
            ])
        elif bet_type == 'Over/Under':
            message_parts.extend([
                f"<b>Odds:</b>",
                f"• Over: {opportunity.get('over_odds', 'N/A')}",
                f"• Under: {opportunity.get('under_odds', 'N/A')}"
            ])
        elif bet_type == 'Asian Handicap':
            message_parts.extend([
                f"<b>Odds:</b>",
                f"• Home ({opportunity.get('handicap', 'N/A')}): {opportunity.get('home_odds', 'N/A')}",
                f"• Away: {opportunity.get('away_odds', 'N/A')}"
            ])
        elif bet_type == 'Home/Away':
            message_parts.extend([
                f"<b>Odds:</b>",
                f"• Home: {opportunity.get('home_odds', 'N/A')}",
                f"• Away: {opportunity.get('away_odds', 'N/A')}"
            ])
        
        return "\n".join(message_parts)
    
    def send_arbitrage_alert(self, opportunity: Dict) -> bool:
        """Send arbitrage opportunity alert via all configured channels."""
        message = self.format_arbitrage_message(opportunity)
        
        # Send via Telegram
        telegram_success = self.send_telegram_message(message)
        
        # Send via AWS Lambda
        aws_success = self.send_aws_lambda_notification({
            'type': 'arbitrage_opportunity',
            'data': opportunity,
            'message': message
        })
        
        return telegram_success or aws_success
    
    def send_system_alert(self, alert_type: str, message: str) -> bool:
        """Send system-level alerts (errors, status updates, etc.)."""
        formatted_message = f"🔧 <b>System Alert - {alert_type}</b>\n\n{message}"
        
        return self.send_telegram_message(formatted_message)


# Global notification manager instance
notification_manager = NotificationManager()
