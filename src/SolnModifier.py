from .Expressions import Expression
from typing import Tuple, List

class SolnModifier:

    def __init__(self, group_clause: 'GroupClause', having_clause: 'HavingClause',
                 order_clause: 'OrderClause', limit_offset_clause: 'LimitOffsetClause'):
        self.group_clause: GroupClause = group_clause
        self.having_clause: HavingClause = having_clause
        self.order_clause: OrderClause = order_clause
        self.limit_offset_clause: LimitOffsetClause = limit_offset_clause

    def __str__(self):
        return f"{self.group_clause} {self.having_clause} {self.order_clause} {self.limit_offset_clause}"
    
    def __format__(self, format_spec):
        return self.__str__()
    

class GroupClause:

    def __init__(self):
        self.built_in_calls: List[Expression] = []
        self.derived_vars: List[Tuple[str, Expression]] = []
        self.vars: List[str] = []

    def add_built_in_call(self, built_in_call: Expression) -> None:
        self.built_in_calls.append(built_in_call)

    def add_derived_var(self, var: str, expr: Expression) -> None:
        self.derived_vars.append((var, expr))

    def add_var(self, var: str) -> None:
        self.vars.append(var)

    def is_empty(self) -> bool:
        return len(self.built_in_calls) + len(self.derived_vars) + len(self.vars) == 0

    def __str__(self):
        output: str = (f"GROUP BY {' '.join(self.built_in_calls)} "
                       f"{' '.join(self.derived_vars)} "
                       f"{' '.join(self.vars)}")
        return output
    
    def __format__(self, format_spec):
        return self.__str__()


class HavingClause:

    def __init__(self, expr: List[Expression] = []):
        self.expr: List[Expression] = expr

    def add_expr(self, expr: Expression) -> None:
        self.expr.append(expr)

    def __str__(self):
        return f"HAVING {' '.join(self.expr)}"
    
    def __format__(self, format_spec):
        return self.__str__()


class OrderClause:

    def __init__(self, expr: List[Expression] = []):
        self.expr: List[Expression] = expr

    def add_expr(self, expr: Expression) -> None:
        self.expr.append(expr)

    def is_empty(self) -> bool:
        return len(self.expr) == 0

    def __str__(self):
        return f"ORDER BY {' '.join(self.expr)}"
    
    def __format__(self, format_spec):
        return self.__str__()


class LimitOffsetClause:

    def __init__(self, limit: int, offset: int, limit_first: bool):
        self.limit = limit
        self.offset = offset
        self.limit_first = limit_first

    def __str__(self):
        if self.limit is None:
            return f"OFFSET {self.offset}"
        elif self.offset is None:
            return f"LIMIT {self.limit}"
        elif self.limit_first:
            return f"LIMIT {self.limit} OFFSET {self.offset}"
        else:
            return f"OFFSET {self.offset} LIMIT {self.limit}"
    
    def __format__(self, format_spec):
        return self.__str__()
