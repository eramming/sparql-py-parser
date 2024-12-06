from typing import List, Tuple, Set
from src import Expression

class SelectClause:

    def __init__(self) -> None:
        self.explicit_vars: Set[str] = set()
        self.derived_vars: List[Tuple[Expression, str]] = []
        self.is_distinct = False
        self.is_select_all = False

    def make_distinct(self) -> None:
        self.is_distinct = True

    def set_select_all(self) -> None:
        self.is_select_all = True

    def add_derived_var(self, expression: Expression, new_var: str) -> None:
        self.derived_vars.append((expression, new_var))

    def add_explicit_var(self, var: str) -> None:
        self.explicit_vars.add(var)
