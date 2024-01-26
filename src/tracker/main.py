#!/usr/bin/env python3

from dataclasses import dataclass, field
from queue import Queue
from threading import Event, Lock, Thread

from tracker.device.adapter import Adapter
from tracker.device.device import Device


def main():
    pass

if __name__ == "__main__":
    main()

# send bytes -> command_t -> encode -> to port
# polling
# getting bytes -> decode -> command_t -> call handler by id

# connect
# write -> polling -> call handler

# table of handlers for each channel
