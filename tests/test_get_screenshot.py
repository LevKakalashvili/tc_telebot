import os

from app_bot.utils import Screenshot

import pytest


@pytest.mark.parametrize(
    "url, expected_result",
    [
        # ("1234", False),
        # (123, False),
        # ("ya.ru", False),
        # ("www.ya.ru", False),
        # ("", False),
        (
            "https://yandex.ru/search/?from=chromesearch&clid=2196598&text=wildberries&lr=11083",
            True,
        ),
    ],
)
def test_get_screenshot(url, expected_result):
    test_screenshot_maker = Screenshot()

    assert test_screenshot_maker.get_screenshot(url) == expected_result


@pytest.mark.parametrize(
    "url, expected_result",
    [
        (
            "https://yandex.ru/search/?from=chromesearch&clid=2196598&text=wildberries&lr=11083",
            True,
        ),
        (
            "https://yandex.ru/search/?from=chromesearch&clid=2196598&text=wildberries&lr=11083",
            Screenshot().reformat_url(
                "https://yandex.ru/search/?from=chromesearch&clid=2196598&text=wildberries&lr=11083"
            ),
        ),
    ],
)
def test_get_screenshot_check_file(url, expected_result):
    test_screenshot_maker = Screenshot()
    test_screenshot_maker.get_screenshot(url)
    scr_folder = os.path.isdir(os.path.join(os.getcwd(), "screenshots_default"))
    assert scr_folder == expected_result
    # assert test_screenshot_maker.file == expected_result
