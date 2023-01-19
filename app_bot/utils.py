"""Модуль утилит."""
import datetime
import json
import os

from .config import Config as AppConfig
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore

invalid_chars = {"nt": r"\/:*?<>|", "posix": r"/"}


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
    def reformat_datetime_string(datetime_str: str) -> str:
        if os.name == "nt":
            return datetime_str.replace(":", "-")
        return datetime_str

    @staticmethod
    def reformat_url(filename: str) -> str:
        return "".join(
            char for char in filename if char not in invalid_chars.get(os.name, "")
        )

    def make_sreeenshot(self, url: str) -> bool:
        """Делает скриншот страницы.

        :return: True если скриншот создан, False в противном случае.
        """
        if self.get_screenshot(url):
            self.get_status_code(url)
            return True
        return False

    def get_screenshot(self, url: str) -> bool:
        self.file = ""
        self.status_code = -1
        self.message = f"Не удалось создать скриншот для url:\n{url}"

        try:
            self._web_driver.get(url)
        except WebDriverException:
            self.message += (
                "\n\nАдрес сайта (url) должен быть в формате:\nhttps://url\nhttp://url"
            )
            return False

        filename = os.path.join(
            AppConfig.SCREENSHOT_FOLDER,
            f'{self.reformat_datetime_string(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M"))}_'
            f"{self.reformat_url(url)}.png",
        )
        if self._web_driver.save_screenshot(filename):
            self.file = filename
            self.status_code = 0
            self.message = ""
            return True
        return False

    def get_status_code(self, url: str) -> int:
        responses = []
        perf_log = self._web_driver.get_log("performance")
        for log_index in range(len(perf_log)):
            log_message = json.loads(perf_log[log_index]["message"])["message"]
            if log_message["method"] == "Network.responseReceived":
                responses.append(log_message["params"]["response"])
                if log_message["params"]["response"]["url"] == url:
                    response = log_message["params"]["response"]
                    self.status_code = response["status"]
                    return self.status_code
        return -1


screenshot_maker = Screenshot()
