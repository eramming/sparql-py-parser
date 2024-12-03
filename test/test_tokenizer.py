from src.tokens import Tokenizer, Token, QueryTerm
from src.LookaheadQueue import LookaheadQueue

def test_tokenizer_prologue() -> None:
    query_str: str = '''
        PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)
    
    assert tokens.get(block=False).term is QueryTerm.PREFIX
    prefix_name: Token = tokens.get(block=False)
    assert prefix_name.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix_name.content == "xsd"
    assert tokens.get(block=False).term == QueryTerm.COLON
    iriref: Token = tokens.get(block=False)
    assert iriref.term == QueryTerm.IRIREF
    assert iriref.content == "http://www.w3.org/2001/XMLSchema#"

    assert tokens.get(block=False).term == QueryTerm.PREFIX
    prefix_name: Token = tokens.get(block=False)
    assert prefix_name.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix_name.content == "rdf"
    assert tokens.get(block=False).term == QueryTerm.COLON
    iriref: Token = tokens.get(block=False)
    assert iriref.term == QueryTerm.IRIREF
    assert iriref.content == "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    assert tokens.get(block=False).term == QueryTerm.EOF

def test_tokenizer_select_variables() -> None:
    raise NotImplementedError()

def test_tokenizer_dataset_clause() -> None:
    raise NotImplementedError()

def test_tokenizer_skeleton_query() -> None:
    raise NotImplementedError()

def test_tokenizer_simple_where() -> None:
    raise NotImplementedError()

def test_tokenizer_complex_where() -> None:
    raise NotImplementedError()

def test_tokenizer_select_with_optional() -> None:
    raise NotImplementedError()

def test_tokenizer_specify_graph() -> None:
    raise NotImplementedError()

def test_tokenizer_comments() -> None:
    raise NotImplementedError()
