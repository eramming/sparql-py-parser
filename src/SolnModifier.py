from .Expressions import Expression
from typing import Dict, List, Any, Tuple
from uuid import uuid4

class SolnModifier:

    def __init__(self):
        self.group_clause: GroupClause = None
        self.having_clause: HavingClause = None
        self.order_clause: OrderClause = None
        self.limit_offset_clause: LimitOffsetClause = None

    def set_group_clause(self, group_clause: 'GroupClause') -> None:
        self.group_clause = group_clause
    
    def set_having_clause(self, having_clause: 'HavingClause') -> None:
        self.having_clause = having_clause
    
    def set_order_clause(self, order_clause: 'OrderClause') -> None:
        self.order_clause = order_clause
    
    def set_limit_offset_clause(self, limit_offset_clause: 'LimitOffsetClause') -> None:
        self.limit_offset_clause = limit_offset_clause

    def __str__(self):
        gc: str = f"{self.group_clause} " if self.group_clause else ""
        hc: str = f"{self.having_clause} " if self.having_clause else ""
        oc: str = f"{self.order_clause} " if self.order_clause else ""
        loc: str = f"{self.limit_offset_clause}" if self.limit_offset_clause else ""
        return f"{gc}{hc}{oc}{loc}".rstrip() + "\n"
    
    def __format__(self, format_spec):
        return self.__str__()
    

class GroupClause:

    def __init__(self):
        self.expressions: Dict[str, Expression] = {}
        self.derived_vars: Dict[str, str] = {}
        self.vars: Dict[str, str] = {}
        self.order_of_elements: List[str] = []

    def add_expr(self, expr: Expression) -> None:
        uuid: str = uuid4()
        self.order_of_elements.append(uuid)
        self.expressions[uuid] = expr

    def add_derived_var(self, var: str, expr: Expression) -> None:
        uuid: str = uuid4()
        self.order_of_elements.append(uuid)
        self.derived_vars[uuid] = f"({expr} AS {var})"

    def add_var(self, var: str) -> None:
        uuid: str = uuid4()
        self.order_of_elements.append(uuid)
        self.vars[uuid] = var

    def is_empty(self) -> bool:
        return len(self.expressions) + len(self.derived_vars) + len(self.vars) == 0
    
    def stringified_elements_in_order(self) -> List[Any]:
        all_elements: Dict[str, Any] = self.expressions | self.derived_vars | self.vars
        return [str(all_elements[uuid]) for uuid in self.order_of_elements]
    
    def in_order_derived_vars

    def __str__(self):
        if self.is_empty():
            return ""
        return f"GROUP BY {' '.join(self.stringified_elements_in_order())}"
    
    def __format__(self, format_spec):
        return self.__str__()


class HavingClause:

    def __init__(self, expressions: List[Expression] = []):
        self.expressions: List[Expression] = expressions

    def add_expr(self, expr: Expression) -> None:
        self.expressions.append(expr)

    def __str__(self):
        if len(self.expressions) == 0:
            return ""
        return f"HAVING {' '.join([str(ex) for ex in self.expressions])}"
    
    def __format__(self, format_spec):
        return self.__str__()


class OrderClause:

    def __init__(self, expressions: List[Expression] = []):
        self.expressions: List[Expression] = expressions

    def add_expr(self, expr: Expression) -> None:
        self.expressions.append(expr)

    def is_empty(self) -> bool:
        return len(self.expressions) == 0

    def __str__(self):
        if len(self.expressions) == 0:
            return ""
        return f"ORDER BY {' '.join([str(ex) for ex in self.expressions])}"
    
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
