from enum import Enum
from typing import List

NON_KEYWORD_TERMS: List[str] = [
    "IRIREF_CONTENT", "PREFIXED_NAME_PREFIX", "PREFIXED_NAME_LOCAL", "VARIABLE",
    "STRING_LITERAL", "U_NUMBER_LITERAL", "EOF"
]
BUILT_IN_CALLS: List[str] = [
    "COUNT", "SUM", "MIN", "MAX", "AVG", "SAMPLE", "GROUP_CONCAT", "REGEX",
    "SUBSTR", "REPLACE", "EXISTS", "NOT", "ABS", "CEIL", "FLOOR", "ROUND",
    "CONCAT", "STRLEN", "UCASE", "LCASE"
]
BRACKETTED_TERMS: List[str] = [
    "WHERE", "OPTIONAL", "UNION", "MINUS"
]
PARENTHIZED_TERMS: List[str] = [
    "SELECT", "DISTINCT", "FILTER", "BIND", "BY", "HAVING", "ASC", "DESC"
] + BUILT_IN_CALLS

class QueryTerm(Enum):
    RPAREN = ")"
    LPAREN = "("
    RBRACKET = "}"
    LBRACKET = "{"
    EXCLAMATION = "!"
    QUESTION = "?"
    CARAT = "^"
    PIPE = "|"
    BASE = "BASE"
    PREFIX = "PREFIX"
    IRIREF_CONTENT = "IRIREF_CONTENT"
    PREFIXED_NAME_PREFIX = "PREFIXED_NAME_PREFIX"
    PREFIXED_NAME_LOCAL = "PREFIXED_NAME_LOCAL"
    COLON = ":"
    FROM = "FROM"
    SELECT = "SELECT"
    ASTERISK = "*"
    VARIABLE = "VARIABLE"
    A = "A"
    WHERE = "WHERE"
    SEMI_COLON = ";"
    PERIOD = "."
    COMMA = ","
    EQUALS = "="
    SEPARATOR = "SEPARATOR"
    DISTINCT = "DISTINCT"
    AS = "AS"
    STRING_LITERAL = "STRING_LITERAL"
    U_NUMBER_LITERAL = "U_NUMBER_LITERAL"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NAMED = "NAMED"
    GRAPH = "GRAPH"
    OPTIONAL = "OPTIONAL"
    UNION = "UNION"
    MINUS = "MINUS"
    SERVICE = "SERVICE"
    SILENT = "SILENT"
    FILTER = "FILTER"
    BIND = "BIND"
    GROUP = "GROUP"
    BY = "BY"
    HAVING = "HAVING"
    ORDER = "ORDER"
    ASC = "ASC"
    DESC = "DESC"
    LIMIT = "LIMIT"
    OFFSET = "OFFSET"
    EOF = "EOF"
    COUNT = "COUNT"
    SUM = "SUM"
    MIN = "MIN"
    MAX = "MAX"
    AVG = "AVG"
    SAMPLE = "SAMPLE"
    GROUP_CONCAT = "GROUP_CONCAT"
    REGEX = "REGEX"
    SUBSTR = "SUBSTR"
    REPLACE = "REPLACE"
    EXISTS = "EXISTS"
    NOT = "NOT"
    ABS = "ABS"
    CEIL = "CEIL"
    FLOOR = "FLOOR"
    ROUND = "ROUND"
    CONCAT = "CONCAT"
    STRLEN = "STRLEN"
    UCASE = "UCASE"
    LCASE = "LCASE"
    DIV = "/"
    ADD = "+"
    SUB = "-"
    LOGICAL_AND = "&&"
    LOGICAL_OR = "||"
    LT = "<"
    GT = ">"
    G_OR_EQ = ">="
    L_OR_EQ = "<="
    NOT_EQ = "!="

    def from_keyword(term: str) -> 'QueryTerm':
        if term is None:
            return None
        if term not in NON_KEYWORD_TERMS:
            try:
                return QueryTerm(term)
            except ValueError:
                return None
        return None
    
    def built_in_calls() -> List[str]:
        return BUILT_IN_CALLS
    
    def parenable(keyword: str) -> bool:
        if keyword.upper() in PARENTHIZED_TERMS:
            return True
        return False
    
    def bracketable(keyword: str) -> bool:
        if keyword.upper() in BRACKETTED_TERMS:
            return True
        return False
    
    def equalable(keyword: str) -> bool:
        if keyword.upper() == "SEPARATOR":
            return True
        return False
    
    def __str__(self):
        return self.name.lower()
