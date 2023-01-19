import os

from dotenv import load_dotenv

load_dotenv()

scr_folder = os.getenv("SCREENSHOT_FOLDER")

if scr_folder is None or not scr_folder:
    if not os.path.isdir("screenshots_default"):
        os.mkdir("screenshots_default")
    scr_folder = os.path.join(os.getcwd(), "screenshots_default")


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    SCREENSHOT_FOLDER = scr_folder
    SCREENSHOT_RESOLUTION_WIDTH = int(str(os.getenv("SCREENSHOT_RESOLUTION_WIDTH")))
    SCREENSHOT_RESOLUTION_HEIGHT = int(str(os.getenv("SCREENSHOT_RESOLUTION_HEIGHT")))
