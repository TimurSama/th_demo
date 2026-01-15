"""
Main Telegram Bot application
"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from config import TELEGRAM_BOT_TOKEN
from bot.handlers import (
    start_command,
    get_pulse_callback,
    subscription_callback,
    referral_callback,
    giveaways_callback,
    main_menu_callback
)
from bot.admin_handlers import (
    admin_stats_command,
    admin_post_command,
    admin_giveaway_start_command,
    admin_giveaway_end_command,
    admin_broadcast_command
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Initialize and run the bot"""
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(get_pulse_callback, pattern="^get_pulse$"))
    application.add_handler(CallbackQueryHandler(subscription_callback, pattern="^subscription$"))
    application.add_handler(CallbackQueryHandler(referral_callback, pattern="^referral$"))
    application.add_handler(CallbackQueryHandler(giveaways_callback, pattern="^giveaways$"))
    application.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"))
    
    # Admin handlers
    application.add_handler(CommandHandler("admin_stats", admin_stats_command))
    application.add_handler(CommandHandler("admin_post", admin_post_command))
    application.add_handler(CommandHandler("admin_giveaway_start", admin_giveaway_start_command))
    application.add_handler(CommandHandler("admin_giveaway_end", admin_giveaway_end_command))
    application.add_handler(CommandHandler("admin_broadcast", admin_broadcast_command))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Run bot
    logger.info("Bot starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

