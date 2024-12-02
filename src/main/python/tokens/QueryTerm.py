from enum import Enum

class QueryTerm(Enum):
    RPAREN = ")",
    LPAREN = "(",
    RBRACKET = "}",
    LBRACKET = "{",
    BASE = "BASE",
    PREFIX = "PREFIX",
    IRI = None,
    COLON = ":",
    FROM = "FROM",
    SELECT = "SELECT",
    WHERE = "WHERE",
    DISTINCT = "DISTINCT",
    AS = "AS",
    NAMED = "NAMED",
    GRAPH = "GRAPH",
    OPTIONAL = "OPTIONAL",
    EOF = None
