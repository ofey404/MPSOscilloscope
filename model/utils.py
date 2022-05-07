from tkinter import W
from typing import Callable
from dataclasses import dataclass


from queue import Queue
from PyQt5.QtCore import QMutex, QMutexLocker


class Pool:
    """Pre-allocated object pool."""

    def __init__(self, size: int, initalizer: Callable):
        self.available = [initalizer() for _ in range(size)]

    def retire(self, block):
        self.available.append(block)

    def alloc(self):
        if self.available:
            return self.available.pop()
        raise Exception("Pool should not expire!")


class LeakQueue(Queue):
    """Thread safe FIFO queue.
       Kick last item when putting into full LeakQueue.
    """

    def __init__(self, maxsize: int, onKick: Callable = None) -> None:
        super().__init__(maxsize)
        self.onKick = onKick

    def put(self, item, block=True, timeout=None):
        if self.full() and (self.onKick is not None):
            self.onKick(self.get())  # Discard last item.
        super().put(item, block=block, timeout=timeout)
