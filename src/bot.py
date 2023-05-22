from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

TASK, MESSAGE, INTERVAL, END_DATETIME = range(4)

async def start(update: Update, context: ContextTypes) -> None:
    """Display a startup message."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hi there, <b>{update.message.from_user.username}</b>.\n\n"
              "I can help you stay on top of things by logging your tasks and periodically sending you reminders about them.\n\n"
              "Use /help to see a list of commands.",
        parse_mode='HTML'
    )

async def help(update: Update, context: ContextTypes) -> None:
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

async def remind(context: ContextTypes) -> None:
    """Send a reminder message."""
    await context.bot.send_message(chat_id=context.job.chat_id, text=f"TASK: {context.job.data}")

async def new_task(update: Update, context: ContextTypes) -> int:
    """Create a new task."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="What task would you like to be reminded about?"
    )
    return TASK

async def task(update: Update, context: ContextTypes) -> int:
    """Store task name."""
    chat_id = update.message.chat_id
    task = update.message.text
    context.job_queue.run_once(remind, 10, data=task, chat_id=chat_id)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes) -> int:
    """End a conversation early."""

    return ConversationHandler.END

async def edit_task(update: Update, context: ContextTypes) -> None:
    """Edit an existing task."""

async def delete_task(update: Update, context: ContextTypes) -> None:
    """Delete an existing task."""

async def unknown(update: Update, context: ContextTypes) -> None:
    """Display unknown command error message."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I don't understand that command.\n\n"
             "Use /help to see a list of available commands."
    )