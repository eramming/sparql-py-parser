from src.tokens import Tokenizer, Token, QueryTerm
from src.LookaheadQueue import LookaheadQueue
from typing import List

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

def test_tokenizer_prologue_with_base() -> None:
    query_str: str = '''
        BASE <http://example1-company.org/>
        base <http://example2-company.org/>
    '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get(block=False).term == QueryTerm.BASE
    iriref1: Token = tokens.get(block=False)
    assert iriref1.term == QueryTerm.IRIREF
    assert iriref1.content == "http://example1-company.org/"
    assert tokens.get(block=False).term == QueryTerm.BASE
    iriref2: Token = tokens.get(block=False)
    assert iriref2.term == QueryTerm.IRIREF
    assert iriref2.content == "http://example2-company.org/"
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

def test_tokenizer_reassigned_select_var() -> None:
    query_str: str = "SELECT (UCASE(?first_name) AS ?uppercase_fname)"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get(block=False).term is QueryTerm.SELECT
    assert tokens.get(block=False).term is QueryTerm.LPAREN
    assert tokens.get(block=False).term is QueryTerm.UCASE
    assert tokens.get(block=False).term is QueryTerm.LPAREN
    var1: Token = tokens.get(block=False)
    assert var1.term == QueryTerm.VARIABLE
    assert var1.content == "first_name"
    assert tokens.get(block=False).term is QueryTerm.RPAREN
    assert tokens.get(block=False).term is QueryTerm.AS
    var2: Token = tokens.get(block=False)
    assert var2.term == QueryTerm.VARIABLE
    assert var2.content == "uppercase_fname"
    assert tokens.get(block=False).term is QueryTerm.RPAREN
    assert tokens.get(block=False).term is QueryTerm.EOF

def test_tokenizer_built_in_functions() -> None:
    query_str: str = '''
        COUNT COUNT(
        SUM SUM(
        MIN MIN(
        MAX MAX(
        AVG AVG(
        SAMPLE SAMPLE(
        GROUP_CONCAT GROUP_CONCAT(
        REGEX REGEX(
        SUBSTR SUBSTR(
        REPLACE REPLACE(
        EXISTS EXISTS(
        NOT
        ABS ABS(
        CEIL CEIL(
        FLOOR FLOOR(
        ROUND ROUND(
        CONCAT CONCAT(
        STRLEN STRLEN(
        UCASE UCASE(
        LCASE LCASE(
    '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    expected: List[QueryTerm] = [
        QueryTerm.COUNT, QueryTerm.COUNT, QueryTerm.LPAREN,
        QueryTerm.SUM, QueryTerm.SUM, QueryTerm.LPAREN,
        QueryTerm.MIN, QueryTerm.MIN, QueryTerm.LPAREN,
        QueryTerm.MAX, QueryTerm.MAX, QueryTerm.LPAREN,
        QueryTerm.AVG, QueryTerm.AVG, QueryTerm.LPAREN,
        QueryTerm.SAMPLE, QueryTerm.SAMPLE, QueryTerm.LPAREN,
        QueryTerm.GROUP_CONCAT, QueryTerm.GROUP_CONCAT, QueryTerm.LPAREN,
        QueryTerm.REGEX, QueryTerm.REGEX, QueryTerm.LPAREN,
        QueryTerm.SUBSTR, QueryTerm.SUBSTR, QueryTerm.LPAREN,
        QueryTerm.REPLACE, QueryTerm.REPLACE, QueryTerm.LPAREN,
        QueryTerm.EXISTS, QueryTerm.EXISTS, QueryTerm.LPAREN,
        QueryTerm.NOT,
        QueryTerm.ABS, QueryTerm.ABS, QueryTerm.LPAREN,
        QueryTerm.CEIL, QueryTerm.CEIL, QueryTerm.LPAREN,
        QueryTerm.FLOOR, QueryTerm.FLOOR, QueryTerm.LPAREN,
        QueryTerm.ROUND, QueryTerm.ROUND, QueryTerm.LPAREN,
        QueryTerm.CONCAT, QueryTerm.CONCAT, QueryTerm.LPAREN,
        QueryTerm.STRLEN, QueryTerm.STRLEN, QueryTerm.LPAREN,
        QueryTerm.UCASE, QueryTerm.UCASE, QueryTerm.LPAREN,
        QueryTerm.LCASE, QueryTerm.LCASE, QueryTerm.LPAREN,
        QueryTerm.EOF
    ]
    assert expected == [token.term for token in tokens.get_all()]

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

def test_tokenizer_where() -> None:
    query_str: str = "WHERE { }"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get(block=False).term is QueryTerm.WHERE
    assert tokens.get(block=False).term is QueryTerm.LBRACKET
    assert tokens.get(block=False).term is QueryTerm.RBRACKET
    assert tokens.get(block=False).term is QueryTerm.EOF

def test_tokenizer_optional() -> None:
    query_str: str = "WHERE { }"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get(block=False).term is QueryTerm.WHERE
    assert tokens.get(block=False).term is QueryTerm.LBRACKET
    assert tokens.get(block=False).term is QueryTerm.RBRACKET
    assert tokens.get(block=False).term is QueryTerm.EOF
    raise NotImplementedError()

def test_tokenizer_specify_graph() -> None:
    raise NotImplementedError()

def test_tokenizer_comments() -> None:
    raise NotImplementedError()

def test_tokenizer_number_literal() -> None:
    raise NotImplementedError()

def test_tokenizer_string_literal() -> None:
    raise NotImplementedError()

def test_tokenizer_expected_errors() -> None:
    raise NotImplementedError()

def test_tokenizer_full_query() -> None:
    query_str: str = '''
        prefix foaf: <http://xmlns.com/foaf/0.1/>
        
        # An example query
        SELECT *
        WHERE {
            ?person foaf:givenName "Eric" ;
                    foaf:age 26 .
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

    assert tokens.get(block=False).term is QueryTerm.SEMI_COLON
    prefix_name: Token = tokens.get(block=False)
    assert prefix_name.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix_name.content == "foaf"
    assert tokens.get(block=False).term is QueryTerm.COLON
    local_name: Token = tokens.get(block=False)
    assert local_name.term == QueryTerm.PREFIXED_NAME_LOCAL
    assert local_name.content == "age"
    string_literal: Token = tokens.get(block=False)
    assert string_literal.term == QueryTerm.NUMBER_LITERAL
    assert string_literal.content == "26"

    assert tokens.get(block=False).term is QueryTerm.PERIOD
    assert tokens.get(block=False).term is QueryTerm.RBRACKET
    assert tokens.get(block=False).term is QueryTerm.EOF
