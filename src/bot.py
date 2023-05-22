from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

TASK, NOTES, INTERVAL, END_DATETIME, CONFIRM = range(4)

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
    """Store task name and prompt additional notes input."""
    context.user_data['task'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Are there any additional notes you would like me to include in the reminder? Enter /skip to skip this step."
    )
    return NOTES

async def notes(update: Update, context: ContextTypes) -> int:
    """Store additional notes and prompt reminder interval input."""
    context.user_data['notes'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="How often do you want to receive a reminder for this task?"
    )
    return INTERVAL

async def skip_notes(update: Update, context: ContextTypes) -> int:
    """Skip adding additional task notes."""
    context.user_data['notes'] = None
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="How often do you want to receive a reminder for this task?"
    )
    return INTERVAL

async def interval(update: Update, context: ContextTypes) -> int:
    """Store reminder interval and prompt reminder end datetime input."""
    context.user_data['interval'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="When would you like to stop receiving reminders about this task?"
    )
    return END_DATETIME

async def end_datetime(update: Update, context: ContextTypes) -> int:
    """Store reminder end datetime and ask user to confirm conversation input."""
    context.user_data['end_datetime'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Task: {context.user_data['task']}\n"
             f"Notes: {context.user_data['notes']}\n"
             f"Interval: {context.user_data['interval']}\n"
             f"End: {context.user_data['end_datetime']}\n"
              "Enter /confirm to start receiving reminders about this task. Otherwise, enter /cancel."
    )
    return CONFIRM

async def confirm(update: Update, context: ContextTypes) -> int:
    """Add reminder to job queue and end the conversation"""
    context.job_queue.run_repeating(
        remind, 
        5, 
        last=15, 
        name=context.user_data['task'], 
        chat_id=update.effective_chat.id,
        user_id=update.message.from_user.id
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Task entry confirmed. You will now start receiving reminders for the following task\n\n"
             f"{context.user_data['task']}"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes) -> int:
    """End a conversation early."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ending conversation..."
    )
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