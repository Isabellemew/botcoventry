import telebot
from telebot import types
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

# Replace with your actual token
TOKEN = '8009133089:AAEg5N6v_CF46jot2ppx2t7zfKPPa-p6wTs'
bot = telebot.TeleBot(TOKEN)

# Frequently Asked Questions
FAQ = [
    {
        'keywords': ['documents', 'apply', 'application', 'required documents'],
        'answer': 'You will need: passport, photo, diploma with transcript, IELTS certificate, and UNT results.'
    },
    {
        'keywords': ['english', 'language', 'ielts', 'requirement'],
        'answer': 'For Foundation: IELTS 5.0–5.5. For Master\'s: IELTS 6.5 or higher.'
    },
    {
        'keywords': ['programs', 'majors', 'foundation', 'bachelor'],
        'answer': 'Foundation: Business, Computer Science, Economics & Finance, International Relations.\nBachelor: Marketing, Management, International Business, Computer Science, Artificial Intelligence.'
    },
    {
        'keywords': ['scholarship', 'gpa', 'essay', 'olympiad'],
        'answer': 'GPA ≥ 4.0, IELTS ≥ 6.0. Two stages: achievement review + essay/olympiad. UNT ≥ 50 by June.'
    },
    {
        'keywords': ['tuition', 'cost', 'price', 'fee'],
        'answer': 'Tuition fee: 10,000,000 KZT per year.'
    },
    {
        'keywords': ['dorm', 'accommodation', 'housing', 'campus'],
        'answer': 'Yes, a student dormitory is available on the Astana campus.'
    },
    {
        'keywords': ['mobility', 'exchange', 'study abroad'],
        'answer': 'Yes, academic mobility programs are available with Coventry University UK.'
    },
    {
        'keywords': ['apply', 'how to apply', 'submit', 'application process'],
        'answer': 'Apply online: choose your program, upload documents, and pay the registration fee.'
    },
    {
        'keywords': ['contact', 'email', 'phone', 'website'],
        'answer': 'Email: admissions@coventry.edu.kz\nPhone: +7xxxxxxxxx\nWebsite: https://coventry.edu.kz'
    },
]

# Create custom keyboard
def create_faq_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "What documents do I need?",
        "English language requirements?",
        "Available programs?",
        "How to get a scholarship?",
        "Tuition cost?",
        "Is there a dormitory?",
        "Is academic mobility available?",
        "How to apply?",
        "Contact info"
    ]
    keyboard.add(*[types.KeyboardButton(text) for text in buttons])
    return keyboard

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Hello! I'm the admission bot for Coventry University Astana. Choose a question or type your own.",
        reply_markup=create_faq_keyboard()
    )

# Handle text messages
@bot.message_handler(content_types=['text'])
def answer_faq(message):
    user_text = message.text.lower()
    for item in FAQ:
        if any(keyword in user_text for keyword in item['keywords']):
            bot.send_message(message.chat.id, item['answer'])
            return 
    bot.send_message(message.chat.id, "Sorry, I can't answer this question yet. Contact the admin.")

# Run the bot
bot.polling(none_stop=True)