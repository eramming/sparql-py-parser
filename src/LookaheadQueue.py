from queue import Queue
from typing import List
from collections import deque

class LookaheadQueue(Queue):
    def __init__(self, maxsize: int = 0) -> None:
        super().__init__(maxsize)

    def lookahead(self):
        with self.mutex:
            if len(self.queue) > 0:
                return self.queue[0]
            return None
        
    def get_now(self):
        return self.get(block=False)
    
    def get_all(self) -> List:
        with self.mutex:
            q_as_list: List = list(self.queue)
            self.queue = deque()
            return q_as_list
