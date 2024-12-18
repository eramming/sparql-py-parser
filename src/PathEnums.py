from enum import Enum


class PathOp(Enum):
    OR = "|"
    SLASH = "/"


class PathMod(Enum):
    PLUS = "+"
    ASTERICK = "*"
    QUESTION_MARK = "?"
