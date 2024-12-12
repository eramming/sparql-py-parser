from enum import Enum
from typing import List

NON_KEYWORD_TERMS: List[str] = [
    "IRIREF", "PREFIXED_NAME_PREFIX", "PREFIXED_NAME_LOCAL", "VARIABLE",
    "STRING_LITERAL", "NUMBER_LITERAL", "EOF"
]
BUILT_IN_CALLS: List[str] = [
    "COUNT", "SUM", "MIN", "MAX", "AVG", "SAMPLE", "GROUP_CONCAT", "REGEX",
    "SUBSTR", "REPLACE", "EXISTS", "NOT", "ABS", "CEIL", "FLOOR", "ROUND",
    "CONCAT", "STRLEN", "UCASE", "LCASE"
]

class QueryTerm(Enum):
    RPAREN = ")"
    LPAREN = "("
    RBRACKET = "}"
    LBRACKET = "{"
    EXCLAMATION = "!"
    BASE = "BASE"
    PREFIX = "PREFIX"
    IRIREF = "IRIREF"
    PREFIXED_NAME_PREFIX = "PREFIXED_NAME_PREFIX"
    PREFIXED_NAME_LOCAL = "PREFIXED_NAME_LOCAL"
    COLON = ":"
    FROM = "FROM"
    SELECT = "SELECT"
    ASTERISK = "*"
    VARIABLE = "VARIABLE"
    WHERE = "WHERE"
    SEMI_COLON = ";"
    PERIOD = "."
    COMMA = ","
    EQUALS = "="
    SEPARATOR = "SEPARATOR"
    DISTINCT = "DISTINCT"
    AS = "AS"
    STRING_LITERAL = "STRING_LITERAL"
    NUMBER_LITERAL = "NUMBER_LITERAL"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NAMED = "NAMED"
    GRAPH = "GRAPH"
    OPTIONAL = "OPTIONAL"
    UNION = "UNION"
    MINUS = "MINUS"
    SERVICE = "SERVICE"
    FILTER = "FILTER"
    BIND = "BIND"
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
    
    def __str__(self):
        return self.name.lower()
