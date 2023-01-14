import datetime
import json
import os

from selenium.common import WebDriverException
from selenium.webdriver import DesiredCapabilities

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from app_bot.config import Config as AppConfig


class Screenshot:
    def __init__(self):
        options = Options()
        options.headless = True
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

        self._web_driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=options,
            desired_capabilities=capabilities,
        )
        self._web_driver.set_window_size(
            AppConfig.SCREENSHOT_RESOLUTION_WIDTH,
            AppConfig.SCREENSHOT_RESOLUTION_HEIGHT,
        )

        self.file = ""
        self.status_code = 0
        self.message = ""

    def make_sreeenshot(self, url: str) -> bool:
        if self.__get_screenshot(url):
            self.__get_status_code(url)
            return True
        self._web_driver.quit()
        return False

    def __get_screenshot(self, url: str) -> bool:
        self.file = ""
        self.status_code = -1
        self.message = "Не удалось создать скриншот для url."

        try:
            self._web_driver.get(url)
        except WebDriverException:
            return False

        filename = os.path.join(
            AppConfig.SCREENSHOT_FOLDER,
            f'{self.__reformat_datetime_string(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M"))}_'
            f"{self.__reformat_url(url)}.png",
        )
        if self._web_driver.save_screenshot(filename):
            self.file = filename
            self.status_code = 0
            self.message = ""
            return True
        else:
            return False

    def __get_status_code(self, url: str):
        for entry in self._web_driver.get_log("performance"):
            for key, val in entry.items():
                if key == "message" and "status" in val:
                    msg = json.loads(val)["message"]["params"]
                    for mes_key, mes_val in msg.items():
                        if mes_key == "response":
                            response_url = mes_val["url"]
                            response_status = mes_val["status"]
                            if response_url == url:
                                self.status_code = response_status
                                return None

    @staticmethod
    def __reformat_datetime_string(datetime_str: str) -> str:
        if os.name == "nt":
            return datetime_str.replace(":", "-")
        return datetime_str

    @staticmethod
    def __reformat_url(filename: str) -> str:
        if os.name == "nt":
            invalid_chars = r"\/:*?<>|"
            return "".join(char for char in filename if char not in invalid_chars)
        return filename


screenshot_maker = Screenshot()
