from __future__ import annotations

from dataclasses import replace, dataclass
from datetime import date
from typing import Tuple, Sequence, TypeVar, Callable, cast

from financial_simulator.messages.message import Message
from financial_simulator.messages.state import State


def distribute_message(destination: str, state: State, message: Message) -> Tuple[State, Sequence[Message]]:
    if len(message.destination) > 0:
        if destination == message.destination[0]:
            return state.on_message(replace(message, destination=message.destination[1:]))
    return state, ()


def distribute_day(_destination: str, state: State, current_date: date) -> Tuple[State, Sequence[Message]]:
    return state.on_day(current_date)


def flatten_messages(message_sequences: Sequence[Tuple[str, Sequence[Message]]]) -> Sequence[Message]:
    return tuple(replace(message, source=(source,) + tuple(message.source))
                 for source, messages in message_sequences
                 for message in messages)


T = TypeVar('T')


@dataclass(frozen=True)
class Container(State):
    children: Sequence[Tuple[str, State]]

    def __distribute(self,
                     data: T,
                     messages: Sequence[Message],
                     distributor: Callable[[str, State, T],
                     Tuple[State, Sequence[Message]]]) -> Tuple[Container, Sequence[Message]]:
        children, message_sequences = zip(*((source, container), (source, messages)
                                            for source, (container, messages)
                                            in (source, distributor(source, container, data)
                                                for source, container
                                                in self.children)))
        return replace(self, children=children), tuple(messages) + tuple(flatten_messages(message_sequences))

    def on_day(self, current_date: date) -> Tuple[Container, Sequence[Message]]:
        # call the parent on_day method first
        state, messages = super().on_day(current_date)
        return cast(Container, state).__distribute(current_date, messages, distribute_day)

    def on_message(self, message: Message) -> Tuple[Container, Sequence[Message]]:
        # call the parent on_message method first
        state, messages = super().on_message(message)
        return cast(Container, state).__distribute(message, messages, distribute_message)
