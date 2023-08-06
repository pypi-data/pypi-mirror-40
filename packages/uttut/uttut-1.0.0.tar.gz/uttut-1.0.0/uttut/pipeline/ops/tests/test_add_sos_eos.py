import pytest

from ..add_sos_eos import AddSosEos
from .common_tests_for_pattern_to_token import pattern_to_token_tests


@pytest.fixture
def op():
    yield AddSosEos()


test_cases = [
    pytest.param(
        ['alvin', '喜歡', '吃', '榴槤'],
        [1, 2, 3, 4],
        ['<sos>', 'alvin', '喜歡', '吃', '榴槤', '<eos>'],
        [0, 1, 2, 3, 4, 0],
        id='zh',
    ),
]

(
    test_data,
    test_transform,
    test_realign_labels,
    test_realign_labels_fails,
) = pattern_to_token_tests(test_cases)
