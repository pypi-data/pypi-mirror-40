import pytest

from ..char_tokenizer import CharTokenizer
from .common_tests_for_pattern_to_token import pattern_to_token_tests


@pytest.fixture
def op():
    yield CharTokenizer()


test_cases = [
    pytest.param(
        "GB亂入",
        [1, 1, 2, 2],
        ["G", "B", "亂", "入"],
        [1, 1, 2, 2],
        id='zh',
    ),
]

(
    test_data,
    test_transform,
    test_realign_labels,
    test_realign_labels_fails,
) = pattern_to_token_tests(test_cases)
