from queue import Queue

class LookaheadQueue(Queue):
    def __init__(self, maxsize: int = 0) -> None:
        super().__init__(maxsize)

    def lookahead(self):
        with self.mutex:
            if len(self.queue) > 0:
                return self.queue[0]
            return None
