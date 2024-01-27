from dataclasses import dataclass, field

import serial

from tracker.adapter import Adapter
from tracker.command import Command


@dataclass
class SerialPortAdapter(Adapter):
    portname: str
    baudrate: int
    ctsrts: bool = field(default=False)

    _serial: serial.Serial = field(init=False)

    def __post_init__(self):
        self._serial = serial.Serial(self.portname, baudrate=self.baudrate)

    def connect(self) -> bool:
        self._serial.open()
        return self._serial.is_open

    def disconnect(self) -> bool:
        if not self._serial.is_open:
            return False
        self._serial.close()
        return True

    def write(self, command: Command) -> int:
        ret = self._serial.write(command.serialize())
        return ret if ret is not None else 0

    def read(self) -> Command:
        raw = self._serial.read_until(b'\00')
        return Command.deserialize(raw)
