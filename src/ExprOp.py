from enum import Enum

class ExprOp(Enum):
    MULT = "*"
    DIV = "/"
    ADD = "+"
    SUB = "-"
    NOT = "!"
    AND = "&&"
    OR = "||"
    EQUALS = "="
    LT = "<"
    GT = ">"
    G_OR_EQ = ">="
    L_OR_EQ = "<="
    NOT_EQ = "!="
