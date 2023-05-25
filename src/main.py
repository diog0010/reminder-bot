import os, logging, bot, pytz
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ConversationHandler, filters, CallbackQueryHandler, Defaults

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
    defaults = Defaults(tzinfo=pytz.timezone('US/Eastern'))

    # Create the application and pass it the authentication token
    application = ApplicationBuilder().token(token).defaults(defaults).build()

    # Initialize command handlers
    start_handler = CommandHandler('start', bot.start)
    help_handler = CommandHandler('help', bot.help)
    list_handler = CommandHandler('list', bot.list_tasks)

    # Initialize conversation handlers
    new_task_handler = ConversationHandler(
        entry_points=[CommandHandler('new', bot.new_task)],
        states={
            bot.TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.task)],
            bot.NOTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.notes), CommandHandler('skip', bot.skip_notes)],
            bot.INTERVAL: [CallbackQueryHandler(bot.interval)],
            bot.CUSTOM_INTERVAL: [MessageHandler(filters.Regex('^([0-9][0-9][0-9]:([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9])$|'
                                                               '^(([0-1][0-9]|2[0-4]):[0-5][0-9]:[0-5][0-9])$|'
                                                               '^([0-5][0-9]:[0-5][0-9])$|'
                                                               '^([0-9]:[0-5][0-9])$|'
                                                               '^([0-5][0-9])$|'
                                                               '^([0-9])$'), bot.custom_interval)],
            bot.START: [MessageHandler(filters.Regex('^(([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9])$'), bot.start_time)],
            bot.END: [MessageHandler(filters.Regex('^([0-9][0-9][0-9][0-9]/(0[0-9]|1[0-2])/([0-2][0-9]|3[0-1])) (([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9])$'), bot.end_time)],
            bot.CONFIRM: [CommandHandler('confirm', bot.confirm)]
        },
        fallbacks=[CommandHandler('cancel', bot.cancel)],
        conversation_timeout=30
    )
    delete_task_handler = ConversationHandler(
        entry_points=[CommandHandler('delete', bot.delete_task)],
        states={
            bot.DEL_SELECT: [CallbackQueryHandler(bot.del_select)],
            bot.DEL_CONFIRM: [CallbackQueryHandler(bot.del_confirm)],
        },
        fallbacks=[CommandHandler('cancel', bot.cancel)],
        conversation_timeout=30
    )

    # Register application handlers
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(list_handler)
    application.add_handler(new_task_handler)
    application.add_handler(delete_task_handler)

    # Notify users of invalid command entry
    unknown_handler = MessageHandler(filters.COMMAND, bot.unknown)
    application.add_handler(unknown_handler)

    # Run the bot until user presses Ctrl+C
    application.run_polling()

if __name__ == '__main__':
    main()