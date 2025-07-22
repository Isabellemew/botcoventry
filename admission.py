import telebot

TOKEN = '7664397142:AAEJXMN1Drmrojbhk66pyb8KjVmSt-PFvWk'
bot = telebot.TeleBot(TOKEN)

def make_inline_keyboard(buttons, row_width=2):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=row_width)
    for btn in buttons:
        keyboard.add(telebot.types.InlineKeyboardButton(btn['text'], callback_data=btn['callback']))
    return keyboard

MAIN_MENU_INLINE = [
    {"text": "🎓 Поступление", "callback": "admission"}
]

ADMISSION_MENU_INLINE = [
    {"text": "📚 Специальности", "callback": "specialties"},
    {"text": "📝 Требования", "callback": "requirements"},
    {"text": "📅 Этапы отбора", "callback": "stages"},
    {"text": "📄 Скачать гайд (PDF)", "callback": "guide"},
    {"text": "🔙 Назад главное меню", "callback": "main"}
]

SPECIALTIES_MENU_INLINE = [
    {"text": "📝 Требования", "callback": "requirements"},
    {"text": "📅 Этапы отбора", "callback": "stages"},
    {"text": "🔙 Назад", "callback": "admission"}
]

REQUIREMENTS_MENU_INLINE = [
    {"text": "📚 Специальности", "callback": "specialties"},
    {"text": "📅 Этапы отбора", "callback": "stages"},
    {"text": "🔙 Назад", "callback": "admission"}
]

STAGES_MENU_INLINE = [
    {"text": "📚 Специальности", "callback": "specialties"},
    {"text": "📝 Требования", "callback": "requirements"},
    {"text": "🔙 Назад", "callback": "admission"}
]

@bot.message_handler(commands=['admission'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 <b>Добро пожаловать в Coventry Foundation!</b>\n\n"
        "Выберите интересующий раздел 👇",
        reply_markup=make_inline_keyboard(MAIN_MENU_INLINE),
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "main")
def callback_main(call):
    bot.edit_message_text(
        "👋 <b>Главное меню:</b>\n\nВыберите интересующий раздел 👇",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=make_inline_keyboard(MAIN_MENU_INLINE),
        parse_mode="HTML"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "admission")
def callback_admission(call):
    bot.edit_message_text(
        "🎓 <b>Поступление</b>\n\nВыберите действие:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=make_inline_keyboard(ADMISSION_MENU_INLINE),
        parse_mode="HTML"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "specialties")
def callback_specialties(call):
    text = (
        "🎓 <b>Доступные направления:</b>\n"
        "────────────────────────────\n"
        "• 📢 Реклама и цифровой маркетинг\n"
        "• 💼 Бизнес-менеджмент\n"
        "• 🌍 Международный бизнес\n"
        "• 🏢 Администрирование бизнеса\n"
        "• 💻 Компьютерные науки\n"
        "• 🤖 Компьютерные науки с ИИ\n"
        "• 📊 Управление информационными технологиями\n"
        "────────────────────────────"
    )
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=make_inline_keyboard(SPECIALTIES_MENU_INLINE),
        parse_mode="HTML"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "requirements")
def callback_requirements(call):
    text = (
        "📝 <b>Требования на ГРАНТ:</b>\n"
        "────────────────────────────\n"
        "• IELTS: <b>от 6.0</b> (не ниже 5.0 в каждой секции)\n"
        "• GPA: <b>от 4.0</b>\n"
        "• Выпуск: <b>2025 года</b>\n"
        "• Олимпиады приветствуются\n"
        "────────────────────────────\n\n"
        "💰 <b>Для платного обучения:</b>\n"
        "────────────────────────────\n"
        "• IELTS: <b>от 5.0</b>\n"
        "• Аттестат + транскрипт\n"
        "────────────────────────────"
    )
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=make_inline_keyboard(REQUIREMENTS_MENU_INLINE),
        parse_mode="HTML"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "stages")
def callback_stages(call):
    text = (
        "📅 <b>Этапы отбора</b>\n"
        "────────────────────────────\n"
        "🔹 <b>Этап I:</b> 24 февраля — 26 марта 2025\n"
        " • Проверка IELTS, GPA, олимпиад\n"
        "🔹 <b>Этап II:</b> 27 марта — 5 апреля 2025\n"
        " • Проверка эссе\n"
        "────────────────────────────\n"
        "📍 <b>Подать заявку:</b>\n"
        "🌐 <a href='https://www.coventry.edu.kz'>www.coventry.edu.kz</a>\n"
        "🏢 Астана, Коргалжынское шоссе, 13А"
    )
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=make_inline_keyboard(STAGES_MENU_INLINE),
        parse_mode="HTML"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "guide")
def callback_guide(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "📥 <b>Загрузка гайдов:</b>", parse_mode="HTML")
    with open("file/grants-kaz.pdf", "rb") as pdf1:
        bot.send_document(call.message.chat.id, pdf1, caption="Гайд на казахском 🇰🇿")
    with open("file/grants-ru.pdf", "rb") as pdf2:
        bot.send_document(call.message.chat.id, pdf2, caption="Гайд на русском 🇷🇺")

bot.polling()