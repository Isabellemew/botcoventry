import sqlite3
import fitz  # PyMuPDF
import re
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Установка пути к языковым данным Tesseract (настройте под вашу систему)
os.environ["TESSDATA_PREFIX"] = "C:/Program Files/Tesseract-OCR/tessdata"  # Для Windows
# Для Linux: os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/4.00/tessdata"

async def start_command(update: Update, context: CallbackContext):
    context.user_data['state'] = 'enter_name'
    await update.message.reply_text("Please enter your name in English:")

async def text_handler(update: Update, context: CallbackContext):
    state = context.user_data.get('state')
    if state == 'enter_name':
        name = update.message.text.strip()
        # Проверка, что имя содержит только английские буквы и пробелы
        if not re.match(r'^[A-Za-z\s]+$', name):
            await update.message.reply_text("Please enter a valid name using only English letters and spaces.")
            return
        user_id = update.message.from_user.id
        conn = sqlite3.connect('applicants.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO applicants (user_id, name) VALUES (?, ?)", (user_id, name))
        conn.commit()
        conn.close()
        context.user_data['name'] = name
        context.user_data['state'] = 'choose_basis'
        keyboard = [
            [InlineKeyboardButton("Grant", callback_data='basis_grant')],
            [InlineKeyboardButton("Paid", callback_data='basis_paid')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Please choose your application basis:", reply_markup=reply_markup)

async def register_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    conn = sqlite3.connect('applicants.db')
    c = conn.cursor()
    c.execute("SELECT basis FROM applicants WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    if result:
        await query.answer()
        await query.message.reply_text("You are already registered.")
        return
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Grant", callback_data='basis_grant')],
        [InlineKeyboardButton("Paid", callback_data='basis_paid')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('Please choose your application basis:', reply_markup=reply_markup)

async def basis_choice_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    basis = 'grant' if query.data == 'basis_grant' else 'paid'
    user_id = query.from_user.id
    conn = sqlite3.connect('applicants.db')
    c = conn.cursor()
    c.execute("UPDATE applicants SET basis = ? WHERE user_id = ?", (basis, user_id))
    conn.commit()
    conn.close()
    context.user_data['basis'] = basis
    context.user_data['state'] = 'upload_ielts'
    await query.edit_message_text('Please upload your IELTS document (PDF).')

async def document_handler(update: Update, context: CallbackContext):
    state = context.user_data.get('state')
    if state not in ['upload_ielts', 'upload_ent']:
        await update.message.reply_text("Please start the registration process by selecting 'Register' from the main menu.")
        return
    document = update.message.document
    if document.mime_type != 'application/pdf':
        await update.message.reply_text("Please send a PDF file.")
        return
    file = await context.bot.get_file(document.file_id)
    file_path = f"documents/{document.file_id}.pdf"
    await file.download_to_drive(file_path)
    
    document_type = 'IELTS' if state == 'upload_ielts' else 'ENT'
    try:
        # Открываем PDF с помощью PyMuPDF
        doc = fitz.open(file_path)
        text = ""
        # Обрабатываем все страницы
        for page_num, page in enumerate(doc):
            logger.info(f"Processing page {page_num + 1} of {document_type} document")
            
            # Пытаемся извлечь текст без OCR
            page_text = page.get_text("text")
            logger.info(f"Text extracted without OCR (page {page_num + 1}): {page_text[:100]}...")
            
            if not page_text.strip():
                logger.info(f"No text found on page {page_num + 1}, performing OCR")
                # Выполняем OCR с указанием языка и высоким DPI
                lang = "eng" if document_type == 'IELTS' else "kaz"
                try:
                    tp = page.get_textpage_ocr(language=lang, dpi=600, fast=False, options="--psm 6")
                    page_text = page.get_text("text", textpage=tp)
                    logger.info(f"Text extracted with OCR (page {page_num + 1}): {page_text[:100]}...")
                except Exception as ocr_error:
                    logger.error(f"OCR failed on page {page_num + 1}: {str(ocr_error)}")
                    continue
            
            text += page_text
        
        doc.close()
        
        # Логируем полный текст
        logger.info(f"Full text for {document_type} document: {text}")
        
        # Извлекаем баллы из объединенного текста
        score = extract_score(text, document_type)
        logger.info(f"Score extracted for {document_type}: {score}")
        
        if score is not None:
            user_id = update.message.from_user.id
            with sqlite3.connect('applicants.db') as conn:
                c = conn.cursor()
                c.execute("INSERT OR REPLACE INTO documents (user_id, document_type, file_path, score) VALUES (?, ?, ?, ?)",
                          (user_id, document_type, file_path, score))
                conn.commit()
            if state == 'upload_ielts':
                context.user_data['state'] = 'upload_ent'
                await update.message.reply_text(f"IELTS document processed. Score: {score}. Please upload your ENT document (PDF).")
            elif state == 'upload_ent':
                # Рассчитываем средний балл
                with sqlite3.connect('applicants.db') as conn:
                    c = conn.cursor()
                    c.execute("SELECT score FROM documents WHERE user_id = ? AND document_type = 'IELTS'", (user_id,))
                    ielts_score = c.fetchone()[0]
                    c.execute("SELECT score FROM documents WHERE user_id = ? AND document_type = 'ENT'", (user_id,))
                    ent_score = c.fetchone()[0]
                    normalized_ent = (ent_score / 140) * 9  # Нормализация ЕНТ к шкале 0-9
                    total_score = (ielts_score + normalized_ent) / 2
                    c.execute("UPDATE applicants SET total_score = ? WHERE user_id = ?", (total_score, user_id))
                    conn.commit()
                context.user_data['state'] = 'completed'
                keyboard = [[InlineKeyboardButton("See my rank", callback_data='see_rank')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text("Documents processed. You can now see your rank.", reply_markup=reply_markup)
        else:
            await update.message.reply_text(f"Could not find score in {document_type} document.")
    except Exception as e:
        logger.error(f"Error processing {document_type} document: {str(e)}")
        await update.message.reply_text(f"Error processing {document_type} document: {str(e)}")
        return

def extract_score(text, document_type):
    try:
        if document_type == 'IELTS':
            # Ищем последовательность из пяти чисел с одной десятичной точкой
            match = re.search(r"(\d+\.\d)\s+(\d+\.\d)\s+(\d+\.\d)\s+(\d+\.\d)\s+(\d+\.\d)", text)
            return float(match.group(1)) if match else None
        elif document_type == 'ENT':
            match = re.search(r"(\d+)\s*Барлығы/Итого", text, re.IGNORECASE)
            return int(match.group(1)) if match else None
    except Exception as e:
        logger.error(f"Error in extract_score for {document_type}: {str(e)}")
        return None
    return None

async def see_rank_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    conn = sqlite3.connect('applicants.db')
    c = conn.cursor()
    # Получение основы пользователя
    c.execute("SELECT basis, total_score FROM applicants WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result is None:
        await query.message.reply_text("You are not registered yet.")
        conn.close()
        return
    basis, total_score = result
    # Получение ранжированного списка для основы пользователя
    c.execute("SELECT user_id FROM applicants WHERE basis = ? ORDER BY total_score DESC", (basis,))
    ranked = c.fetchall()
    rank = 1
    for row in ranked:
        if row[0] == user_id:
            break
        rank += 1
    conn.close()
    await query.message.reply_text(f"Your rank is {rank} in {basis} applicants.")

async def ranked_list(update: Update, context: CallbackContext):
    ADMIN_IDS = [123456789]  # Замените на реальные ID администраторов
    if update.message.from_user.id not in ADMIN_IDS:
        await update.message.reply_text("You do not have permission.")
        return
    conn = sqlite3.connect('applicants.db')
    c = conn.cursor()
    c.execute("SELECT user_id, name, total_score FROM applicants WHERE basis = 'grant' AND total_score IS NOT NULL ORDER BY total_score DESC")
    grant_ranked = c.fetchall()
    c.execute("SELECT user_id, name, total_score FROM applicants WHERE basis = 'paid' AND total_score IS NOT NULL ORDER BY total_score DESC")
    paid_ranked = c.fetchall()
    conn.close()
    message = "Grant Applicants:\n"
    for i, (user_id, name, total_score) in enumerate(grant_ranked, start=1):
        message += f"{i}. {name} (ID: {user_id}): total score {total_score:.2f}\n"
    message += "\nPaid Applicants:\n"
    for i, (user_id, name, total_score) in enumerate(paid_ranked, start=1):
        message += f"{i}. {name} (ID: {user_id}): total score {total_score:.2f}\n"
    await update.message.reply_text(message)