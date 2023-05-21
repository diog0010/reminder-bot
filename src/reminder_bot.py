import os, logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# Get bot authentication token from environment
load_dotenv()
token = os.environ.get('AUTH_TOKEN')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes) -> None:
    """Display a startup message."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hi there, <b>{update.message.from_user.username}</b>.\n\n" +
              "I can help stay on top of things by logging your tasks and periodically sending you reminders about them.\n\n" +
              "Use /help to see a list of commands.",
        parse_mode='HTML'
    )

def main() -> None:
    """Start the bot."""
    # Create the application and pass it the authentication token
    application = ApplicationBuilder().token(token).build()

    # Intialize handlers
    start_handler = CommandHandler('start', start)

    # Register application handlers
    application.add_handler(start_handler)

    # Run the bot until user presses Ctrl+C
    application.run_polling()

if __name__ == '__main__':
    main()