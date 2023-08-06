from typing import List

import json

from uttut.elements import Datum

from .ops.base import Realigner
from .step import Step
from .ops import op_factory as default_factory
from .utils import unpack_datum


class Pipe:

    def __init__(self, operator_factory=None):
        self._steps = []
        self._step_info = []

        self.operator_factory = operator_factory
        if self.operator_factory is None:
            self.operator_factory = default_factory

    def add(self, op_name: str, op_kwargs=None):
        """Add steps based on the operation name.

        This method creates a step, which has an op. The op
        is created.

        Args:
            op_name (str)
            op_kwargs (dict)

        Raises:
            KeyError

        """
        if op_kwargs is None:
            op_kwargs = {}

        op = self.operator_factory[op_name](**op_kwargs)
        step = Step(op)

        self._validate_steps(step)

        self._push_step(step)
        self._push_step_info(op_name, op_kwargs)

    def _validate_steps(self, step: Step):
        if len(self._steps) > 0:
            target_type = self._steps[-1].output_type
            in_type = step.input_type
            if in_type != target_type:
                raise TypeError(
                    "InputType of the step op is not valid."
                    f"Got {in_type}, but requires {target_type}")

    def _push_step(self, step: Step):
        self._steps.append(step)

    def _push_step_info(self, name: str, kwargs: dict):
        self._step_info.append(
            {  # for serialization
                'op_name': name,
                'op_kwargs': kwargs,
            },
        )

    def __eq__(self, other):
        same_op_factory = self.operator_factory == other.operator_factory
        same_steps = self._steps == other._steps
        same_step_info = self._step_info == other._step_info
        return same_op_factory and same_steps and same_step_info

    def transform(self, datum: Datum):
        """Process data based on Steps(Ops).

        This method processes datum according to the Pipe's steps.

        Arg:
            datum (Datum)

        Returns:
            output_sequence: transfromed sequence
            intent_labels (ints):
            entity_labels (ints):
            realigners: list of Realigners

        """
        input_sequence, intent_labels, entity_labels = unpack_datum(datum)

        realigners = RealignerSequence()
        for step in self._steps:
            input_sequence, entity_labels, realigner = step.transform(input_sequence, entity_labels)
            realigners.add(realigner)
        return input_sequence, intent_labels, entity_labels, realigners

    def serialize(self) -> str:
        return json.dumps(self._step_info)

    @classmethod
    def deserialize(cls, serialized_str: str, operator_factory=None) -> 'Pipe':
        pipe = cls(operator_factory)

        step_infos = json.loads(serialized_str)

        # restore steps
        for step_info in step_infos:
            pipe.add(
                op_name=step_info['op_name'],
                op_kwargs=step_info['op_kwargs'],
            )
        return pipe


class RealignerSequence:

    def __init__(self):
        self.collections = []

    def add(self, realigner: Realigner):
        """Append realigner into collections

        Arg:
            realigner: an instance of Realigner
        """
        self.collections.append(realigner)

    def __call__(self, labels: List[int]) -> List[int]:
        """Realign model prediction to its original input

        Arg:
            labels (ints): model prediction (entity)

        Return:
            ints: updated labels which has the same length as
                  original input (utterance)

        """
        for realigner in self.collections[::-1]:
            labels = realigner(labels)
        return labels
