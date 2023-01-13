from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    SCREENSHOT_FOLDER = os.getenv("SCREENSHOT_FOLDER")
    SCREENSHOT_RESOLUTION_WIDTH = int(os.getenv("SCREENSHOT_RESOLUTION_WIDTH"))
    SCREENSHOT_RESOLUTION_HEIGHT = int(os.getenv("SCREENSHOT_RESOLUTION_HEIGHT"))
