from .SelectQuery import SelectQuery
from .Prologue import Prologue

class Query:

    def __init__(self,
                 prologue: Prologue,
                 select_query: SelectQuery) -> None:
        self.prologue: Prologue = prologue
        self.select_query: SelectQuery = select_query

    def __str__(self):
        return f"{self.prologue}{self.select_query}"
    
    def __format__(self, format_spec):
        return self.__str__()
