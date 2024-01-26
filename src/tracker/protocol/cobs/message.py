#!/usr/bin/env python3

import ctypes as ct

import serial
from cobs import cobsr

from tracker.protocol.commands.reports import GetReportsV1

DataPointer = ct.POINTER(ct.c_uint8)


class CMessage(ct.Structure):
    _pack_ = 1
    _fields_ = [
        ('size', ct.c_uint32),
        ('channel', ct.c_uint32),
        ('data', DataPointer),
    ]


class Message:

    @staticmethod
    def len() -> int:
        return ct.sizeof(CMessage) - ct.sizeof(DataPointer)

    @staticmethod
    def serialize(channel: int, data: bytes | None) -> bytes:
        size = Message.len() if data is None else len(data) + Message.len()
        msg = CMessage(size=size, channel=channel)
        buffer = (ct.c_uint8 * size)()
        ct.memmove(ct.addressof(buffer), ct.addressof(msg), Message.len())
        if data is not None:
            ct.memmove(ct.addressof(buffer) + Message.len(), data, len(data))
        return cobsr.encode(bytes(buffer)) + b'\x00'


def main():
    port = "/dev/ttyS10"
    get_report = GetReportsV1()
    msg = Message.serialize(channel=0, data=bytes(get_report))
    with serial.Serial(port, timeout=0.5) as ser:
        ser.write(msg)


if __name__ == "__main__":
    main()
