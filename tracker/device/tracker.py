import logging
from dataclasses import dataclass, field
from queue import Queue
from threading import Event, Lock, Thread

from tracker.interface import Adapter, Command

# from tracker.protocol.tables import TablesByChannel

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

@dataclass
class Tracker:
    adapter: Adapter
    # tables: TablesByChannel

    _queue: Queue = field(init=False, repr=False)
    _polling: Thread = field(init=False, repr=False)
    _kill_evt: Event = field(init=False, repr=False)
    _mutex: Lock = field(init=False, default_factory=Lock)

    def __post_init__(self):
        self._queue = Queue()
        self._kill_evt = Event()
        self._polling = Thread(target=self._port_handler,
                                      name='port_handling')

    def run(self):
        self.adapter.connect()

        self._polling.start()

    def stop(self):
        self.adapter.disconnect()
        self._kill_evt.set()
        self._polling.join()

    def send(self, cmd: Command) -> bool:
        self._queue.put_nowait(cmd)
        return True

    def _port_handler(self):
        while not self._kill_evt.wait(0.001):
            if self._queue.empty():
                continue
            with self._mutex:
                command:Command = self._queue.get_nowait()
                self.adapter.write(command)
                if not (command := self.adapter.read()):
                    continue
                log.info(f"{command}")
