import os
from uuid import uuid4

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from cleanup import schedule_cleanup
from recognizer import recognize_faces

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Get cleanup interval and max_age from environment variables, with defaults
CLEANUP_INTERVAL = int(os.environ.get("CLEANUP_INTERVAL", 3600))  # default: 1 hour
CLEANUP_MAX_AGE = int(os.environ.get("CLEANUP_MAX_AGE", 3600))    # default: 1 hour

# Start scheduled cleanup
schedule_cleanup(UPLOAD_FOLDER, interval=CLEANUP_INTERVAL, max_age=CLEANUP_MAX_AGE)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable not set")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    message_id = update.message.message_id

    # Reply to the photo with "checking" (👀)
    sent_message = await update.message.reply_text(
        "\U0001f440 Checking...",
        reply_to_message_id=message_id,
    )

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = os.path.join(UPLOAD_FOLDER, f"{uuid4().hex}.jpg")
    await file.download_to_drive(file_path)

    result = recognize_faces(file_path)

    # Edit the sent message with the result
    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=sent_message.message_id,
        text=result,
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("Bot is polling...")
    app.run_polling()
