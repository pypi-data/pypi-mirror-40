import pytest

from uttut.pipeline.ops import op_factory as default_op_factory
from uttut.elements import Datum, Intent, Entity
from ..pipe import Pipe
from .mock_factory import mock_factory


@pytest.fixture
def fake_pipe():
    p_custom = Pipe(mock_factory)
    p_custom.add('Str2Str', {})
    p_custom.add('Str2Lst', {})
    p_custom.add('Lst2Lst', {})
    return p_custom


def test_pipe_init_use_correct_factory():
    p = Pipe()
    assert p.operator_factory == default_op_factory
    p_custom = Pipe(mock_factory)
    assert p_custom.operator_factory == mock_factory


def test_pipe_fails_to_add():
    p = Pipe(mock_factory)
    p.add('Lst2Lst')
    with pytest.raises(TypeError):
        p.add('Str2Str')


def test_transform(fake_pipe):
    datum = Datum(
        utterance='123',
        intents=[Intent(1)],
        entities=[
            Entity(label=1, start=0, end=1, value='1'),
            Entity(label=2, start=1, end=2, value='2'),
            Entity(label=3, start=2, end=3, value='3'),
        ],
    )
    output_seq, intent_labels, entity_labels, realigner = fake_pipe.transform(datum)

    assert output_seq == ['1', '2', '3']
    assert intent_labels == [1]
    assert entity_labels == [1, 2, 3]

    output = realigner(entity_labels)
    assert output == [1, 2, 3]


def test_serialization():
    p_custom = Pipe(mock_factory)
    p_custom.add('Str2Str', {'1': 1})

    serialized_str = p_custom.serialize()
    o_pipe = Pipe.deserialize(serialized_str, mock_factory)

    assert p_custom == o_pipe
