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
    query_str: str = "SELECT ?first_name ?_AGE ?4th_grade_teacher"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get(block=False).term is QueryTerm.SELECT
    var1: Token = tokens.get(block=False)
    assert var1.term == QueryTerm.VARIABLE
    assert var1.content == "first_name"
    var2: Token = tokens.get(block=False)
    assert var2.term == QueryTerm.VARIABLE
    assert var2.content == "_AGE"
    var3: Token = tokens.get(block=False)
    assert var3.term == QueryTerm.VARIABLE
    assert var3.content == "4th_grade_teacher"
    assert tokens.get(block=False).term is QueryTerm.EOF

def test_tokenizer_select_distinct() -> None:
    query_str: str = "SELECT DISTINCT ?first_name"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get(block=False).term is QueryTerm.SELECT
    assert tokens.get(block=False).term is QueryTerm.DISTINCT
    var1: Token = tokens.get(block=False)
    assert var1.term == QueryTerm.VARIABLE
    assert var1.content == "first_name"
    assert tokens.get(block=False).term is QueryTerm.EOF

def test_tokenizer_select_all() -> None:
    query_str: str = "SELECT *"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get(block=False).term is QueryTerm.SELECT
    assert tokens.get(block=False).term is QueryTerm.ASTERISK
    assert tokens.get(block=False).term is QueryTerm.EOF

def test_tokenizer_dataset_clause() -> None:
    query_str: str = "FROM NAMED ex:MyGraph-uuid"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get(block=False).term is QueryTerm.FROM
    assert tokens.get(block=False).term is QueryTerm.NAMED
    prefix_name: Token = tokens.get(block=False)
    assert prefix_name.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix_name.content == "ex"
    assert tokens.get(block=False).term == QueryTerm.COLON
    local_name: Token = tokens.get(block=False)
    assert local_name.term == QueryTerm.PREFIXED_NAME_LOCAL
    assert local_name.content == "MyGraph-uuid"
    assert tokens.get(block=False).term is QueryTerm.EOF

def test_tokenizer_full_query() -> None:
    query_str: str = '''
        prefix foaf: <http://xmlns.com/foaf/0.1/>
        
        # An example query
        SELECT *
        WHERE {
            ?person foaf:givenName "Eric" .
        }
        '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get(block=False).term is QueryTerm.PREFIX
    prefix_name: Token = tokens.get(block=False)
    assert prefix_name.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix_name.content == "foaf"
    assert tokens.get(block=False).term == QueryTerm.COLON
    iriref: Token = tokens.get(block=False)
    assert iriref.term == QueryTerm.IRIREF
    assert iriref.content == "http://xmlns.com/foaf/0.1/"

    assert tokens.get(block=False).term is QueryTerm.SELECT
    assert tokens.get(block=False).term is QueryTerm.ASTERISK
    assert tokens.get(block=False).term is QueryTerm.WHERE
    assert tokens.get(block=False).term is QueryTerm.LBRACKET
    var1: Token = tokens.get(block=False)
    assert var1.term == QueryTerm.VARIABLE
    assert var1.content == "person"
    prefix_name: Token = tokens.get(block=False)
    assert prefix_name.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix_name.content == "foaf"
    assert tokens.get(block=False).term is QueryTerm.COLON
    local_name: Token = tokens.get(block=False)
    assert local_name.term == QueryTerm.PREFIXED_NAME_LOCAL
    assert local_name.content == "givenName"
    string_literal: Token = tokens.get(block=False)
    assert string_literal.term == QueryTerm.STRING_LITERAL
    assert string_literal.content == "Eric"

    assert tokens.get(block=False).term is QueryTerm.PERIOD
    assert tokens.get(block=False).term is QueryTerm.RBRACKET
    assert tokens.get(block=False).term is QueryTerm.EOF


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
