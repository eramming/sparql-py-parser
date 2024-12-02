from tokens import Token
from queue import Queue

class Tokenizer:

    def __init__(self) -> None:
        pass

    def tokenize(self, query_str: str) -> Queue[Token]:
        raise NotImplementedError()
