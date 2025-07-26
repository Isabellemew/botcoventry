import telebot
import psycopg2
from datetime import datetime
from telebot import types

API_TOKEN = '8014658275:AAGrOuAlv3OV4TGBC1PYZgRNQyDLFyBfTCM'
bot = telebot.TeleBot(API_TOKEN)

DB_CONFIG = {
    'dbname': 'coventry_bot',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': 5432,
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_all_clubs():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT name, category, description FROM clubs")
                return cur.fetchall()
    except Exception as e:
        print(f"[DB ERROR - Clubs] {e}")
        return []

def get_all_rooms():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT room_number, room_type, capacity FROM rooms")
                return cur.fetchall()
    except Exception as e:
        print(f"[DB ERROR - Rooms] {e}")
        return []

def book_room(club_name, room_number, date, start_time, end_time, booked_by):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM rooms WHERE room_number = %s", (room_number,))
                room = cur.fetchone()
                if not room:
                    return "❌ Room not found."

                room_id = room[0]

                # Проверка пересечения по времени
                cur.execute("""
                    SELECT 1 FROM bookings 
                    WHERE room_id = %s AND date = %s 
                    AND (start_time < %s AND end_time > %s)
                """, (room_id, date, end_time, start_time))

                if cur.fetchone():
                    return "⛔️ This room is already booked at that time."

                # Добавление бронирования
                cur.execute("""
                    INSERT INTO bookings (user_id, room_id, date, start_time, end_time, purpose, booked_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (0, room_id, date, start_time, end_time, f"{club_name} booking", booked_by))
                conn.commit()
                return "✅ Room booked successfully!"
    except Exception as e:
        print(f"[DB ERROR - Booking] {e}")
        return f"❌ Error: {e}"

# FAQ DATA
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

# Временное хранилище
user_data = {}

# === Команды ===

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📚 Clubs"),
        types.KeyboardButton("🏫 Rooms"),
        types.KeyboardButton("📝 Book"),
        types.KeyboardButton("📆 My Bookings"),
        types.KeyboardButton("❓ FAQ")
    )

    text = (
        "👋 <b>Welcome to the Coventry University Room Booking Bot!</b>\n\n"
        "Choose an option from the menu below or use a command:"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)


@bot.message_handler(commands=['clubs'])
def send_clubs(message):
    clubs = get_all_clubs()
    if not clubs:
        bot.send_message(message.chat.id, "❌ No clubs found.")
        return

    for name, category, desc in clubs:
        text = f"📌 <b>{name}</b>\nCategory: <i>{category}</i>\n<code>{desc}</code>"
        bot.send_message(message.chat.id, text, parse_mode="HTML")

@bot.message_handler(commands=['rooms'])
def send_rooms(message):
    rooms = get_all_rooms()
    if not rooms:
        bot.send_message(message.chat.id, "❌ No rooms available.")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for number, rtype, capacity in rooms:
        btn_text = f"{rtype} (Room {number}) — {capacity} ppl"
        markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"viewroom_{number}"))

    bot.send_message(message.chat.id, "🏫 <b>Available Rooms:</b>", reply_markup=markup, parse_mode="HTML")


@bot.message_handler(commands=['book'])
def book_start(message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    
    clubs = get_all_clubs()
    if not clubs:
        bot.send_message(message.chat.id, "❌ No clubs found.")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for name, category, _ in clubs:
        markup.add(types.InlineKeyboardButton(f"{name} ({category})", callback_data=f"club_{name}"))
    
    bot.send_message(message.chat.id, "📝 <b>Select your club:</b>", reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("club_"))
def handle_club_selection(call):
    user_id = call.from_user.id
    club_name = call.data[5:]
    user_data[user_id]['club'] = club_name

    rooms = get_all_rooms()
    if not rooms:
        bot.send_message(call.message.chat.id, "❌ No rooms found.")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for number, rtype, capacity in rooms:
        markup.add(types.InlineKeyboardButton(f"{rtype} (Room {number}) — {capacity} ppl", callback_data=f"room_{number}"))

    bot.edit_message_text("🏫 <b>Select a room:</b>", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("room_"))
def handle_room_selection(call):
    user_id = call.from_user.id
    room_number = call.data[5:]
    user_data[user_id]['room'] = room_number

    bot.edit_message_text("📅 Please enter the booking date (YYYY-MM-DD):", call.message.chat.id, call.message.message_id)
    bot.register_next_step_handler(call.message, get_date)

@bot.callback_query_handler(func=lambda call: call.data.startswith("viewroom_"))
def handle_room_detail(call):
    room_number = call.data.split("_")[1]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT room_type, capacity FROM rooms WHERE room_number = %s", (room_number,))
            room = cur.fetchone()

    if not room:
        bot.answer_callback_query(call.id, "❌ Room not found.")
        return

    room_type, capacity = room
    text = (
        f"🏫 <b>{room_type}</b>\n"
        f"Room Number: <b>{room_number}</b>\n"
        f"👥 Capacity: {capacity}"
    )
    bot.send_message(call.message.chat.id, text, parse_mode="HTML")


def get_date(message):
    user_id = message.from_user.id
    try:
        date = message.text.strip()
        datetime.strptime(date, "%Y-%m-%d")
        user_data[user_id]['date'] = date
                # Показать занятые слоты на эту дату
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT start_time, end_time FROM bookings
                    JOIN rooms ON bookings.room_id = rooms.id
                    WHERE rooms.room_number = %s AND date = %s
                    ORDER BY start_time
                """, (user_data[user_id]['room'], date))
                slots = cur.fetchall()

                if slots:
                    text = "⛔️ Busy time slots for this room:\n" + "\n".join([f"— {s[0]}–{s[1]}" for s in slots])
                else:
                    text = "✅ This room is free all day!"

                bot.send_message(message.chat.id, text)

        bot.send_message(message.chat.id, "⏰ Enter start time (HH:MM):")
        bot.register_next_step_handler(message, get_start_time)
    except:
        bot.send_message(message.chat.id, "❌ Invalid format. Try again (YYYY-MM-DD):")
        bot.register_next_step_handler(message, get_date)

def get_start_time(message):
    user_id = message.from_user.id
    try:
        start = message.text.strip()
        datetime.strptime(start, "%H:%M")
        user_data[user_id]['start'] = start
        bot.send_message(message.chat.id, "⏰ Enter end time (HH:MM):")
        bot.register_next_step_handler(message, get_end_time)
    except:
        bot.send_message(message.chat.id, "❌ Invalid time. Try again (HH:MM):")
        bot.register_next_step_handler(message, get_start_time)

def get_end_time(message):
    user_id = message.from_user.id
    try:
        end = message.text.strip()
        datetime.strptime(end, "%H:%M")
        user_data[user_id]['end'] = end

        start = user_data[user_id]['start']
        if datetime.strptime(end, "%H:%M") <= datetime.strptime(start, "%H:%M"):
            bot.send_message(message.chat.id, "❌ End time must be after start time. Try again (HH:MM):")
            bot.register_next_step_handler(message, get_end_time)
            return

        data = user_data[user_id]
        summary = (
            f"📝 <b>Confirm booking:</b>\n"
            f"Club: <b>{data['club']}</b>\n"
            f"Room: <b>{data['room']}</b>\n"
            f"Date: <b>{data['date']}</b>\n"
            f"Time: <b>{data['start']} - {data['end']}</b>"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Confirm", callback_data="confirm_booking"))
        markup.add(types.InlineKeyboardButton("❌ Cancel", callback_data="cancel_booking"))

        bot.send_message(message.chat.id, summary, parse_mode="HTML", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "❌ Invalid time. Try again (HH:MM):")
        bot.register_next_step_handler(message, get_end_time)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_booking")
def handle_confirm_booking(call):
    user_id = call.from_user.id
    data = user_data.get(user_id)
    if not data:
        bot.send_message(call.message.chat.id, "⚠️ Session expired.")
        return

    result = book_room(
        club_name=data['club'],
        room_number=data['room'],
        date=data['date'],
        start_time=data['start'],
        end_time=data['end'],
        booked_by=call.from_user.username or str(user_id)
    )

    bot.edit_message_text(result, call.message.chat.id, call.message.message_id, parse_mode="HTML")
    user_data.pop(user_id, None)

@bot.callback_query_handler(func=lambda call: call.data == "cancel_booking")
def handle_cancel(call):
    user_data.pop(call.from_user.id, None)
    bot.edit_message_text("❌ Booking cancelled.", call.message.chat.id, call.message.message_id)

@bot.message_handler(commands=['mybookings'])
def my_bookings(message):
    username = message.from_user.username or str(message.from_user.id)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT r.room_number, b.date, b.start_time, b.end_time, b.purpose
                FROM bookings b
                JOIN rooms r ON b.room_id = r.id
                WHERE b.booked_by = %s
                ORDER BY b.date, b.start_time
            """, (username,))
            rows = cur.fetchall()

    if not rows:
        bot.send_message(message.chat.id, "❌ You have no bookings.")
        return

    text = "<b>Your bookings:</b>\n\n"
    for room, date, start, end, purpose in rows:
        text += f"📅 {date} | Room {room} | ⏰ {start}–{end}\n📝 {purpose}\n\n"

    bot.send_message(message.chat.id, text, parse_mode="HTML")

# FAQ keyboard and handler
@bot.message_handler(func=lambda message: message.text == "❓ FAQ")
def handle_faq_button(message):
    bot.send_message(
        message.chat.id,
        "Choose a question or type your own:",
        reply_markup=create_faq_keyboard()
    )

@bot.message_handler(content_types=['text'])
def answer_faq(message):
    user_text = message.text.lower()
    for item in FAQ:
        if any(keyword in user_text for keyword in item['keywords']):
            bot.send_message(message.chat.id, item['answer'])
            return
    # fallback to booking/rooms/clubs/mybookings if button pressed
    if message.text in ["📚 Clubs", "🏫 Rooms", "📝 Book", "📆 My Bookings"]:
        # already handled by other handlers
        return
    bot.send_message(message.chat.id, "Sorry, I can't answer this question yet. Contact the admin +7xxxxx.")

# Запуск
if __name__ == '__main__':
    print("🤖 Bot is running...")
    bot.polling()
# Handle text messages
@bot.message_handler(content_types=['text'])
def answer_faq(message):
    user_text = message.text.lower()
    for item in FAQ:
        if any(keyword in user_text for keyword in item['keywords']):
            bot.send_message(message.chat.id, item['answer'])
            return 
    bot.send_message(message.chat.id, "Sorry, I can't answer this question yet. Contact the admin +7xxxxx.")

# Run the bot
bot.polling(none_stop=True)
