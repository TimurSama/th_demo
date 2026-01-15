"""
Telegram Bot handlers
Command and callback handlers with Matrix-style tone
"""
import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import aiosqlite

from config import DATABASE_PATH, SUBSCRIPTION_LEVELS, TELEGRAM_BOT_TOKEN
from database import Database, User, MarketSnapshot, Referral
from services.subscription_service import SubscriptionService
from services.referral_service import ReferralService
from services.market_collector import MarketCollector
from config import EXCHANGES

logger = logging.getLogger(__name__)

# Initialize services
subscription_service = SubscriptionService(DATABASE_PATH)
referral_service = ReferralService(DATABASE_PATH)
market_collector = MarketCollector(EXCHANGES)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with referral support"""
    user = update.effective_user
    user_id = user.id
    
    # Check for referral code
    referral_code = None
    if context.args and len(context.args) > 0:
        ref_arg = context.args[0]
        if ref_arg.startswith("ref_"):
            referral_code = ref_arg[4:]
    
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Get or create user
        user_data = await User.get_or_create(
            db, user_id, user.username, user.first_name, user.last_name
        )
        
        # Process referral if present
        if referral_code:
            await referral_service.process_referral(referral_code, user_id)
        
        await User.update_last_active(db, user_id)
    
    # Welcome message in Matrix style
    username = user.first_name or user.username or "node"
    message = f"Knock knock, {username}.\n\n"
    message += "The network has detected your signal.\n"
    message += "Market streams are active.\n\n"
    message += "Choose your next move."
    
    keyboard = [
        [InlineKeyboardButton("GET THE PULSE", callback_data="get_pulse")],
        [
            InlineKeyboardButton("Subscription Level", callback_data="subscription"),
            InlineKeyboardButton("Referral System", callback_data="referral")
        ],
        [
            InlineKeyboardButton("Giveaways", callback_data="giveaways"),
            InlineKeyboardButton("Application", url=f"https://t.me/{context.bot.username}?startapp=main")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, reply_markup=reply_markup)


async def get_pulse_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle GET THE PULSE button"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    # Check subscription access
    async with aiosqlite.connect(DATABASE_PATH) as db:
        subscription = await subscription_service.get_user_subscription(user_id)
        level = subscription["level"]
        
        # Get latest market snapshots
        snapshots = await MarketSnapshot.get_latest_snapshots(db, limit=20)
    
    if not snapshots:
        # Collect fresh data if no snapshots
        pulse_data = await market_collector.get_market_pulse(top_pairs_limit=20)
        
        # Save to database
        async with aiosqlite.connect(DATABASE_PATH) as db:
            for item in pulse_data:
                for exchange_data in item.get('exchanges', []):
                    await MarketSnapshot.save_snapshot(
                        db,
                        exchange_data['exchange'],
                        item['symbol'],
                        item['avg_price'],
                        item['total_volume_24h'],
                        item['avg_change_24h']
                    )
        
        # Format message
        message = "MARKET PULSE — LAST SNAPSHOT\n\n"
        for item in pulse_data[:10]:
            symbol = item['symbol']
            change = item['avg_change_24h']
            volume = item['total_volume_24h']
            
            change_str = f"+{change:.2f}%" if change >= 0 else f"{change:.2f}%"
            volume_str = format_volume(volume)
            
            message += f"{symbol:12} | {change_str:8} | Vol: {volume_str}\n"
        
        message += "\nData source: multi-exchange\n"
        message += f"Timestamp: UTC\n\n"
        message += f"Access level: {SUBSCRIPTION_LEVELS[level]['name']}"
    else:
        # Format from database snapshots
        message = "MARKET PULSE — LAST SNAPSHOT\n\n"
        for snapshot in snapshots[:10]:
            symbol = snapshot['symbol']
            change = snapshot['change_24h']
            volume = snapshot['volume_24h']
            
            change_str = f"+{change:.2f}%" if change >= 0 else f"{change:.2f}%"
            volume_str = format_volume(volume)
            
            message += f"{symbol:12} | {change_str:8} | Vol: {volume_str}\n"
        
        message += "\nData source: multi-exchange\n"
        message += f"Timestamp: UTC\n\n"
        message += f"Access level: {SUBSCRIPTION_LEVELS[level]['name']}"
    
    # Show main menu
    keyboard = [
        [InlineKeyboardButton("GET THE PULSE", callback_data="get_pulse")],
        [
            InlineKeyboardButton("Subscription Level", callback_data="subscription"),
            InlineKeyboardButton("Referral System", callback_data="referral")
        ],
        [
            InlineKeyboardButton("Giveaways", callback_data="giveaways"),
            InlineKeyboardButton("Application", url=f"https://t.me/{context.bot.username}?startapp=main")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup)


async def subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Subscription Level menu"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    subscription = await subscription_service.get_user_subscription(user_id)
    current_level = subscription["level"]
    
    message = "SUBSCRIPTION LEVELS\n\n"
    message += "Choose your level of access.\n\n"
    
    for level_key, level_data in SUBSCRIPTION_LEVELS.items():
        marker = "✓" if level_key == current_level else "○"
        message += f"{marker} {level_key.upper()}\n"
        message += f"  {level_data['name']}\n"
        for feature in level_data['features']:
            message += f"  • {feature}\n"
        message += "\n"
    
    keyboard = [
        [InlineKeyboardButton("← Back", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup)


async def referral_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Referral System menu"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    # Get referral stats
    stats = await referral_service.get_referral_stats(user_id)
    referral_code = await referral_service.get_referral_link(user_id)
    bot_username = context.bot.username or "your_bot"
    referral_link = f"https://t.me/{bot_username}?start=ref_{referral_code}"
    
    message = "REFERRAL SYSTEM\n\n"
    message += "Invite new nodes into the network.\n\n"
    message += "Earn bonuses for every active referral.\n"
    message += "The deeper your network — the higher your influence.\n\n"
    message += f"Your referrals: {stats['referral_count']}\n\n"
    message += f"Invite link:\n{referral_link}"
    
    keyboard = [
        [InlineKeyboardButton("COPY INVITE LINK", callback_data=f"copy_link_{user_id}")],
        [InlineKeyboardButton("SEND INVITATION", callback_data=f"send_invite_{user_id}")],
        [InlineKeyboardButton("← Back", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup)


async def giveaways_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Giveaways menu"""
    query = update.callback_query
    await query.answer()
    
    from database import Giveaway
    
    async with aiosqlite.connect(DATABASE_PATH) as db:
        giveaways = await Giveaway.get_active(db)
    
    if not giveaways:
        message = "GIVEAWAYS\n\n"
        message += "No active giveaways at the moment.\n\n"
        message += "The network is preparing new opportunities."
    else:
        message = "GIVEAWAYS\n\n"
        for giveaway in giveaways:
            message += f"ACTIVE GIVEAWAY\n"
            message += f"Prize: {giveaway['prize']}\n"
            message += f"Ends in: {giveaway['end_date']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("← Back", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup)


async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to main menu"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    username = user.first_name or user.username or "node"
    
    message = f"Knock knock, {username}.\n\n"
    message += "The network has detected your signal.\n"
    message += "Market streams are active.\n\n"
    message += "Choose your next move."
    
    keyboard = [
        [InlineKeyboardButton("GET THE PULSE", callback_data="get_pulse")],
        [
            InlineKeyboardButton("Subscription Level", callback_data="subscription"),
            InlineKeyboardButton("Referral System", callback_data="referral")
        ],
        [
            InlineKeyboardButton("Giveaways", callback_data="giveaways"),
            InlineKeyboardButton("Application", url=f"https://t.me/{context.bot.username}?startapp=main")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup)


def format_volume(volume: float) -> str:
    """Format volume for display"""
    if volume >= 1_000_000_000:
        return f"{volume / 1_000_000_000:.2f}B"
    elif volume >= 1_000_000:
        return f"{volume / 1_000_000:.2f}M"
    elif volume >= 1_000:
        return f"{volume / 1_000:.2f}K"
    else:
        return f"{volume:.2f}"

