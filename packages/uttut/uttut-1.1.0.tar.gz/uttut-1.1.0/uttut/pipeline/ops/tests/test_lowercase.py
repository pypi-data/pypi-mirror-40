import pytest

from ..lowercase import Lowercase
from .common_tests import common_test, update_locals


@pytest.fixture
def op():
    yield Lowercase()


test_cases = [
    pytest.param(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        list(range(26)),
        "abcdefghijklmnopqrstuvwxyz",
        list(range(26)),
        id='all a-z',
    ),
    pytest.param(
        "薄餡亂入",
        [0, 1, 2, 3],
        "薄餡亂入",
        [0, 1, 2, 3],
        id='zh',
    ),
    pytest.param(
        "0123456789",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "0123456789",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        id='digits',
    ),
]


funcs = common_test(test_cases)
update_locals(locals(), funcs)


def test_equal(op):
    assert op == Lowercase()
