from telegram import Update
from telegram.ext import ContextTypes

class Reminder:
    """A class representing a reminder"""
    def __init__(self, title, description, interval, end):
        self.title = title
        self.description = description
        self.interval = interval
        self.end = end

async def start(update: Update, context: ContextTypes) -> None:
    """Display a startup message."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hi there, <b>{update.message.from_user.username}</b>.\n\n"
              "I can help you stay on top of things by logging your tasks and periodically sending you reminders about them.\n\n"
              "Use /help to see a list of commands.",
        parse_mode='HTML'
    )

async def help(update: Update, context:ContextTypes) -> None:
    """Display a list of commands."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="<b>Available Commands</b>\n"
             "/new - Create a new task\n"
             "/list - List all current tasks\n"
             "/edit - Edit a task\n"
             "/delete - Delete a task\n",
        parse_mode='HTML'
    )

async def new_reminder(update: Update, context:ContextTypes) -> None:
    """Create a new reminder."""

async def edit_reminder(update: Update, context:ContextTypes) -> None:
    """Edit an existing reminder."""

async def delete_reminder(update: Update, context:ContextTypes) -> None:
    """Delete an existing reminder."""

async def unknown(update: Update, context:ContextTypes) -> None:
    """Display unknown command error message."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I don't understand that command.\n\n"
             "Use /help to see a list of available commands."
    )