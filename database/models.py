"""
Database models for TokenHunter
SQLite database schema definitions
"""
from datetime import datetime
from typing import Optional
import aiosqlite


class Database:
    """Database connection and initialization"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    async def init_db(self):
        """Initialize database tables"""
        async with aiosqlite.connect(self.db_path) as db:
            # Users table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    subscription_level TEXT DEFAULT 'free',
                    referral_code TEXT UNIQUE,
                    referred_by INTEGER,
                    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (referred_by) REFERENCES users(user_id)
                )
            """)
            
            # Referrals table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referrer_id INTEGER NOT NULL,
                    referred_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (referrer_id) REFERENCES users(user_id),
                    FOREIGN KEY (referred_id) REFERENCES users(user_id),
                    UNIQUE(referrer_id, referred_id)
                )
            """)
            
            # Market snapshots table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS market_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    exchange TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    price REAL NOT NULL,
                    volume_24h REAL,
                    change_24h REAL,
                    UNIQUE(timestamp, exchange, symbol)
                )
            """)
            
            # Signals table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    symbol TEXT NOT NULL,
                    exchange TEXT NOT NULL,
                    signal_type TEXT NOT NULL,
                    price REAL NOT NULL,
                    change_24h REAL,
                    volume_24h REAL,
                    status TEXT DEFAULT 'active',
                    expires_at TIMESTAMP,
                    priority_level TEXT DEFAULT 'normal'
                )
            """)
            
            # Giveaways table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS giveaways (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    prize TEXT NOT NULL,
                    prize_type TEXT NOT NULL,
                    start_date TIMESTAMP NOT NULL,
                    end_date TIMESTAMP NOT NULL,
                    status TEXT DEFAULT 'upcoming',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Giveaway participants table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS giveaway_participants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    giveaway_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    tickets INTEGER DEFAULT 1,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (giveaway_id) REFERENCES giveaways(id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    UNIQUE(giveaway_id, user_id)
                )
            """)
            
            # News/Updates table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT DEFAULT 'update',
                    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    published_by INTEGER,
                    is_published BOOLEAN DEFAULT 1
                )
            """)
            
            # Admin users table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS admin_users (
                    user_id INTEGER PRIMARY KEY,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes
            await db.execute("CREATE INDEX IF NOT EXISTS idx_users_referral_code ON users(referral_code)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_market_snapshots_timestamp ON market_snapshots(timestamp)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_signals_status ON signals(status)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_giveaways_status ON giveaways(status)")
            
            await db.commit()


class User:
    """User model"""
    
    @staticmethod
    async def get_or_create(db: aiosqlite.Connection, user_id: int, username: Optional[str] = None,
                           first_name: Optional[str] = None, last_name: Optional[str] = None):
        """Get user or create if not exists"""
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        
        if row:
            return dict(zip([col[0] for col in cursor.description], row))
        
        # Generate referral code
        import secrets
        referral_code = secrets.token_urlsafe(8)[:12]
        
        await db.execute("""
            INSERT INTO users (user_id, username, first_name, last_name, referral_code)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, first_name, last_name, referral_code))
        await db.commit()
        
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        return dict(zip([col[0] for col in cursor.description], row))
    
    @staticmethod
    async def update_subscription(db: aiosqlite.Connection, user_id: int, level: str):
        """Update user subscription level"""
        await db.execute(
            "UPDATE users SET subscription_level = ? WHERE user_id = ?",
            (level, user_id)
        )
        await db.commit()
    
    @staticmethod
    async def update_last_active(db: aiosqlite.Connection, user_id: int):
        """Update user last active timestamp"""
        await db.execute(
            "UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE user_id = ?",
            (user_id,)
        )
        await db.commit()


