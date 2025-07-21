import logging
import os

from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from handlers.start import start_command, show_teachers_callback, teacher_info_callback

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("8009133089:AAEg5N6v_CF46jot2ppx2t7zfKPPa-p6wTs").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(show_teachers_callback, pattern="^show_teachers$"))
    application.add_handler(CallbackQueryHandler(teacher_info_callback, pattern="^teacher_\\d+$"))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
