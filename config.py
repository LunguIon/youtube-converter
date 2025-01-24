import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TEMP_DOWNLOAD_PATH = os.getenv("TEMP_DOWNLOAD_PATH", "temp_files/")  # Default path if not set