class Referral:
    """Referral model"""
    
    @staticmethod
    async def create(db: aiosqlite.Connection, referrer_id: int, referred_id: int):
        """Create referral relationship"""
        try:
            await db.execute("""
                INSERT INTO referrals (referrer_id, referred_id)
                VALUES (?, ?)
            """, (referrer_id, referred_id))
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False
    
    @staticmethod
    async def get_referral_count(db: aiosqlite.Connection, user_id: int) -> int:
        """Get referral count for user"""
        cursor = await db.execute(
            "SELECT COUNT(*) FROM referrals WHERE referrer_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
        return row[0] if row else 0


class MarketSnapshot:
    """Market snapshot model"""
    
    @staticmethod
    async def save_snapshot(db: aiosqlite.Connection, exchange: str, symbol: str,
                           price: float, volume_24h: float, change_24h: float):
        """Save market snapshot"""
        await db.execute("""
            INSERT OR REPLACE INTO market_snapshots 
            (timestamp, exchange, symbol, price, volume_24h, change_24h)
            VALUES (datetime('now'), ?, ?, ?, ?, ?)
        """, (exchange, symbol, price, volume_24h, change_24h))
        await db.commit()
    
    @staticmethod
    async def get_latest_snapshots(db: aiosqlite.Connection, limit: int = 50):
        """Get latest market snapshots"""
        cursor = await db.execute("""
            SELECT exchange, symbol, price, volume_24h, change_24h, timestamp
            FROM market_snapshots
            WHERE timestamp >= datetime('now', '-1 hour')
            ORDER BY volume_24h DESC
            LIMIT ?
        """, (limit,))
        rows = await cursor.fetchall()
        return [dict(zip([col[0] for col in cursor.description], row)) for row in rows]


class Signal:
    """Signal model"""
    
    @staticmethod
    async def create(db: aiosqlite.Connection, symbol: str, exchange: str,
                    signal_type: str, price: float, change_24h: float,
                    volume_24h: float, priority_level: str = "normal"):
        """Create signal"""
        await db.execute("""
            INSERT INTO signals 
            (symbol, exchange, signal_type, price, change_24h, volume_24h, priority_level)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (symbol, exchange, signal_type, price, change_24h, volume_24h, priority_level))
        await db.commit()
    
    @staticmethod
    async def get_active_signals(db: aiosqlite.Connection, limit: int = 20):
        """Get active signals"""
        cursor = await db.execute("""
            SELECT * FROM signals
            WHERE status = 'active'
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        rows = await cursor.fetchall()
        return [dict(zip([col[0] for col in cursor.description], row)) for row in rows]


class Giveaway:
    """Giveaway model"""
    
    @staticmethod
    async def create(db: aiosqlite.Connection, title: str, description: str,
                    prize: str, prize_type: str, start_date: datetime,
                    end_date: datetime):
        """Create giveaway"""
        await db.execute("""
            INSERT INTO giveaways 
            (title, description, prize, prize_type, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?, ?, 'upcoming')
        """, (title, description, prize, prize_type, start_date, end_date))
        await db.commit()
    
    @staticmethod
    async def get_active(db: aiosqlite.Connection):
        """Get active giveaways"""
        cursor = await db.execute("""
            SELECT * FROM giveaways
            WHERE status IN ('upcoming', 'active')
            AND datetime('now') >= start_date
            AND datetime('now') <= end_date
            ORDER BY start_date ASC
        """)
        rows = await cursor.fetchall()
        return [dict(zip([col[0] for col in cursor.description], row)) for row in rows]
    
    @staticmethod
    async def participate(db: aiosqlite.Connection, giveaway_id: int, user_id: int, tickets: int = 1):
        """Add user to giveaway"""
        try:
            await db.execute("""
                INSERT OR REPLACE INTO giveaway_participants 
                (giveaway_id, user_id, tickets)
                VALUES (?, ?, COALESCE((SELECT tickets FROM giveaway_participants 
                                       WHERE giveaway_id = ? AND user_id = ?), 0) + ?)
            """, (giveaway_id, user_id, giveaway_id, user_id, tickets))
            await db.commit()
            return True
        except Exception:
            return False


class News:
    """News/Updates model"""
    
    @staticmethod
    async def create(db: aiosqlite.Connection, title: str, content: str,
                    category: str = "update", published_by: Optional[int] = None):
        """Create news item"""
        await db.execute("""
            INSERT INTO news (title, content, category, published_by)
            VALUES (?, ?, ?, ?)
        """, (title, content, category, published_by))
        await db.commit()
    
    @staticmethod
    async def get_recent(db: aiosqlite.Connection, limit: int = 10):
        """Get recent news"""
        cursor = await db.execute("""
            SELECT * FROM news
            WHERE is_published = 1
            ORDER BY published_at DESC
            LIMIT ?
        """, (limit,))
        rows = await cursor.fetchall()
        return [dict(zip([col[0] for col in cursor.description], row)) for row in rows]

