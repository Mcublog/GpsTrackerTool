#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Handler:
    cmdid: int
    handler: Callable[[bytes], Any]

@dataclass
class TablesByChannel:
    tables:tuple[tuple[Handler,...],]

def test_handler(data:bytes) -> bytes:
    print(f"test_handler get {data}")
    return b''

def main():

    handler_list = []
    for i in range(5):
        handler_list.append(Handler(cmdid=i, handler=test_handler))
    tables = TablesByChannel(tables=(tuple(handler_list),))
    print(tables)

    channel = 0
    cmdid = 1
    data = b'122342'

    tables.tables[channel][cmdid].handler(data)


if __name__ == "__main__":
    main()