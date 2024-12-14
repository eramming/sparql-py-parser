from typing import Dict, Set
from Expressions import SelectExpr

class SelectClause:

    def __init__(self) -> None:
        self.explicit_vars: Set[str] = set()
        self.derived_vars: Dict[str, SelectExpr] = []
        self.is_distinct = False
        self.is_select_all = False

    def make_distinct(self) -> None:
        self.is_distinct = True

    def set_select_all(self) -> None:
        self.is_select_all = True

    def set_derived_var(self, var: str, expr: SelectExpr) -> None:
        self.derived_vars[var] = expr

    def add_explicit_var(self, var: str) -> None:
        self.explicit_vars.add(var)
