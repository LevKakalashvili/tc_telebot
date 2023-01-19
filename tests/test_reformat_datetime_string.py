import os

import pytest

from app_bot.utils import Screenshot


@pytest.mark.parametrize(
    "date_time, expected_result",
    [
        (
            "2022-13-14_15:88",
            "2022-13-14_15-88",
        ),
        ("", ""),
    ],
)
def test_reformat_datetime_string(date_time, expected_result):
    if os.name == "nt":
        assert Screenshot.reformat_datetime_string(date_time) == expected_result
    else:
        assert True
