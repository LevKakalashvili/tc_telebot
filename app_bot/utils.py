"""Модуль утилит."""
import datetime
import json
import os

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore

from app_bot.config import Config as AppConfig


class Screenshot:
    """Класс для создания скриншотов web-страниц."""

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

    def make_sreeenshot(self, url: str) -> bool:
        """Делает скриншот страницы.

            :return: True если скриншот создан, False в противном случае.
        """
        if self.__get_screenshot(url):
            self.__get_status_code(url)
            return True
        return False

    def __get_screenshot(self, url: str) -> bool:
        self.file = ""
        self.status_code = -1
        self.message = f"Не удалось создать скриншот для url:\n{url}"

        try:
            self._web_driver.get(url)
        except WebDriverException:
            self.message += "\n\nUrl должен быть в формате:\n https://url\nhttp://url"
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
        return False

    def __get_status_code(self, url: str):
        for entry in self._web_driver.get_log("performance"):
            for key, value in entry.items():
                if key == "message" and "status" in value:
                    msg = json.loads(value)["message"]["params"]
                    for mes_key, mes_val in msg.items():
                        if mes_key == "response":
                            response_url = mes_val.get("url")
                            response_status = mes_val.get("status")
                            if url in response_url:
                                self.status_code = response_status
                                return None


screenshot_maker = Screenshot()
