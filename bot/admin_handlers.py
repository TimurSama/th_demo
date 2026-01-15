"""
Admin handlers for Telegram Bot
Admin-only commands for managing the system
"""
import logging
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
import aiosqlite

from config import DATABASE_PATH
from database import News, Giveaway, User

logger = logging.getLogger(__name__)


async def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT 1 FROM admin_users WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
        return row is not None


async def admin_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command: /admin_stats"""
    user_id = update.effective_user.id
    
    if not await is_admin(user_id):
        await update.message.reply_text("Access denied. You are not inside the grid.")
        return
    
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Total users
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        total_users = (await cursor.fetchone())[0]
        
        # Active users (last 24h)
        cursor = await db.execute("""
            SELECT COUNT(*) FROM users 
            WHERE last_active >= datetime('now', '-24 hours')
        """)
        active_users = (await cursor.fetchone())[0]
        
        # Subscription breakdown
        cursor = await db.execute("""
            SELECT subscription_level, COUNT(*) 
            FROM users 
            GROUP BY subscription_level
        """)
        subscriptions = await cursor.fetchall()
        
        # Total referrals
        cursor = await db.execute("SELECT COUNT(*) FROM referrals")
        total_referrals = (await cursor.fetchone())[0]
        
        # Active giveaways
        cursor = await db.execute("""
            SELECT COUNT(*) FROM giveaways 
            WHERE status IN ('active', 'upcoming')
        """)
        active_giveaways = (await cursor.fetchone())[0]
    
    message = "SYSTEM STATISTICS\n\n"
    message += f"Total users: {total_users}\n"
    message += f"Active (24h): {active_users}\n\n"
    message += "Subscriptions:\n"
    for level, count in subscriptions:
        message += f"  {level}: {count}\n"
    message += f"\nTotal referrals: {total_referrals}\n"
    message += f"Active giveaways: {active_giveaways}"
    
    await update.message.reply_text(message)


async def admin_post_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command: /admin_post"""
    user_id = update.effective_user.id
    
    if not await is_admin(user_id):
        await update.message.reply_text("Access denied. You are not inside the grid.")
        return
    
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /admin_post <title> <content>\n"
            "Example: /admin_post \"Update\" \"New features available\""
        )
        return
    
    title = context.args[0]
    content = " ".join(context.args[1:])
    
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await News.create(db, title, content, "update", user_id)
    
    await update.message.reply_text("News post created. The network has been updated.")


async def admin_giveaway_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command: /admin_giveaway_start"""
    user_id = update.effective_user.id
    
    if not await is_admin(user_id):
        await update.message.reply_text("Access denied. You are not inside the grid.")
        return
    
    if not context.args or len(context.args) < 4:
        await update.message.reply_text(
            "Usage: /admin_giveaway_start <title> <prize> <prize_type> <days>\n"
            "Example: /admin_giveaway_start \"Premium Access\" \"30 days\" \"premium\" 7"
        )
        return
    
    title = context.args[0]
    prize = context.args[1]
    prize_type = context.args[2]
    days = int(context.args[3])
    
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=days)
    
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await Giveaway.create(
            db, title, "", prize, prize_type, start_date, end_date
        )
    
    await update.message.reply_text(f"Giveaway started. Ends in {days} days.")


async def admin_giveaway_end_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command: /admin_giveaway_end"""
    user_id = update.effective_user.id
    
    if not await is_admin(user_id):
        await update.message.reply_text("Access denied. You are not inside the grid.")
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /admin_giveaway_end <giveaway_id>")
        return
    
    giveaway_id = int(context.args[0])
    
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE giveaways SET status = 'ended' WHERE id = ?",
            (giveaway_id,)
        )
        await db.commit()
    
    await update.message.reply_text("Giveaway ended. The network has processed the results.")


async def admin_broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command: /admin_broadcast"""
    user_id = update.effective_user.id
    
    if not await is_admin(user_id):
        await update.message.reply_text("Access denied. You are not inside the grid.")
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /admin_broadcast <message>")
        return
    
    message = " ".join(context.args)
    
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT user_id FROM users")
        users = await cursor.fetchall()
    
    # Note: In production, you'd want to batch these and handle rate limits
    sent = 0
    failed = 0
    
    for (target_user_id,) in users:
        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text=message
            )
            sent += 1
        except Exception as e:
            logger.error(f"Failed to send to {target_user_id}: {e}")
            failed += 1
    
    await update.message.reply_text(
        f"Broadcast complete.\nSent: {sent}\nFailed: {failed}"
    )

