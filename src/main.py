import os, logging, bot
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters

# Get bot authentication token from environment
load_dotenv()
token = os.environ.get('AUTH_TOKEN')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main() -> None:
    """Start the bot."""
    # Create the application and pass it the authentication token
    application = ApplicationBuilder().token(token).build()

    # Intialize handlers
    start_handler = CommandHandler('start', bot.start)
    help_handler = CommandHandler('help', bot.help)
    unknown_handler = CommandHandler(filters.COMMAND, bot.unknown)

    # Register application handlers
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(unknown_handler)

    # Run the bot until user presses Ctrl+C
    application.run_polling()

if __name__ == '__main__':
    main()