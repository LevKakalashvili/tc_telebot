import datetime
import os

from validators import url as validate_url, ValidationFailure

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from app_bot.config import Config as AppConfig


options = Options()
options.headless = True
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.set_window_size(AppConfig.SCREENSHOT_RESOLUTION_WIDTH, AppConfig.SCREENSHOT_RESOLUTION_HEIGHT)


def is_valid_url(url: str) -> bool:
    res = validate_url(url)
    if isinstance(res, ValidationFailure):
        return False
    return res


def get_screenshot(url: str) -> str | None:
    driver.get(url)
    filename = os.path.join(AppConfig.SCREENSHOT_FOLDER,
                            f'{reformat_datetime_string(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M"))}_'
                            f'{reformat_url(url)}.png')
    if not driver.save_screenshot(filename):
        filename = None

    driver.quit()
    return filename


def reformat_datetime_string(datetime: str) -> str:
    if os.name == "nt":
        return datetime.replace(":", "-")
    return datetime


def reformat_url(filename: str) -> str:
    if os.name == "nt":
        invalid_chars = r"\/:*?<>|"
        return "".join(char for char in filename if char not in invalid_chars)
    return filename
