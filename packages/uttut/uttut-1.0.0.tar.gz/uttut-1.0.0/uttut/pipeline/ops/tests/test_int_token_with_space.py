import pytest

from ..int_token_with_space import IntTokenWithSpace
from .common_tests_for_pattern_to_token import pattern_to_token_tests


@pytest.fixture
def op():
    yield IntTokenWithSpace()


test_cases = [
    pytest.param(
        "12 24 3666",
        [1, 1, 0, 2, 2, 0, 3, 3, 3, 3],
        " _int_   _int_   _int_ ",
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 3, 3, 3, 3, 3, 0],
        id='int int int',
    ),
    pytest.param(
        "12.3 1000 3.5",
        [1, 1, 1, 1, 0, 2, 2, 2, 2, 0, 3, 3, 3],
        "12.3  _int_  3.5",
        [1, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 3, 3, 3],
        id='float int float',
    ),
    pytest.param(
        "999",
        [0, 0, 0],
        " _int_ ",
        [0, 0, 0, 0, 0, 0, 0],
        id='int with label 0',
    ),
    pytest.param(
        "GB亂入",
        [1, 1, 2, 2],
        "GB亂入",
        [1, 1, 2, 2],
        id='identity',
    ),
    pytest.param(
        "GB亂入10次",
        [1, 1, 2, 2, 3, 3, 4],
        "GB亂入 _int_ 次",
        [1, 1, 2, 2, 0, 3, 3, 3, 3, 3, 0, 4],
        id='zh with int',
    ),
]

(
    test_data,
    test_transform,
    test_realign_labels,
    test_realign_labels_fails,
) = pattern_to_token_tests(test_cases)
