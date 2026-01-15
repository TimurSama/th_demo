"""
Configuration module for TokenHunter
Centralized configuration management
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_WEBAPP_URL = os.getenv("TELEGRAM_WEBAPP_URL", "")

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", str(DATA_DIR / "tokenhunter.db"))

# Exchange Configuration
EXCHANGES = os.getenv("EXCHANGES", "binance,okx,bybit,gateio").split(",")
EXCHANGES = [ex.strip() for ex in EXCHANGES]

# Market Pulse Configuration
MARKET_PULSE_INTERVAL_HOURS = int(os.getenv("MARKET_PULSE_INTERVAL_HOURS", "1"))
TOP_PAIRS_COUNT = int(os.getenv("TOP_PAIRS_COUNT", "50"))

# Subscription Configuration
SUBSCRIPTION_LEVELS = {
    "free": {
        "name": "FREE ACCESS",
        "pulse_interval_hours": int(os.getenv("FREE_PULSE_INTERVAL_HOURS", "4")),
        "features": [
            "Market pulse every 4 hours",
            "Limited signals",
            "Public data stream"
        ]
    },
    "pro": {
        "name": "PRO ACCESS",
        "pulse_interval_hours": int(os.getenv("PRO_PULSE_INTERVAL_HOURS", "2")),
        "features": [
            "Market pulse every 2 hours",
            "Extended signals",
            "Priority data stream"
        ]
    },
    "premium": {
        "name": "PREMIUM ACCESS",
        "pulse_interval_hours": int(os.getenv("PREMIUM_PULSE_INTERVAL_HOURS", "1")),
        "features": [
            "Market pulse every 1 hour",
            "Full signal feed",
            "Access to private signals chat"
        ]
    }
}

# Referral Configuration
REFERRAL_BONUS_DAYS = int(os.getenv("REFERRAL_BONUS_DAYS", "30"))

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Validate critical configuration
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN must be set in environment variables")

