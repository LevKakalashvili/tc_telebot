from app_bot.utils import Screenshot
from app_bot.config import Config as AppConfig

import pytest


@pytest.mark.parametrize(
    "url, expected_result",
    [
        ("1234", (False, {"file": "", "message": "\n\nАдрес сайта (url) должен быть в формате:\nhttps://url\nhttp://url"})),
        (123, (False, {"file": "", "message": "\n\nАдрес сайта (url) должен быть в формате:\nhttps://url\nhttp://url"})),
        ("ya.ru", (False, {"file": "", "message": "\n\nАдрес сайта (url) должен быть в формате:\nhttps://url\nhttp://url"})),
        ("www.ya.ru", (False, {"file": "", "message": "\n\nАдрес сайта (url) должен быть в формате:\nhttps://url\nhttp://url"})),
        ("", (False, {"file": "", "message": "\n\nАдрес сайта (url) должен быть в формате:\nhttps://url\nhttp://url"})),
        (
            "https://yandex.ru/search/?from=chromesearch&clid=2196598&text=wildberries&lr=11083",
            (True, {"file": "File.png", "message": ""}),
        ),
    ],
)
def test_get_screenshot(url, expected_result):
    test_screenshot_maker = Screenshot(app_config=AppConfig())
    assert test_screenshot_maker.get_screenshot(url, "File.png") == expected_result






