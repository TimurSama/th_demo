"""
Referral service
Handles referral system logic
"""
import aiosqlite
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ReferralService:
    """Manages referral system"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    async def get_referral_link(self, user_id: int) -> str:
        """
        Get user's referral link
        
        Args:
            user_id: Telegram user ID
        
        Returns:
            Referral link
        """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT referral_code FROM users WHERE user_id = ?",
                (user_id,)
            )
            row = await cursor.fetchone()
            
            if row and row[0]:
                referral_code = row[0]
            else:
                # Generate new code if missing
                import secrets
                referral_code = secrets.token_urlsafe(8)[:12]
                await db.execute(
                    "UPDATE users SET referral_code = ? WHERE user_id = ?",
                    (referral_code, user_id)
                )
                await db.commit()
            
            # Bot username will be set when creating referral link
            # For now, return code that can be used with bot username
            return referral_code
    
    async def process_referral(self, referrer_code: str, referred_user_id: int) -> bool:
        """
        Process referral when new user joins via referral link
        
        Args:
            referrer_code: Referral code of the referrer
            referred_user_id: User ID of the new user
        
        Returns:
            True if referral was processed successfully
        """
        async with aiosqlite.connect(self.db_path) as db:
            # Find referrer by code
            cursor = await db.execute(
                "SELECT user_id FROM users WHERE referral_code = ?",
                (referrer_code,)
            )
            row = await cursor.fetchone()
            
            if not row:
                return False
            
            referrer_id = row[0]
            
            # Don't allow self-referral
            if referrer_id == referred_user_id:
                return False
            
            # Create referral relationship
            from database import Referral
            return await Referral.create(db, referrer_id, referred_user_id)
    
    async def get_referral_stats(self, user_id: int) -> Dict:
        """
        Get referral statistics for user
        
        Args:
            user_id: Telegram user ID
        
        Returns:
            Dict with referral stats
        """
        async with aiosqlite.connect(self.db_path) as db:
            from database import Referral
            
            referral_count = await Referral.get_referral_count(db, user_id)
            
            return {
                "referral_count": referral_count,
                "user_id": user_id
            }

