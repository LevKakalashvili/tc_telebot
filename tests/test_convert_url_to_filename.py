import os

import pytest

from app_bot.utils import Screenshot


@pytest.mark.parametrize(
    "url, expected_result",
    [
        (
            "https://yandex.ru/search/?from=chromesearch&clid=2196598&text=wildberries&lr=11083",
            {
                "nt": "httpsyandex.rusearchfrom=chromesearch&clid=2196598&text=wildberries&lr=11083",
                "posix": "https:yandex.rusearch?from=chromesearch&clid=2196598&text=wildberries&lr=11083"
            }
            ,
        ),
        (
            "https://docs.pytest.org/en/7.1.x/how-to/index.html",
            {
                "nt": "httpsdocs.pytest.orgen7.1.xhow-toindex.html",
                "posix": "https:docs.pytest.orgen7.1.xhow-toindex.html"
            },
        ),
        (
            "https://www.ozon.ru/category/dom-i-sad-14500/",
            {
                "nt": "httpswww.ozon.rucategorydom-i-sad-14500",
                "posix": "https:www.ozon.rucategorydom-i-sad-14500"
            },
        ),
    ],
)
def test_convert_url_to_filename(url, expected_result):
    assert Screenshot.convert_url_to_filename(url) == expected_result[os.name]