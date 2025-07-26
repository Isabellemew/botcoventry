from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def teachers_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with a button to get teacher info."""
    keyboard = [
        [InlineKeyboardButton("Get teacher information", callback_data='get_teacher_info')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Click the button to get teacher information:', reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()

    # Here you would typically look up the teacher's information in a database
    # For now, we'll just use a placeholder
    teacher_info = {
        "name": "Dr. John Smith",
        "email": "john.smith@coventry.ac.uk",
        "phone": "+44 24 7765 7688",
        "office": "EC2-14",
        "department": "School of Computing, Electronics and Maths",
        "research_interests": "Artificial Intelligence, Machine Learning, Natural Language Processing",
        "office_hours": "Mondays 10:00-12:00, Wednesdays 14:00-16:00",
        "biography": "Dr. Smith is a leading researcher in the field of AI...",
        "publications": "1. 'The Future of AI', 2022\n2. 'Deep Learning for Vision', 2021"
    }

    info_text = (
        f"Name: {teacher_info['name']}\n"
        f"Email: {teacher_info['email']}\n"
        f"Phone: {teacher_info['phone']}\n"
        f"Office: {teacher_info['office']}\n"
        f"Department: {teacher_info['department']}\n"
        f"Research interests: {teacher_info['research_interests']}\n"
        f"Office hours: {teacher_info['office_hours']}\n"
        f"Biography: {teacher_info['biography']}\n"
        f"Publications: {teacher_info['publications']}"
    )

    await query.edit_message_text(text=f"Teacher information:\n\n{info_text}")