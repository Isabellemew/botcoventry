from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from teachers_info import teachers

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Информация о преподавателях", callback_data="show_teachers")],
        [InlineKeyboardButton("Event Announcements", callback_data="show_events")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я — CoventryBot 💬",
        reply_markup=reply_markup
    )

async def show_teachers_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for idx, t in enumerate(teachers):
        keyboard.append([InlineKeyboardButton(f"{t['title']} {t['name']}", callback_data=f"teacher_{idx}")])
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Выберите преподавателя:", reply_markup=reply_markup
    )

async def teacher_info_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    idx = int(query.data.split('_')[1])
    t = teachers[idx]
    info = f"{t['title']} {t['name']}\nСтрана: {t['country']}\nРоль: {t.get('role', '—')}\nОпыт: {t.get('experience', '—')}"
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="show_teachers")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.answer()
    await query.edit_message_text(info, reply_markup=reply_markup)

async def show_events_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "No upcoming events announced yet.", reply_markup=reply_markup
    )
