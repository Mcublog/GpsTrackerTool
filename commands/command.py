#!/usr/bin/env python3

from typing import Protocol


class Command(Protocol):
    channel: int
    paylod: bytes
    timeout_ms: int

    def serialize(self) -> bytes:
        ...

    @staticmethod
    def deserialize(raw: bytes) -> 'Command':
        ...
