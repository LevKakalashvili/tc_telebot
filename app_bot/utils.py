"""Модуль утилит."""
import datetime
import json
import os

from config import Config as AppConfig
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore

invalid_chars = {"nt": r"\/:*?<>|", "posix": r"/"}


class Screenshot:
    """Класс для создания скриншотов web-страниц."""

    def __init__(self, app_config: AppConfig = None):
        if app_config is None:
            self.app_config = AppConfig()
        else:
            self.app_config = app_config

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
            self.app_config.SCREENSHOT_RESOLUTION_WIDTH,
            self.app_config.SCREENSHOT_RESOLUTION_HEIGHT,
        )

    @staticmethod
    def reformat_datetime_string(datetime_str: str) -> str:
        if os.name == "nt":
            return datetime_str.replace(":", "-")
        return datetime_str

    @staticmethod
    def convert_url_to_filename(filename: str) -> str:
        return "".join(
            char for char in filename if char not in invalid_chars.get(os.name, "")
        )

    def make_sreeenshot(self, url: str) -> tuple[bool, dict]:
        """Делает скриншот страницы и получает статус ответа от запрошенной страницы.

        :return: (success, result)
        success - True если скриншот создан, False в противном случае.
        result - {
        file - имя созданного файла,
        status_code - код ответа страницы
        message - сообщение
        }
        """
        success, result = self.get_screenshot(url)
        if success:
            code = self.get_status_code(url)
            result["status_code"] = "Unknown" if code <= 0 else code
            return True, result
        return False, result

    def get_screenshot(self, url: str) -> tuple[bool, dict]:
        """Делает скриншот страницы.

        :return: (success, result)
        success - True если скриншот создан, False в противном случае.
        result - {
        file - имя созданного файла,
        message - сообщение
        }
        """
        result = {"file": "", "message": f"Не удалось создать скриншот для url:\n{url}"}

        try:
            self._web_driver.get(url)
        except WebDriverException:
            result[
                "message"
            ] = "\n\nАдрес сайта (url) должен быть в формате:\nhttps://url\nhttp://url"
            return False, result

        filename = os.path.join(
            self.app_config.SCREENSHOT_FOLDER,
            f'{self.reformat_datetime_string(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M"))}_'
            f"{self.convert_url_to_filename(url)}.png",
        )
        if self._web_driver.save_screenshot(filename):
            result["file"] = filename
            result["message"] = ""
            return True, result
        return False, result

    def get_status_code(self, url: str) -> int:
        """Возвращает код ответа от url"""
        responses = []
        perf_log = self._web_driver.get_log("performance")
        for log_index in range(len(perf_log)):
            log_message = json.loads(perf_log[log_index]["message"])["message"]
            if log_message["method"] != "Network.responseReceived":
                continue
            responses.append(log_message["params"]["response"])

            if log_message["params"]["response"]["url"] != url:
                continue
            response = log_message["params"]["response"]
            return response["status"]
        return -1


screenshot_maker = Screenshot(app_config=AppConfig())
