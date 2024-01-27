from dataclasses import dataclass, field

import tracker.protocol.cobs.message as msg
from tracker.adapter import Command


@dataclass
class TrackerCommand(Command):
    _channel: int = field(init=False)
    _paylod: bytes = field(init=False)
    _timeout_ms: int = field(default=100)
    version: int = field(default=0)

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
        return msg.serialize(
            msg.Message(channel=self._channel,
                        version=self.version,
                        data=self._paylod))

    @staticmethod
    def deserialize(raw: bytes) -> 'Command':
        cmsg = msg.deserialize(raw)
        cmd = TrackerCommand(version=cmsg.version)
        cmd.channel = cmsg.channel
        cmd.paylod = cmsg.data
        return cmd
