import pytest

from ..pad import Pad
from ..tokens import PAD_TOKEN
from .common_tests_for_pattern_to_token import pattern_to_token_tests


@pytest.fixture
def op():
    yield Pad(5)


test_cases = [
    pytest.param(
        ['alvin', '喜歡', '吃', '榴槤', '!'],
        [1, 2, 3, 4, 5],
        ['alvin', '喜歡', '吃', '榴槤', '!'],
        [1, 2, 3, 4, 5],
        id='equal',
    ),
    pytest.param(
        ['alvin'],
        [1],
        ['alvin', PAD_TOKEN, PAD_TOKEN, PAD_TOKEN, PAD_TOKEN],
        [1, 0, 0, 0, 0],
        id='shorter',
    ),
]

(
    test_data,
    test_transform,
    test_realign_labels,
    test_realign_labels_fails,
) = pattern_to_token_tests(test_cases)


def test_longer_case(op):
    # labels are not invertible
    output_seq, output_labels, realigner = op.transform(
        ['alvin', '喜歡', '吃', '榴槤', '和', '蟲', '!'],
        [1, 2, 3, 4, 5, 6, 7],
    )
    assert ['alvin', '喜歡', '吃', '榴槤', '和'] == output_seq
    assert [1, 2, 3, 4, 5] == output_labels

    output = realigner([1, 2, 3, 4, 5])
    assert output == [1, 2, 3, 4, 5, 0, 0]
