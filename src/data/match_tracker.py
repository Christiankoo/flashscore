"""Match tracking and deduplication system."""

import os
import hashlib
from typing import Dict, List, Set
from pathlib import Path
import pandas as pd
from src.utils.logging import main_logger


class MatchTracker:
    """Tracks processed matches and opportunities to prevent duplicates."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.checked_file = self.data_dir / "checked_opportunities.csv"
        self.processed_matches_file = self.data_dir / "processed_matches.csv"
        
        # Load existing data
        self.checked_opportunities = self._load_checked_opportunities()
        self.processed_matches = self._load_processed_matches()
    
    def _load_checked_opportunities(self) -> Set[str]:
        """Load previously checked opportunities."""
        if self.checked_file.exists():
            try:
                df = pd.read_csv(self.checked_file)
                return set(df['opportunity_hash'].tolist())
            except Exception as e:
                main_logger.warning(f"Could not load checked opportunities: {e}")
        return set()
    
    def _load_processed_matches(self) -> Set[str]:
        """Load previously processed matches."""
        if self.processed_matches_file.exists():
            try:
                df = pd.read_csv(self.processed_matches_file)
                return set(df['match_hash'].tolist())
            except Exception as e:
                main_logger.warning(f"Could not load processed matches: {e}")
        return set()
    
    def _generate_opportunity_hash(self, opportunity: Dict) -> str:
        """Generate unique hash for an arbitrage opportunity."""
        # Create hash based on key opportunity characteristics
        hash_data = {
            'home_team': opportunity.get('home_team', ''),
            'away_team': opportunity.get('away_team', ''),
            'sport': opportunity.get('sport', ''),
            'type': opportunity.get('type', ''),
            'match_time': opportunity.get('match_time', ''),
            'profit_margin': round(opportunity.get('profit_margin', 0), 2)
        }
        
        hash_string = str(sorted(hash_data.items()))
        return hashlib.md5(hash_string.encode()).hexdigest()
    
    def _generate_match_hash(self, match: Dict) -> str:
        """Generate unique hash for a match."""
        hash_data = {
            'home_team': match.get('home_team', ''),
            'away_team': match.get('away_team', ''),
            'sport': match.get('sport', ''),
            'match_time': match.get('match_time', ''),
            'site': match.get('site', '')
        }
        
        hash_string = str(sorted(hash_data.items()))
        return hashlib.md5(hash_string.encode()).hexdigest()
    
    def is_opportunity_new(self, opportunity: Dict) -> bool:
        """Check if an arbitrage opportunity is new."""
        opportunity_hash = self._generate_opportunity_hash(opportunity)
        return opportunity_hash not in self.checked_opportunities
    
    def is_match_new(self, match: Dict) -> bool:
        """Check if a match is new."""
        match_hash = self._generate_match_hash(match)
        return match_hash not in self.processed_matches
    
    def mark_opportunity_sent(self, opportunity: Dict):
        """Mark an opportunity as sent/processed."""
        opportunity_hash = self._generate_opportunity_hash(opportunity)
        
        if opportunity_hash not in self.checked_opportunities:
            self.checked_opportunities.add(opportunity_hash)
            
            # Save to CSV
            opportunity_data = {
                'opportunity_hash': opportunity_hash,
                'home_team': opportunity.get('home_team', ''),
                'away_team': opportunity.get('away_team', ''),
                'sport': opportunity.get('sport', ''),
                'type': opportunity.get('type', ''),
                'profit_margin': opportunity.get('profit_margin', 0),
                'timestamp': pd.Timestamp.now()
            }
            
            # Append to CSV
            df = pd.DataFrame([opportunity_data])
            if self.checked_file.exists():
                df.to_csv(self.checked_file, mode='a', header=False, index=False)
            else:
                df.to_csv(self.checked_file, index=False)
            
            main_logger.info(f"Marked opportunity as sent: {opportunity_hash}")
    
    def mark_match_processed(self, match: Dict):
        """Mark a match as processed."""
        match_hash = self._generate_match_hash(match)
        
        if match_hash not in self.processed_matches:
            self.processed_matches.add(match_hash)
            
            # Save to CSV
            match_data = {
                'match_hash': match_hash,
                'home_team': match.get('home_team', ''),
                'away_team': match.get('away_team', ''),
                'sport': match.get('sport', ''),
                'site': match.get('site', ''),
                'timestamp': pd.Timestamp.now()
            }
            
            # Append to CSV
            df = pd.DataFrame([match_data])
            if self.processed_matches_file.exists():
                df.to_csv(self.processed_matches_file, mode='a', header=False, index=False)
            else:
                df.to_csv(self.processed_matches_file, index=False)
    
    def filter_new_opportunities(self, opportunities: List[Dict]) -> List[Dict]:
        """Filter out already processed opportunities."""
        new_opportunities = []
        
        for opportunity in opportunities:
            if self.is_opportunity_new(opportunity):
                new_opportunities.append(opportunity)
        
        main_logger.info(f"Filtered {len(opportunities)} opportunities -> {len(new_opportunities)} new")
        return new_opportunities
    
    def filter_new_matches(self, matches: List[Dict]) -> List[Dict]:
        """Filter out already processed matches."""
        new_matches = []
        
        for match in matches:
            if self.is_match_new(match):
                new_matches.append(match)
        
        return new_matches
    
    def cleanup_old_records(self, days_old: int = 7):
        """Clean up old tracking records."""
        cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=days_old)
        
        # Clean opportunities
        if self.checked_file.exists():
            try:
                df = pd.read_csv(self.checked_file)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df_filtered = df[df['timestamp'] > cutoff_date]
                df_filtered.to_csv(self.checked_file, index=False)
                
                # Update in-memory set
                self.checked_opportunities = set(df_filtered['opportunity_hash'].tolist())
                
                main_logger.info(f"Cleaned up {len(df) - len(df_filtered)} old opportunity records")
            except Exception as e:
                main_logger.error(f"Error cleaning opportunity records: {e}")
        
        # Clean matches
        if self.processed_matches_file.exists():
            try:
                df = pd.read_csv(self.processed_matches_file)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df_filtered = df[df['timestamp'] > cutoff_date]
                df_filtered.to_csv(self.processed_matches_file, index=False)
                
                # Update in-memory set
                self.processed_matches = set(df_filtered['match_hash'].tolist())
                
                main_logger.info(f"Cleaned up {len(df) - len(df_filtered)} old match records")
            except Exception as e:
                main_logger.error(f"Error cleaning match records: {e}")
    
    def get_stats(self) -> Dict:
        """Get tracking statistics."""
        return {
            'total_opportunities_tracked': len(self.checked_opportunities),
            'total_matches_tracked': len(self.processed_matches),
            'data_directory': str(self.data_dir)
        }
