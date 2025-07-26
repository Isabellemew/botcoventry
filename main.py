import logging
import os
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters
from handlers.start import (
    start_command,
    show_teachers_callback,
    teacher_info_callback,
    show_events_callback,
    back_to_main_callback,
)
from db import init_db
from handlers.registration import (
    text_handler,
    register_callback,
    basis_choice_callback,
    document_handler,
    see_rank_callback,
    ranked_list
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot."""
    # Create documents directory and initialize database
    if not os.path.exists('documents'):
        os.makedirs('documents')
    init_db()

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('BOT_TOKEN', '8009133089:AAEg5N6v_CF46jot2ppx2t7zfKPPa-p6wTs')).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    application.add_handler(CallbackQueryHandler(show_teachers_callback, pattern="^show_teachers$"))
    application.add_handler(CallbackQueryHandler(teacher_info_callback, pattern="^teacher_\\d+$"))
    application.add_handler(CallbackQueryHandler(show_events_callback, pattern="^show_events$"))
    application.add_handler(CallbackQueryHandler(back_to_main_callback, pattern="^back_to_main$"))
    application.add_handler(CallbackQueryHandler(register_callback, pattern="^register$"))
    application.add_handler(CallbackQueryHandler(basis_choice_callback, pattern="^basis_(grant|paid)$"))
    application.add_handler(CallbackQueryHandler(see_rank_callback, pattern="^see_rank$"))
    application.add_handler(MessageHandler(filters.Document.ALL, document_handler))
    application.add_handler(CommandHandler("ranked_list", ranked_list))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()