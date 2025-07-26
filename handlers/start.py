from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
import sqlite3
from telegram.ext import CallbackContext
from teachers_info import teachers
import json
from datetime import datetime, timedelta
import os

EVENTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'events.json')

def load_events():
    if not os.path.exists(EVENTS_FILE):
        return []
    with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_actual_events():
    events = load_events()
    now = datetime.utcnow()
    two_weeks_ago = now - timedelta(weeks=2)
    actual = [e for e in events if datetime.fromisoformat(e['date']) >= two_weeks_ago]
    return actual

async def start_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    conn = sqlite3.connect('applicants.db')
    c = conn.cursor()
    c.execute("SELECT name FROM applicants WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    if result:
        # Пользователь уже зарегистрирован, показываем главное меню
        keyboard = [
            [InlineKeyboardButton("Teachers", callback_data='show_teachers')],
            [InlineKeyboardButton("Events", callback_data='show_events')],
            [InlineKeyboardButton("Register", callback_data='register')],
            [InlineKeyboardButton("See my rank", callback_data='see_rank')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Welcome back! Choose an option:', reply_markup=reply_markup)
    else:
        context.user_data['state'] = 'enter_name'
        await update.message.reply_text("Please enter your name in English:")

async def show_teachers_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for idx, t in enumerate(teachers):
        keyboard.append([InlineKeyboardButton(f"{t['title']} {t['name']}", callback_data=f"teacher_{idx}")])
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Choose a teacher:", reply_markup=reply_markup
    )

async def teacher_info_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    idx = int(query.data.split('_')[1])
    t = teachers[idx]
    info = f"{t['title']} {t['name']}\nCountry: {t['country']}\nRole: {t.get('role', '—')}\nExperience: {t.get('experience', '—')}"
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="show_teachers")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.answer()
    await query.edit_message_text(info, reply_markup=reply_markup)

async def show_events_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = get_actual_events()
    if events:
        text = '\n\n'.join([e['text'] for e in events])
    else:
        text = 'No upcoming events announced yet.'
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text, reply_markup=reply_markup
    )

async def back_to_main_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Teachers Information", callback_data="show_teachers")],
        [InlineKeyboardButton("Event Announcements", callback_data="show_events")],
        [InlineKeyboardButton("Register", callback_data='register')],
        [InlineKeyboardButton("See my rank", callback_data='see_rank')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Hello! I am CoventryBot 💬",
        reply_markup=reply_markup
    )
