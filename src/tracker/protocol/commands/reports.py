import ctypes as ct

from tracker.protocol.commands.list import Commands


class GetReportsV1(ct.Structure):
    _pack_ = 1
    _fields_ = [
        ('cmdid', ct.c_uint32),
    ]

    def __init__(self):
        self.cmdid = Commands.CMDID_GET_REPORTS.value
