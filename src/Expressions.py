from .ExprOp import ExprOp
from .tokens import QueryTerm
from typing import List
from uuid import uuid4


class Expression:
    def __init__(self) -> None:
        self._id = uuid4()

    def __hash__(self) -> int:
        return hash(self._id)

    def __eq__(self, value) -> bool:
        if isinstance(value, Expression):
            return value._id == self._id
        return False


# Covers Booleans, Numbers, Strings, Irirefs, Variables
class TerminalExpr(Expression):

    def __init__(self, stringified_val: str, is_quoted: bool = False):
        super().__init__()
        self.stringified_val: str = stringified_val
        self.is_quoted: bool = is_quoted

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        if self.is_quoted:
            return f"\"{self.stringified_val}\""
        return self.stringified_val

class NegationExpr(Expression):

    def __init__(self, expr: Expression):
        super().__init__()
        self.expr: Expression = expr

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        return f"!{self.expr}"


class MultiExprExpr(Expression):

    def __init__(self, l_expr: Expression, r_expr: Expression, expr_op: ExprOp):
        super().__init__()
        self.l_expr: Expression = l_expr
        self.r_expr: Expression = r_expr
        self.expr_op: ExprOp = expr_op

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        return f"{self.l_expr} {self.expr_op.value} {self.r_expr}"


class Function(Expression):

    def __init__(self, func_name: str = None, args: List[Expression] = []):
        super().__init__()
        self.func_name: str = func_name
        self.args: List[Expression] = args

    def add_arg(self, exp: Expression) -> None:
        self.args.append(exp)

    def set_func_name(self, func_name: str) -> None:
        self.func_name = func_name

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        arg_str: str = ", ".join([str(expr) for expr in self.args])
        return f"{self.func_name.upper()}({arg_str})"


class AggregateFunction(Function):

    def __init__(self, func_name: str, arg: Expression,
                 is_distinct: bool = False):
        super().__init__(func_name, [arg])
        self.is_distinct: bool = is_distinct

    def set_distinct_flag(self) -> None:
        self.is_distinct = True

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        distinct: str = "DISTINCT " if self.is_distinct else ""
        return f"{self.func_name.upper()}({distinct}{self.args[0]})"
    

class GroupConcatFunction(AggregateFunction):

    def __init__(self, arg: Expression, is_distinct: bool = False,
                 separator: str = None):
        super().__init__(QueryTerm.GROUP_CONCAT.value, arg, is_distinct)
        self.separator = separator

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        distinct: str = "DISTINCT " if self.is_distinct else ""
        separator_str: str = f"; SEPARATOR=\"{self.separator}\"" if self.separator else ""
        return f"{self.func_name.upper()}({distinct}{self.args[0]}{separator_str})"


class IdentityFunction(Function):

    def __init__(self, arg: Expression):
        super().__init__("", [arg])

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        return f"({self.args[0]})"


# class NumberLiteralExpr(Expression):

#     def __init__(self, literal: float):
#         self.literal: float = literal


# class StringLiteralExpr(Expression):

#     def __init__(self, literal: str):
#         self.literal: str = literal


# class BoolLiteralExpr(Expression):

#     def __init__(self, literal: bool):
#         self.literal: bool = literal
