from enum import Enum

class QueryTerm(Enum):
    RPAREN = ")",
    LPAREN = "(",
    RBRACKET = "}",
    LBRACKET = "{",
    BASE = "BASE",
    PREFIX = "PREFIX",
    IRIREF = "FULLY SPECIFIED IRI",
    PREFIX_NAME = "PREFIX NAME",
    COLON = ":",
    IRI = "IRI",
    FROM = "FROM",
    SELECT = "SELECT",
    VARIABLE = "VARIABLE",
    WHERE = "WHERE",
    DISTINCT = "DISTINCT",
    AS = "AS",
    NAMED = "NAMED",
    GRAPH = "GRAPH",
    OPTIONAL = "OPTIONAL",
    EOF = "EOF"
