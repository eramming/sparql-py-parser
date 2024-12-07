from .GroupGraphPattern import GroupGraphPattern
from typing import List

class Expression:
    def __init__(self) -> None:
        pass


class Function(Expression):

    def __init__(self, func_name: str = None, args: List[Expression] = []):
        self.func_name = func_name
        self.args = args

    def add_arg(self, exp: Expression) -> None:
        self.args.append(exp)

    def set_func_name(self, func_name: str) -> None:
        self.func_name = func_name

    def __format__(self, format_spec):
        arg_str: str = ", ".join(self.args)
        return f"{self.func_name.upper()}({arg_str})"
    
    def __str__(self):
        arg_str: str = ", ".join(self.args)
        return f"{self.func_name.upper()}({arg_str})"


class IdentityFunction(Function):

    def __init__(self, args: List[Expression] = []):
        super().__init__("", args)


class ExistenceExpr(Expression):

    def __init__(self, pattern: GroupGraphPattern, not_exists: bool = False):
        self.pattern: GroupGraphPattern = pattern
        self.not_exists: bool = not_exists

# Covers Booleans, Numbers, Strings, Irirefs, Variables
class TerminalExpr(Expression):

    def __init__(self, stringified_val: str):
        self.stringified_val: str = stringified_val


# class NumberLiteralExpr(Expression):

#     def __init__(self, literal: float):
#         self.literal: float = literal


# class StringLiteralExpr(Expression):

#     def __init__(self, literal: str):
#         self.literal: str = literal


# class BoolLiteralExpr(Expression):

#     def __init__(self, literal: bool):
#         self.literal: bool = literal
