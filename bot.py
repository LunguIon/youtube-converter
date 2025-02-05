import io
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler
import re
from config import BOT_TOKEN
import os


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
            context.user_data['youtube_url'] = user_message

            keyboard = [
                [
                    InlineKeyboardButton("Download as MP3 🎵", callback_data="download_mp3"),
                    InlineKeyboardButton("Download as MP4 🎥", callback_data="download_mp4"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                "✅ Valid link! Please choose a format to download:",
                reply_markup=reply_markup
            )
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


async def download_mp3(youtube_url: str, save_path: str):
    try:
        ydl_opts = {
            'outtmpl': f'{save_path}%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '0',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        return True
    except Exception as e:
        print(f"Error downloading MP3: {e}")
        return False


# async def download_mp4(youtube_url: str, save_path: str):
#     try:
#         ydl_opts = {
#             'outtmpl': f'{save_path}%(title)s.mp4',
#             'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
#             'merge_output_format': 'mp4',
#         }
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([youtube_url])
#         return True
#     except Exception as e:
#         print(f"Error downloading MP4: {e}")
#         return False


async def download_video(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    youtube_url = context.user_data.get('youtube_url')
    save_path = 'downloads/'

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    if not youtube_url:
        await query.edit_message_text("❌ Link not found! Please send a valid YouTube link again.")
        return

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            title = info_dict.get('title', 'unknown')

        if query.data == "download_mp3":
            await query.edit_message_text("🔄 Downloading MP3 format...")
            success = await download_mp3(youtube_url, save_path)
            file_extension = "mp3"
        # elif query.data == "download_mp4":
        #     await query.edit_message_text("🔄 Downloading MP4 format...")
        #     success = await download_mp4(youtube_url, save_path)
        #     file_extension = "mp4"
        else:
            await query.edit_message_text("❌ Invalid selection!")
            return

        if success:
            file_path = f"{save_path}{title}.{file_extension}"
            with open(file_path, 'rb') as file:
                await query.message.reply_document(document=file, filename=f"{title}.{file_extension}")
            await query.edit_message_text("✅ Download completed! File sent successfully.")
        else:
            await query.edit_message_text("❌ Download failed. Please try again later.")

    except Exception as e:
        await query.edit_message_text("❌ An error occurred. Please try again later.")
        print(f"Error: {e}")

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Available commands:"
        "\n/start - Start the bot and receive a welcome message."
        "\n/help - Get a list of available commands."
        "\n\nThis bot allows you to download YouTube videos as MP3 or MP4."
        "\nSimply send a YouTube link, and you will receive the file in your desired format."
    )



def main():
    try:
        application = Application.builder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, validate_youtube_url))
        application.add_handler(CallbackQueryHandler(download_video))

        application.run_polling()

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
