import pytest

from ..ops.base import Operator
from ..step import Step


class MockedOperator(Operator):

    def __init__(self, state=None):
        super().__init__('in', 'out')
        self.state = state

    def transform(self, input_sequence, labels):
        pass


@pytest.fixture
def step():
    yield Step(MockedOperator())


def test_equal(step):
    assert step != Step(MockedOperator('123'))
    assert step != ()


def test_transform(step, mocker):
    mock_method = mocker.patch.object(step.op, 'transform')
    step.transform('abc', [1, 2, 3])
    mock_method.assert_called_once_with(input_sequence='abc', labels=[1, 2, 3])


def test_attributes(step):
    assert MockedOperator().input_type == step.input_type
    assert MockedOperator().output_type == step.output_type
