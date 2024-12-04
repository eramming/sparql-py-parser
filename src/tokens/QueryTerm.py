from enum import Enum

class QueryTerm(Enum):
    RPAREN = ")"
    LPAREN = "("
    RBRACKET = "}"
    LBRACKET = "{"
    BASE = "BASE"
    PREFIX = "PREFIX"
    IRIREF = "IRIREF"
    PREFIXED_NAME_PREFIX = "PREFIXED_NAME_PREFIX"
    PREFIXED_NAME_LOCAL = "PREFIXED_NAME_LOCAL"
    COLON = ":"
    IRI = "IRI"
    FROM = "FROM"
    SELECT = "SELECT"
    ASTERISK = "*"
    VARIABLE = "VARIABLE"
    WHERE = "WHERE"
    SEMI_COLON = ";"
    PERIOD = "."
    DISTINCT = "DISTINCT"
    AS = "AS"
    STRING_LITERAL = "STRING_LITERAL"
    NUMBER_LITERAL = "NUMBER_LITERAL"
    NAMED = "NAMED"
    GRAPH = "GRAPH"
    OPTIONAL = "OPTIONAL"
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
