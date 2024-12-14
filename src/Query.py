from SelectQuery import SelectQuery
from Prologue import Prologue

class Query:

    def __init__(self,
                 prologue: Prologue,
                 select_query: SelectQuery) -> None:
        self.prologue: Prologue = prologue if prologue else Prologue()
        self.select_query: SelectQuery = select_query
