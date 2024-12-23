from typing import Dict, Set, List
from .Expressions import Expression
from collections import defaultdict

class SelectClause:

    def __init__(self) -> None:
        self.explicit_vars: Set[str] = set()
        self.derived_vars: Dict[str, Expression] = {}
        self.is_distinct = False
        self.is_select_all = False

    def make_distinct(self) -> None:
        self.is_distinct = True

    def set_select_all(self) -> None:
        self.is_select_all = True
        self.derived_vars = {}
        self.explicit_vars = set()

    def set_derived_var(self, var: str, expr: Expression) -> None:
        self.derived_vars[var] = expr
        self.is_select_all = False

    def add_explicit_var(self, var: str) -> None:
        self.explicit_vars.add(var)
        self.is_select_all = False

    def add_explicit_vars(self, vars: Set[str]) -> None:
        self.explicit_vars = self.explicit_vars.union(vars)
        self.is_select_all = False

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        distinct: str = "DISTINCT " if self.is_distinct else ""
        if self.is_select_all:
            return f"SELECT {distinct}*\n"
        ordered_vars: List[str] = sorted(self.explicit_vars.union(self.derived_vars.keys()))
        output = f"SELECT {distinct}"
        for var in ordered_vars:
            if var in self.derived_vars:
                output += f"({self.derived_vars[var]} AS {var})\n"
            else:
                output += f"{var}\n"
        return output
