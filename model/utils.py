from typing import Callable
from dataclasses import dataclass


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


@dataclass
class Billboard:
    """Object for thread synchronization.

    Producer post block to billboard, then consumer take them away.
    """
    block = None
    mutex: QMutex = QMutex()

    def atomicSwap(self, block):
        with QMutexLocker(self.mutex):
            oldBlock = self.block
            self.block = block
        return oldBlock
