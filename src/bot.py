from datetime import time, timedelta
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler

# Initialize new task constants
TASK, NOTES, INTERVAL, CUSTOM_INTERVAL, START, END, CONFIRM = range(7)

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
    job = context.job
    await context.bot.send_message(
        chat_id=context.job.chat_id, 
        text=f"This is a message to remind you of the following task:\n\n"
             f"<b>{job.data['task']}</b>\n"
             f"<i>{job.data['notes']}</i>\n\n"
             f"Don't forget!",
        parse_mode='HTML'
    )

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
    keyboard = [
        [
            InlineKeyboardButton("Hourly", callback_data="hourly"),
            InlineKeyboardButton("Daily", callback_data="daily"),
        ],
        [
            InlineKeyboardButton("Weekly", callback_data="weekly"),
            InlineKeyboardButton("Monthly", callback_data="monthly"),
        ],
        [InlineKeyboardButton("Custom", callback_data="custom")]
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="How often do you want to receive a reminder for this task?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return INTERVAL

async def skip_notes(update: Update, context: ContextTypes) -> int:
    """Skip adding additional task notes."""
    context.user_data['notes'] = "No additional notes."

    keyboard = [
        [
            InlineKeyboardButton("Hourly", callback_data="hourly"),
            InlineKeyboardButton("Daily", callback_data="daily"),
        ],
        [
            InlineKeyboardButton("Weekly", callback_data="weekly"),
            InlineKeyboardButton("Monthly", callback_data="monthly"),
        ],
        [InlineKeyboardButton("Custom", callback_data="custom")]
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="How often do you want to receive a reminder for this task?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return INTERVAL

async def interval(update: Update, context: ContextTypes) -> int:
    """Store reminder interval and prompt reminder start datetime input."""
    query = update.callback_query
    context.user_data['interval'] = query.data

    await query.answer()

    if query.data == "custom":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Enter your preferred interval between reminders for this task using 24 hour notation (i.e. hh:mm:ss)."
        )
        return CUSTOM_INTERVAL

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="When would you like to start receiving reminders about this task?\n\n" 
             "Please use 24 hour notation (i.e. hh:mm:ss)"
    )
    return START

async def custom_interval(update: Update, context: ContextTypes) -> int:
    """Store custom reminder interval and prompt reminder start datetime input."""
    context.user_data['interval'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="When would you like to start receiving reminders about this task?\n\n" 
             "Please use 24 hour notation (i.e. hh:mm:ss)"
    )
    return START

async def start_time(update: Update, context: ContextTypes) -> int:
    """Store reminder start datetime and prompt reminder end datetime input."""
    context.user_data['start'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="When would you like to stop receiving reminders about this task?\n\n"
             "Please use 24 hour notation (i.e. hh:mm:ss)"
    )
    return END

async def end_time(update: Update, context: ContextTypes) -> int:
    """Store reminder end datetime and ask user to confirm conversation input."""
    context.user_data['end'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You entered the following:\n\n"
             f"Task: {context.user_data['task']}\n"
             f"Notes: {context.user_data['notes']}\n"
             f"Interval: {context.user_data['interval']}\n"
             f"Start: {context.user_data['start']}\n"
             f"End: {context.user_data['end']}\n\n"
              "Enter /confirm to start receiving reminders about this task. Otherwise, enter /cancel."
    )
    return CONFIRM

def parse_time_notation(notation: str) -> tuple:
    """Seperate a time notation string into its various units."""
    days, hours, minutes, seconds = 0, 0, 0, 0

    notation = notation.split(':')
    
    for i in range(len(notation)):
        if i == 0:
            seconds = int(notation[len(notation)-(1+i)])
        elif i == 1:
            minutes = int(notation[len(notation)-(1+i)])
        elif i == 2:
            hours = int(notation[len(notation)-(1+i)])
        elif i == 3:
            days = int(notation[len(notation)-(1+i)])

    return (seconds, minutes, hours, days)  

async def confirm(update: Update, context: ContextTypes) -> int:
    """Add reminder to job queue and end the conversation"""
    start = parse_time_notation(context.user_data['start'])

    reminder = {
        "task": context.user_data['task'],
        "notes": context.user_data['notes'],
        "interval": context.user_data['interval'],
        "start": context.user_data['start'],
        "end": context.user_data['end'],
    }

    interval = 0

    match reminder['interval']:
        case "hourly":
            interval = timedelta(hours=1)
        case "daily":
            interval = timedelta(days=1)
        case "weekly":
            interval = timedelta(weeks=1)
        case "monthly":
            interval = timedelta(weeks=4)
        case _:
            interval = parse_time_notation(context.user_data['interval'])

            interval = timedelta(days=interval[3], hours=interval[2], minutes=interval[1], seconds=interval[0])

    context.job_queue.run_repeating(
        remind, 
        interval,
        first=time(hour=start[2], minute=start[1], second=start[0]),
        last=None,
        data=reminder,
        name=str(update.message.from_user.id), 
        chat_id=update.effective_chat.id
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You will now start receiving reminders for the following task:\n\n"
             f"<b>{context.user_data['task']}</b>\n\n"
             "Edit this task at anytime using the /edit command.",
        parse_mode='HTML'
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

async def list_tasks(update: Update, context: ContextTypes) -> None:
    """Display a user's tasks."""
    tasks = ""
    user_id = str(update.message.from_user.id)

    for i, job in enumerate(context.job_queue.get_jobs_by_name(user_id)):
        tasks += f"{i+1}. {job.data['task']}\n"
        i += 1
    
    if tasks == "":
        tasks = "No active tasks"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Active tasks:\n{tasks}"
    )

async def unknown(update: Update, context: ContextTypes) -> None:
    """Display unknown command error message."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I don't understand that command.\n\n"
             "Use /help to see a list of available commands."
    )