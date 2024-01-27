#!/usr/bin/env python3

import ctypes as ct

import serial
from cobs import cobsr

from tracker.protocol.commands.reports import GetReportsV1

DataPointer = ct.POINTER(ct.c_uint8)

class CMessageHeader(ct.Structure):
    _pack_ = 1
    _fields_ = [
        ('channel', ct.c_uint32),
        ('size', ct.c_uint32),
        ('version', ct.c_uint32),
    ]
class CMessage(ct.Structure):
    _pack_ = 1
    _fields_ = [
        ('channel', ct.c_uint32),
        ('size', ct.c_uint32),
        ('version', ct.c_uint32),
        ('data', DataPointer),
    ]


class Message:

    @staticmethod
    def len() -> int:
        return ct.sizeof(CMessageHeader)

    @staticmethod
    def serialize(channel: int, version:int, data: bytes | None) -> bytes:
        size = Message.len() if data is None else len(data) + Message.len()
        msg = CMessage(channel=channel, size=size, version=version)
        buffer = (ct.c_uint8 * size)()
        ct.memmove(ct.addressof(buffer), ct.addressof(msg), Message.len())
        if data is not None:
            ct.memmove(ct.addressof(buffer) + Message.len(), data, len(data))
        return cobsr.encode(bytes(buffer)) + b'\x00'

    @staticmethod
    def deserialize(raw: bytes) -> bytes:
        # remove /x00
        size = len(raw) - 1
        decoded = cobsr.decode(raw[:size])
        decoded += b'\x00' * (size - len(decoded))
        cmsg = CMessageHeader.from_buffer_copy(decoded)
        return decoded


def main():
    # raw =  b"\002\v\001\001\002\024\001\001\002\026\001\001\002\001\001\001\002\002\001\001\00"
    # # \x02\x08\x01\x01\x01\x01\x01\x01\x00'
    # # raw = b'\x02\x08\x01\x01\x02\x04\x01\x01\x00'
    # v = Message.deserialize(raw)
    # print(v)

    port = "/dev/ttyS10"
    get_report = GetReportsV1()
    msg = Message.serialize(channel=0, version=0, data=bytes(get_report))
    with serial.Serial(port, timeout=0.5) as ser:
        ser.write(msg)
        print(ser.read(100))


if __name__ == "__main__":
    main()
