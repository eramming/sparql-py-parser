from .SelectQuery import SelectQuery
from .Prologue import Prologue

class Query:

    def __init__(self,
                 prologue: Prologue,
                 select_query: SelectQuery) -> None:
        self.prologue: Prologue = prologue
        self.select_query: SelectQuery = select_query

    def __str__(self):
        pro_str = "" if self.prologue.is_empty() else f"{self.prologue}\n\n"
        return f"{pro_str}{self.select_query}"
    
    def __format__(self, format_spec):
        return self.__str__()
