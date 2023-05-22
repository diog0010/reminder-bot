import os, logging, bot
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ConversationHandler, filters

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

    # Initialize command handlers
    start_handler = CommandHandler('start', bot.start)
    help_handler = CommandHandler('help', bot.help)

    # Initialize conversation handlers
    new_task_handler = ConversationHandler(
        entry_points=[CommandHandler('new', bot.new_task)],
        states={
            bot.TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.task)],
            bot.NOTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.notes), CommandHandler('skip', bot.skip_notes)],
            bot.INTERVAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.interval)], # FIX THIS
            bot.END_DATETIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.end_datetime)], # FIX THIS
            bot.CONFIRM: [CommandHandler('confirm', bot.confirm)]
        },
        fallbacks=[CommandHandler('cancel', bot.cancel)]
    )

    # Register application handlers
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(new_task_handler)

    # Notify users of invalid command entry
    unknown_handler = MessageHandler(filters.COMMAND, bot.unknown)
    application.add_handler(unknown_handler)

    # Run the bot until user presses Ctrl+C
    application.run_polling()

if __name__ == '__main__':
    main()