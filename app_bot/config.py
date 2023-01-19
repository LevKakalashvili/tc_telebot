import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        scr_folder = os.getenv("SCREENSHOT_FOLDER")

        if scr_folder is None or not scr_folder:
            if not os.path.isdir("screenshots_default"):
                os.mkdir("screenshots_default")
            scr_folder = os.path.join(os.getcwd(), "screenshots_default")

        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        self.SCREENSHOT_FOLDER = scr_folder
        self.SCREENSHOT_RESOLUTION_WIDTH = int(
            str(os.getenv("SCREENSHOT_RESOLUTION_WIDTH"))
        )
        self.SCREENSHOT_RESOLUTION_HEIGHT = int(
            str(os.getenv("SCREENSHOT_RESOLUTION_HEIGHT"))
        )
