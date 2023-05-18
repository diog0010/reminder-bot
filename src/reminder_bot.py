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
    return 0

if __name__ == '__main__':
    main()