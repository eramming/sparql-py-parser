from src import QueryParser, Query, LookaheadQueue, Prologue
from src.tokens import Tokenizer, Token
from typing import List
from src.tokens import QueryTerm as qt

SIMPLE_SELECT: List[Token] = [Token(qt.SELECT), Token(qt.ASTERISK)]
SIMPLE_WHERE: List[Token] = [Token(qt.WHERE), Token(qt.LBRACKET),
                             Token(qt.RBRACKET), Token(qt.EOF)]

def test_select_all() -> None:
    parser: QueryParser = QueryParser()
    query_str: str = ""
    with open("../resources/select_all.rq", "r") as f:
        query_str = f.read()
    tokenizer: Tokenizer = Tokenizer()
    parse_result: Query = parser.parse(tokenizer.tokenize(query_str))
    raise NotImplementedError()

def test_parser_prologue() -> None:
    base_iri: str = "http://ex.com/"
    foaf: str = "http://xmlns.com/foaf/0.1/"
    rdf: str = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    tokens: List[Token] = [
        Token(qt.BASE), Token(qt.IRIREF, base_iri), Token(qt.PREFIX),
        Token(qt.PREFIXED_NAME_PREFIX, "foaf"), Token(qt.COLON),
        Token(qt.IRIREF, foaf), Token(qt.PREFIX),
        Token(qt.PREFIXED_NAME_PREFIX, "rdf"), Token(qt.COLON),
        Token(qt.IRIREF, rdf)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    for token in (tokens + SIMPLE_SELECT + SIMPLE_WHERE):
        tok_queue.put(token)
    prologue: Prologue = QueryParser().parse(tok_queue).prologue
    assert prologue.base_iri == base_iri
    assert len(prologue.prefixes) == 2
    assert prologue.prefixes["foaf"] == foaf
    assert prologue.prefixes["rdf"] == rdf

def test_parser_select_clause() -> None:
    parser: QueryParser = QueryParser()
    query_str: str = ""
    with open("../resources/select_all.rq", "r") as f:
        query_str = f.read()
    tokenizer: Tokenizer = Tokenizer()
    tokens: List[Token] = []
    parse_result: Query = parser.parse(tokenizer.tokenize(query_str))
    raise NotImplementedError()

def test_select_by_name() -> None:
    parser: QueryParser = QueryParser()
    query_str: str = ""
    with open("../resources/select_by_name.rq", "r") as f:
        query_str = f.read()
    tokenizer: Tokenizer = Tokenizer()
    parse_result: Query = parser.parse(tokenizer.tokenize(query_str))
    raise NotImplementedError()


def test_select_with_optionals() -> None:
    parser: QueryParser = QueryParser()
    query_str: str = ""
    with open("../resources/select_with_optionals.rq", "r") as f:
        query_str = f.read()
    tokenizer: Tokenizer = Tokenizer()
    parse_result: Query = parser.parse(tokenizer.tokenize(query_str))
    raise NotImplementedError()


def test_select_from_named_graph() -> None:
    parser: QueryParser = QueryParser()
    query_str: str = ""
    with open("../resources/select_from_named_graph.rq", "r") as f:
        query_str = f.read()
    tokenizer: Tokenizer = Tokenizer()
    parse_result: Query = parser.parse(tokenizer.tokenize(query_str))
    raise NotImplementedError()


def test_select_with_derived_vars() -> None:
    parser: QueryParser = QueryParser()
    query_str: str = ""
    with open("../resources/select_with_derived_vars.rq", "r") as f:
        query_str = f.read()
    tokenizer: Tokenizer = Tokenizer()
    parse_result: Query = parser.parse(tokenizer.tokenize(query_str))
    raise NotImplementedError()
