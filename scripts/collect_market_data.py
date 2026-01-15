"""
Market data collection script
Runs periodically to collect and store market data
Can be executed via GitHub Actions cron or locally
"""
import asyncio
import logging
import sys
import aiosqlite
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DATABASE_PATH, EXCHANGES, TOP_PAIRS_COUNT
from database import Database, MarketSnapshot
from services.market_collector import MarketCollector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def collect_and_store():
    """Collect market data and store in database"""
    # Initialize database
    db_instance = Database(DATABASE_PATH)
    await db_instance.init_db()
    
    # Initialize collector
    collector = MarketCollector(EXCHANGES)
    
    logger.info("Starting market data collection...")
    
    # Collect market pulse
    pulse_data = await collector.get_market_pulse(top_pairs_limit=TOP_PAIRS_COUNT)
    
    logger.info(f"Collected {len(pulse_data)} market pairs")
    
    # Store in database
    async with aiosqlite.connect(DATABASE_PATH) as db:
        stored_count = 0
        for item in pulse_data:
            for exchange_data in item.get('exchanges', []):
                try:
                    await MarketSnapshot.save_snapshot(
                        db,
                        exchange_data['exchange'],
                        item['symbol'],
                        item['avg_price'],
                        item['total_volume_24h'],
                        item['avg_change_24h']
                    )
                    stored_count += 1
                except Exception as e:
                    logger.error(f"Error storing snapshot for {item['symbol']} on {exchange_data['exchange']}: {e}")
        
        logger.info(f"Stored {stored_count} market snapshots")
    
    logger.info("Market data collection complete")


if __name__ == "__main__":
    asyncio.run(collect_and_store())

