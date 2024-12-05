from enum import Enum

class QueryTerm(Enum):
    RPAREN = ")"
    LPAREN = "("
    RBRACKET = "}"
    LBRACKET = "{"
    BASE = "BASE"
    PREFIX = "PREFIX"
    IRIREF = None
    PREFIXED_NAME_PREFIX = None
    PREFIXED_NAME_LOCAL = None
    COLON = ":"
    FROM = "FROM"
    SELECT = "SELECT"
    ASTERISK = "*"
    VARIABLE = None
    WHERE = "WHERE"
    SEMI_COLON = ";"
    PERIOD = "."
    DISTINCT = "DISTINCT"
    AS = "AS"
    STRING_LITERAL = None
    NUMBER_LITERAL = None
    NAMED = "NAMED"
    GRAPH = "GRAPH"
    OPTIONAL = "OPTIONAL"
    EOF = None
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

    def from_string(term: str) -> 'QueryTerm':
        if term is None:
            return None
        try:
            return QueryTerm(term)
        except ValueError:
            return None
