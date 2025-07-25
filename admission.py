import telebot

TOKEN = '8009133089:AAEg5N6v_CF46jot2ppx2t7zfKPPa-p6wTs'
bot = telebot.TeleBot(TOKEN)

def make_inline_keyboard(buttons, row_width=2):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=row_width)
    for btn in buttons:
        keyboard.add(telebot.types.InlineKeyboardButton(btn['text'], callback_data=btn['callback']))
    return keyboard

MAIN_MENU_INLINE = [
    {"text": "🎓 Admission", "callback": "admission"}
]

ADMISSION_MENU_INLINE = [
    {"text": "📚 Programmes", "callback": "specialties"},
    {"text": "📝 Requirements", "callback": "requirements"},
    {"text": "📅 Application Stages", "callback": "stages"},
    {"text": "📄 Download Guide (PDF)", "callback": "guide"},
    {"text": "🔙 Back to Main Menu", "callback": "main"}
]

SPECIALTIES_MENU_INLINE = [
    {"text": "📝 Requirements", "callback": "requirements"},
    {"text": "📅 Application Stages", "callback": "stages"},
    {"text": "🔙 Back", "callback": "admission"}
]

REQUIREMENTS_MENU_INLINE = [
    {"text": "📚 Programmes", "callback": "specialties"},
    {"text": "📅 Application Stages", "callback": "stages"},
    {"text": "🔙 Back", "callback": "admission"}
]

STAGES_MENU_INLINE = [
    {"text": "📚 Programmes", "callback": "specialties"},
    {"text": "📝 Requirements", "callback": "requirements"},
    {"text": "🔙 Back", "callback": "admission"}
]

@bot.message_handler(commands=['admission'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 <b>Welcome to Coventry Foundation!</b>\n\n"
        "Please select a section 👇",
        reply_markup=make_inline_keyboard(MAIN_MENU_INLINE),
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "main")
def callback_main(call):
    bot.edit_message_text(
        "👋 <b>Main Menu:</b>\n\nPlease select a section 👇",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=make_inline_keyboard(MAIN_MENU_INLINE),
        parse_mode="HTML"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "admission")
def callback_admission(call):
    bot.edit_message_text(
        "🎓 <b>Admission</b>\n\nPlease choose an option:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=make_inline_keyboard(ADMISSION_MENU_INLINE),
        parse_mode="HTML"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "specialties")
def callback_specialties(call):
    text = (
        "🎓 <b>Available Programmes:</b>\n"
        "────────────────────────────\n"
        "• 📢 Advertising and Digital Marketing\n"
        "• 💼 Business Management\n"
        "• 🌍 International Business\n"
        "• 🏢 Business Administration\n"
        "• 💻 Computer Science\n"
        "• 🤖 Computer Science with AI\n"
        "• 📊 Information Technology Management\n"
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
        "📝 <b>Scholarship Requirements:</b>\n"
        "────────────────────────────\n"
        "• IELTS: <b>from 6.0</b> (no less than 5.0 in each section)\n"
        "• GPA: <b>from 4.0</b>\n"
        "• Graduation: <b>2025</b>\n"
        "• Olympiad participation is welcome\n"
        "────────────────────────────\n\n"
        "💰 <b>For paid tuition:</b>\n"
        "────────────────────────────\n"
        "• IELTS: <b>from 5.0</b>\n"
        "• High school certificate + transcript\n"
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
        "📅 <b>Application Stages</b>\n"
        "────────────────────────────\n"
        "🔹 <b>Stage I:</b> 24 February — 26 March 2025\n"
        " • IELTS, GPA, and olympiad check\n"
        "🔹 <b>Stage II:</b> 27 March — 5 April 2025\n"
        " • Essay review\n"
        "────────────────────────────\n"
        "📍 <b>Apply now:</b>\n"
        "🌐 <a href='https://www.coventry.edu.kz'>www.coventry.edu.kz</a>\n"
        "🏢 Astana, Korgalzhyn Highway, 13A"
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
    bot.send_message(call.message.chat.id, "📥 <b>Guide download:</b>", parse_mode="HTML")
    with open("file/grants-kaz.pdf", "rb") as pdf1:
        bot.send_document(call.message.chat.id, pdf1, caption="Guide in Kazakh 🇰🇿")
    with open("file/grants-ru.pdf", "rb") as pdf2:
        bot.send_document(call.message.chat.id, pdf2, caption="Guide in Russian 🇷🇺")

bot.polling()