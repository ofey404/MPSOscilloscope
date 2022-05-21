from typing import Callable


from queue import Queue


class Pool:
    """Pre-allocated object pool."""

    def __init__(self, size: int, initalizer: Callable, doResizeIfShould: Callable):
        self.available = [initalizer() for _ in range(size)]
        self.doResizeIfShould = doResizeIfShould

    def retire(self, block):
        self.available.append(block)

    def alloc(self):
        if self.available:
            block = self.available.pop()
            return self.doResizeIfShould(block)
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
            # Use _get(): Discard last item, without notifying other threads.
            self.onKick(self._get())
        super().put(item, block=block, timeout=timeout)
