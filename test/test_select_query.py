from src import QueryParser, Query
from src.tokens import Tokenizer

def test_select_all() -> None:
    parser: QueryParser = QueryParser()
    query_str: str = ""
    with open("../resources/select_all.rq", "r") as f:
        query_str = f.read()
    tokenizer: Tokenizer = Tokenizer()
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
