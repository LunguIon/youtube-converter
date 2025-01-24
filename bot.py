from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from config import BOT_TOKEN

# /start function
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"Hello, {update.message.from_user.first_name}!")

# /help function
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"Comenzi disponibile:"
                                    f"\n/start - Salut!"
                                    f"\n/help - Lista comenzilor disponibile")

def main():
    try:
        application = Application.builder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))

        application.run_polling()

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
