#!/usr/bin/env python3

import ctypes as ct
from dataclasses import dataclass, field

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


@dataclass
class Message:
    channel: int
    # size with header
    size: int = field(init=False)
    version: int
    data: bytes = field(default=b'')

    def __post_init__(self):
        self.size = header_size() if self.data is None else len(
            self.data) + header_size()


def serialize(msg: Message) -> bytes:
    cmsg = CMessage(channel=msg.channel, size=msg.size, version=msg.version)
    buffer = (ct.c_uint8 * msg.size)()
    ct.memmove(ct.addressof(buffer), ct.addressof(cmsg), header_size())
    if msg.data is not None:
        ct.memmove(
            ct.addressof(buffer) + header_size(), msg.data, len(msg.data))
    return cobsr.encode(bytes(buffer)) + b'\x00'


def deserialize(raw: bytes) -> Message:
    # remove /x00
    size = len(raw) - 1
    decoded = cobsr.decode(raw[:size])
    decoded += b'\x00' * (size - len(decoded))
    cmsg = CMessageHeader.from_buffer_copy(decoded)
    return Message(channel=cmsg.channel,
                   version=cmsg.version,
                   data=decoded[header_size():])


def header_size() -> int:
    return ct.sizeof(CMessageHeader)


def main():
    # raw = b"\002\v\001\001\002\024\001\001\002\026\001\001\002\001\001\001\002\002\001\001\00"
    # v = deserialize(raw)
    # print(v)

    port = "/dev/ttyS10"
    get_report = GetReportsV1()
    msg = serialize(Message(channel=0, version=0, data=bytes(get_report)))
    with serial.Serial(port, timeout=0.5) as ser:
        ser.write(msg)
        if (raw := ser.read_until(b'\x00')) != b'':
            v = deserialize(raw)
            print(v)


if __name__ == "__main__":
    main()
