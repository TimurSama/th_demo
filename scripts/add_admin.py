"""
Script to add admin user
Usage: python scripts/add_admin.py <user_id>
"""
import sys
import asyncio
import aiosqlite
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DATABASE_PATH
from database import Database


async def add_admin(user_id: int):
    """Add user as admin"""
    # Initialize database
    db_instance = Database(DATABASE_PATH)
    await db_instance.init_db()
    
    async with aiosqlite.connect(DATABASE_PATH) as db:
        try:
            await db.execute(
                "INSERT INTO admin_users (user_id) VALUES (?)",
                (user_id,)
            )
            await db.commit()
            print(f"User {user_id} added as admin successfully.")
        except aiosqlite.IntegrityError:
            print(f"User {user_id} is already an admin.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/add_admin.py <user_id>")
        sys.exit(1)
    
    user_id = int(sys.argv[1])
    asyncio.run(add_admin(user_id))

