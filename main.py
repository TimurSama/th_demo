"""
Main entry point for TokenHunter
Initializes database and starts the bot
"""
import asyncio
import logging
from pathlib import Path

from config import DATABASE_PATH
from database import Database
from bot.bot import main as bot_main

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def init_database():
    """Initialize database"""
    logger.info("Initializing database...")
    db = Database(DATABASE_PATH)
    await db.init_db()
    logger.info("Database initialized")


if __name__ == "__main__":
    # Initialize database
    asyncio.run(init_database())
    
    # Start bot
    logger.info("Starting TokenHunter bot...")
    bot_main()

