from enum import Enum, auto


class Commands(Enum):
    CMDID_SET_SETTINGS = 0x00
    CMDID_GET_SETTINGS = 0x01
    CMDID_SET_RTC = 0x02
    CMDID_GET_RTC = 0x03
    CMDID_GET_REPORTS = 0x04
    CMDID_STORAGE_CLEAR = 0x05
    CMDID_LAST = auto()
