from dataclasses import dataclass

from tracker.protocol.cobs.message import Message
from tracker.protocol.command import Command


@dataclass
class TrackerCommand(Command):
    _channel: int
    _paylod: bytes
    _timeout_ms: int

    @property
    def channel(self) -> int:
        return self._channel

    @channel.setter
    def channel(self, channel: int):
        self._channel = channel

    @property
    def paylod(self) -> bytes:
        return self._paylod

    @paylod.setter
    def paylod(self, paylod: bytes):
        self._paylod = paylod

    @property
    def timeout_ms(self) -> int:
        return self._timeout_ms

    @timeout_ms.setter
    def timeout_ms(self, timeout_ms: int):
        self._timeout_ms = timeout_ms

    def serialize(self) -> bytes:
        return Message.serialize(self.channel, self.paylod)

    @staticmethod
    def deserialize(raw: bytes) -> 'Command':
        ...
