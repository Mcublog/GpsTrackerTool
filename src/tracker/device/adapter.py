from abc import abstractmethod
from typing import Protocol

from tracker.protocol.command import Command


class Adapter(Protocol):

    @abstractmethod
    def connect(self) -> bool:
        ...

    @abstractmethod
    def disconnect(self) -> bool:
        ...

    @abstractmethod
    def write(self, command: Command) -> int:
        ...

    @abstractmethod
    def read(self) -> Command:
        ...
