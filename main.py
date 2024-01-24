#!/usr/bin/env python3

from dataclasses import dataclass, field
from queue import Queue
from threading import Event, Lock, Thread

from commands.command import Command
from commands.tables import TablesByChannel
from device.adapter import Adapter


@dataclass
class Device:
    adapter: Adapter
    tables: TablesByChannel

    _queue: Queue
    _polling: Thread
    _kill_evt: Event = field(init=False, repr=False, default=Event())
    _mutex: Lock = field(init=False, default_factory=Lock)

    def run(self):
        self.adapter.connect()

    def stop(self):
        self.adapter.disconnect()

    def send(self, cmd: Command) -> bool:
        self._queue.put_nowait(cmd)
        return True

    def _port_handler(self):
        while not self._kill_evt.wait(0.001):
            if self._queue.empty():
                continue
            with self._mutex:
                command:Command = self._queue.get_nowait()
                self.adapter.write(command)
                command = self.adapter.read()
                print(f"{command}")



# send bytes -> command_t -> encode -> to port
# polling
# getting bytes -> decode -> command_t -> call handler by id

# connect
# write -> polling -> call handler

# table of handlers for each channel
