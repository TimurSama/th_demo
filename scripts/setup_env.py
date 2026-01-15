"""
Setup script to create .env file
Usage: python scripts/setup_env.py
"""
import os
from pathlib import Path

ENV_TEMPLATE = """# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN={token}
TELEGRAM_WEBAPP_URL=https://your-domain.com/webapp

# Database
DATABASE_PATH=./data/tokenhunter.db

# Exchanges (comma-separated)
EXCHANGES=binance,okx,bybit,gateio

# Market Pulse Settings
MARKET_PULSE_INTERVAL_HOURS=1
TOP_PAIRS_COUNT=50

# Subscription Settings
FREE_PULSE_INTERVAL_HOURS=4
PRO_PULSE_INTERVAL_HOURS=2
PREMIUM_PULSE_INTERVAL_HOURS=1

# Referral Settings
REFERRAL_BONUS_DAYS=30

# Server Configuration
HOST=0.0.0.0
PORT=5000
DEBUG=False
"""


def setup_env():
    """Create .env file if it doesn't exist"""
    env_path = Path(".env")
    
    if env_path.exists():
        print(".env file already exists. Skipping creation.")
        return
    
    # Use provided token or ask user
    token = os.getenv("TELEGRAM_BOT_TOKEN", "8591869020:AAFnlsirUwd3TKMibAWDE209OBwVU40ZEjo")
    
    env_content = ENV_TEMPLATE.format(token=token)
    
    with open(env_path, "w") as f:
        f.write(env_content)
    
    print(".env file created successfully!")
    print("Please update TELEGRAM_WEBAPP_URL with your actual webapp URL.")


if __name__ == "__main__":
    setup_env()

