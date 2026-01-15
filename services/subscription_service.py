"""
Subscription service
Handles subscription levels and access control
"""
import aiosqlite
from typing import Dict, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class SubscriptionService:
    """Manages user subscriptions"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    async def get_user_subscription(self, user_id: int) -> Dict:
        """
        Get user subscription level
        
        Args:
            user_id: Telegram user ID
        
        Returns:
            Dict with subscription info
        """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT subscription_level FROM users WHERE user_id = ?",
                (user_id,)
            )
            row = await cursor.fetchone()
            
            if row:
                level = row[0] or "free"
            else:
                level = "free"
            
            return {
                "level": level,
                "user_id": user_id
            }
    
    async def can_access_pulse(self, user_id: int, last_pulse_time: Optional[datetime]) -> bool:
        """
        Check if user can access market pulse based on subscription
        
        Args:
            user_id: Telegram user ID
            last_pulse_time: Last time user accessed pulse
        
        Returns:
            True if user can access pulse now
        """
        from config import SUBSCRIPTION_LEVELS
        
        subscription = await self.get_user_subscription(user_id)
        level = subscription["level"]
        
        if level not in SUBSCRIPTION_LEVELS:
            level = "free"
        
        interval_hours = SUBSCRIPTION_LEVELS[level]["pulse_interval_hours"]
        
        if last_pulse_time is None:
            return True
        
        next_access_time = last_pulse_time + timedelta(hours=interval_hours)
        return datetime.utcnow() >= next_access_time
    
    async def get_subscription_info(self, level: str) -> Dict:
        """
        Get subscription level information
        
        Args:
            level: Subscription level name
        
        Returns:
            Dict with subscription details
        """
        from config import SUBSCRIPTION_LEVELS
        
        if level not in SUBSCRIPTION_LEVELS:
            level = "free"
        
        return SUBSCRIPTION_LEVELS[level]

