import pytest

from ..token_to_index import Token2Index
from ..tokens import UNK_TOKEN
from .common_tests_for_pattern_to_token import pattern_to_token_tests


@pytest.fixture
def op():
    yield Token2Index({UNK_TOKEN: 0, '薄餡': 1, '要': 2, '帶': 3, '妹': 4})


test_cases = [
    pytest.param(
        ['薄餡', '要', '帶', '櫻花', '妹', '回來'],
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, 0, 4, 0],
        [1, 2, 3, 4, 5, 6],
        id='zh',
    ),
]

(
    test_data,
    test_transform,
    test_realign_labels,
    test_realign_labels_fails,
) = pattern_to_token_tests(test_cases)


@pytest.mark.parametrize(
    'error,token2index,unk_token',
    [
        pytest.param(
            ValueError, {'薄餡': 1, '要': 1, '帶': 3, '妹': 4}, UNK_TOKEN,
            id='duplicated indices',
        ),
        pytest.param(
            ValueError, {'薄餡': 0, '要': 2, '帶': 3, '妹': 4}, UNK_TOKEN,
            id='indices not continuous',
        ),
        pytest.param(
            KeyError, {'薄餡': 0, '要': 1, '帶': 2, '妹': 3}, UNK_TOKEN,
            id='token2index has no unk',
        ),
    ],
)
def test_invalid_token2index(error, token2index, unk_token):
    with pytest.raises(error):
        Token2Index(token2index=token2index, unk_token=unk_token)
