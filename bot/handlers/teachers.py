from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def teachers_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with a button to get teacher info."""
    keyboard = [
        [InlineKeyboardButton("Получить информацию о преподавателе", callback_data='get_teacher_info')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Нажмите на кнопку, чтобы получить информацию о преподавателе:', reply_markup=reply_markup)


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
        f"Имя: {teacher_info['name']}\n"
        f"Email: {teacher_info['email']}\n"
        f"Телефон: {teacher_info['phone']}\n"
        f"Кабинет: {teacher_info['office']}\n"
        f"Факультет: {teacher_info['department']}\n"
        f"Научные интересы: {teacher_info['research_interests']}\n"
        f"Часы приема: {teacher_info['office_hours']}\n"
        f"Биография: {teacher_info['biography']}\n"
        f"Публикации: {teacher_info['publications']}"
    )

    await query.edit_message_text(text=f"Информация о преподавателе:\n\n{info_text}") 