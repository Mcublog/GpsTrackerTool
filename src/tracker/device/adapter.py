from curses import baudrate
from dataclasses import dataclass

import serial

from tracker.adapter import Adapter


@dataclass
class SerialPortAdapter(Adapter):
    portname: str
    baudrate: int
    ctsrts: bool

    _serial: serial.Serial
