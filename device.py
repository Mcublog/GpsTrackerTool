#!/usr/bin/env python3

from abc import abstractmethod
from dataclasses import dataclass
from queue import Queue
from typing import Protocol
from threading import Thread

class Command(Protocol):
    channel: int
    datatx: bytes
    datarx: bytes

    def serialize(self) -> bytes:
        ...

    @staticmethod
    def deserialize(raw: bytes) -> 'Command':
        ...

class Adapter(Protocol):

    @abstractmethod
    def connect(self) -> bool:
        ...

    @abstractmethod
    def disconnect(self) -> bool:
        ...

    @abstractmethod
    def write(self, data: bytes) -> int:
        ...

    @abstractmethod
    def read(self) -> bytes:
        ...

@dataclass
class Device:
    adapter: Adapter
    _queue: Queue
    _polling: Thread

    def run(self):
        self.adapter.connect()

    def stop(self):
        pass

    def send(self, cmd: Command) -> bool:
        pass


# send bytes -> command_t -> encode -> to port
# polling
# getting bytes -> decode -> command_t -> call handler by id

# connect
# write -> polling -> call handler

# table of handlers for each channel
