from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes) -> None:
    """Display a startup message."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hi there, <b>{update.message.from_user.username}</b>.\n\n" +
              "I can help stay on top of things by logging your tasks and periodically sending you reminders about them.\n\n" +
              "Use /help to see a list of commands.",
        parse_mode='HTML'
    )