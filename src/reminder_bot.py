import os, logging
from dotenv import load_dotenv
from telegram import Updates
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# Get bot authentication token from environment
load_dotenv()
token = os.environ.get('AUTH_TOKEN')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    # Create the application and pass it the authentication token
    application = ApplicationBuilder().token(token).build()

    # Run the bot until user presses Ctrl+C
    application.run_polling()

if __name__ == '__main__':
    main()