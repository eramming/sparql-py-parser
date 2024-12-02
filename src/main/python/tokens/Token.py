from tokens import QueryTerm

class Token:
    def __init__(self, term: QueryTerm, content: str = None) -> None:
        self.term: QueryTerm = term
        self.content: str = content
