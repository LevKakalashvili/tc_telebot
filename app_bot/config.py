import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    SCREENSHOT_FOLDER = str(os.getenv("SCREENSHOT_FOLDER"))
    SCREENSHOT_RESOLUTION_WIDTH = int(str(os.getenv("SCREENSHOT_RESOLUTION_WIDTH")))
    SCREENSHOT_RESOLUTION_HEIGHT = int(str(os.getenv("SCREENSHOT_RESOLUTION_HEIGHT")))
