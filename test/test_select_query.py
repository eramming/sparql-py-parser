from src import QueryParser, Query, LookaheadQueue, Prologue, SelectClause, \
    GroupConcatFunction, TerminalExpr, Tokenizer, Token, QueryTerm as qt
from typing import List

SIMPLE_SELECT: List[Token] = [Token(qt.SELECT), Token(qt.ASTERISK)]
SIMPLE_WHERE: List[Token] = [Token(qt.WHERE), Token(qt.LBRACKET),
                             Token(qt.RBRACKET), Token(qt.EOF)]

# def test_select_all() -> None:
#     parser: QueryParser = QueryParser()
#     query_str: str = ""
#     with open("../resources/select_all.rq", "r") as f:
#         query_str = f.read()
#     tokenizer: Tokenizer = Tokenizer()
#     parse_result: Query = parser.parse(tokenizer.tokenize(query_str))
#     raise NotImplementedError()

def test_parser_prologue() -> None:
    # BASE <base_iri> PREFIX foaf:<foaf_iri> PREFIX rdf:<rdf_iri>
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
    # SELECT DISTINCT ?fName ?age
    # (GROUP_CONCAT(DISTINCT ?concat_subject_attribute; SEPARATOR=" ~~~~ ") AS ?subject_attributes)
    # ?lName
    fname, age, concat_subj_attr, sep = "fName", "age", "concat_subject_attribute", " ~~~~ "
    sub_attr, lname = "subject_attributes", "lName"
    tokens: List[Token] = [
        Token(qt.SELECT), Token(qt.DISTINCT), Token(qt.VARIABLE, fname),
        Token(qt.VARIABLE, age), Token(qt.LPAREN), Token(qt.GROUP_CONCAT),
        Token(qt.LPAREN), Token(qt.DISTINCT), Token(qt.VARIABLE, concat_subj_attr),
        Token(qt.SEMI_COLON), Token(qt.SEPARATOR), Token(qt.EQUALS),
        Token(qt.STRING_LITERAL, sep), Token(qt.RPAREN), Token(qt.AS),
        Token(qt.VARIABLE, sub_attr), Token(qt.RPAREN), Token(qt.VARIABLE, lname)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    for token in (tokens + SIMPLE_WHERE):
        tok_queue.put(token)
    query: Query = QueryParser().parse(tok_queue)
    select_clause: SelectClause = query.select_query.select_clause
    assert query.prologue.base_iri is None
    assert len(query.prologue.prefixes) == 0
    assert select_clause.explicit_vars == set([fname, age, lname])
    assert select_clause.is_distinct
    assert not select_clause.is_select_all
    assert len(select_clause.derived_vars) == 1
    assert sub_attr in select_clause.derived_vars
    gc_func: GroupConcatFunction = select_clause.derived_vars[sub_attr]
    assert isinstance(gc_func, GroupConcatFunction)
    assert gc_func.has_distinct_flag
    assert isinstance(gc_func.args[0], TerminalExpr)
    assert gc_func.args[0].stringified_val == concat_subj_attr
    assert gc_func.separator == sep


def test_parser_dataset_clause() -> None:
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

def test_parser_where_clause() -> None:
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

# def test_parser_select_clause() -> None:
#     parser: QueryParser = QueryParser()
#     query_str: str = ""
#     with open("../resources/select_all.rq", "r") as f:
#         query_str = f.read()
#     tokenizer: Tokenizer = Tokenizer()
#     tokens: List[Token] = []
#     parse_result: Query = parser.parse(tokenizer.tokenize(query_str))
#     raise NotImplementedError()

# def test_select_by_name() -> None:
#     parser: QueryParser = QueryParser()
#     query_str: str = ""
#     with open("../resources/select_by_name.rq", "r") as f:
#         query_str = f.read()
#     tokenizer: Tokenizer = Tokenizer()
#     parse_result: Query = parser.parse(tokenizer.tokenize(query_str))
#     raise NotImplementedError()


# def test_select_with_optionals() -> None:
#     parser: QueryParser = QueryParser()
#     query_str: str = ""
#     with open("../resources/select_with_optionals.rq", "r") as f:
#         query_str = f.read()
#     tokenizer: Tokenizer = Tokenizer()
#     parse_result: Query = parser.parse(tokenizer.tokenize(query_str))
#     raise NotImplementedError()


# def test_select_from_named_graph() -> None:
#     parser: QueryParser = QueryParser()
#     query_str: str = ""
#     with open("../resources/select_from_named_graph.rq", "r") as f:
#         query_str = f.read()
#     tokenizer: Tokenizer = Tokenizer()
#     parse_result: Query = parser.parse(tokenizer.tokenize(query_str))
#     raise NotImplementedError()


# def test_select_with_derived_vars() -> None:
#     parser: QueryParser = QueryParser()
#     query_str: str = ""
#     with open("../resources/select_with_derived_vars.rq", "r") as f:
#         query_str = f.read()
#     tokenizer: Tokenizer = Tokenizer()
#     parse_result: Query = parser.parse(tokenizer.tokenize(query_str))
#     raise NotImplementedError()
