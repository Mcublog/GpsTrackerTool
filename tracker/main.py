#!/usr/bin/env python3
import logging
import time

from pylogus import logger_init

from tracker.device.serial_adapter import SerialPortAdapter
from tracker.device.tracker import Tracker
from tracker.protocol.cobs.tracker_command import TrackerCommand
from tracker.protocol.commands.reports import GetReportsV1

log = logger_init(__name__, logging.INFO)

def main():
    adapter = SerialPortAdapter("/dev/ttyS10", 115200, False)
    tracker = Tracker(adapter=adapter)

    cmd = TrackerCommand(version=0)
    cmd.channel = 0
    cmd.paylod = bytes(GetReportsV1())

    tracker.run()
    tracker.send(cmd)

    for _ in range(1):
        time.sleep(1)
        log.info("...")

if __name__ == "__main__":
    main()

# send bytes -> command_t -> encode -> to port
# polling
# getting bytes -> decode -> command_t -> call handler by id

# connect
# write -> polling -> call handler

# table of handlers for each channel
