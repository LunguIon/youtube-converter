from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
from config import BOT_TOKEN
import re

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        f"Hi, {update.message.from_user.first_name}! 👋\n\n"
        f"I'm a bot that helps you download YouTube videos in MP3 or MP4 format. 🎵🎥\n"
        f"Just send me a valid YouTube link, and I'll take care of the rest! 🚀\n\n"
        f"If you need assistance, use the /help command for more information. 😊"
    )
def is_valid_youtube_url(url: str) -> bool:
    pattern = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=|embed/|v/|.+\?v=)?[a-zA-Z0-9_-]{11}"
    return re.match(pattern, url) is not None

async def validate_youtube_url(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.strip()

    if not user_message:
        await update.message.reply_text("It looks like you didn't send anything! Please send a valid YouTube link.")
        return

    try:
        if is_valid_youtube_url(user_message):
            await update.message.reply_text("✅ Valid link! Ready for download.")
        else:
            await update.message.reply_text(
                "❌ Invalid link! Please send a valid YouTube link.\n"
                "Examples:\n"
                "1️⃣ https://youtu.be/glUHA2mypNs\n"
                "2️⃣ https://youtu.be/msjhid1kTKM\n"
                "3️⃣ https://youtu.be/dh72Dz0OqLk?list=PL55PvHOtffL68eYjCLAK6fnv9kZ5XIVZs"
            )
    except Exception as e:
        await update.message.reply_text("❌ An error occurred while validating the link. Please try again later.")
        print(f"Error during validation: {e}")



async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"Comenzi disponibile:"
                                    f"\n/start - Salut!"
                                    f"\n/help - Lista comenzilor disponibile")

def main():
    try:
        application = Application.builder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))

        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, validate_youtube_url))

        application.run_polling()

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
