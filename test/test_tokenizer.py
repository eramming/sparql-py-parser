from src.tokens import Tokenizer, Token, QueryTerm
from src.LookaheadQueue import LookaheadQueue
from typing import List

def test_tokenizer_prologue() -> None:
    query_str: str = '''
        PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)
    
    assert tokens.get_now().term is QueryTerm.PREFIX
    prefix_name: Token = tokens.get_now()
    assert prefix_name.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix_name.content == "xsd"
    assert tokens.get_now().term == QueryTerm.COLON
    iriref: Token = tokens.get_now()
    assert iriref.term == QueryTerm.IRIREF
    assert iriref.content == "http://www.w3.org/2001/XMLSchema#"

    assert tokens.get_now().term == QueryTerm.PREFIX
    prefix_name: Token = tokens.get_now()
    assert prefix_name.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix_name.content == "rdf"
    assert tokens.get_now().term == QueryTerm.COLON
    iriref: Token = tokens.get_now()
    assert iriref.term == QueryTerm.IRIREF
    assert iriref.content == "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    assert tokens.get_now().term == QueryTerm.EOF

def test_tokenizer_prologue_with_base() -> None:
    query_str: str = '''
        BASE <http://example1-company.org/>
        base <http://example2-company.org/>
    '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get_now().term == QueryTerm.BASE
    iriref1: Token = tokens.get_now()
    assert iriref1.term == QueryTerm.IRIREF
    assert iriref1.content == "http://example1-company.org/"
    assert tokens.get_now().term == QueryTerm.BASE
    iriref2: Token = tokens.get_now()
    assert iriref2.term == QueryTerm.IRIREF
    assert iriref2.content == "http://example2-company.org/"
    assert tokens.get_now().term == QueryTerm.EOF

def test_tokenizer_select_variables() -> None:
    query_str: str = "SELECT ?first_name ?_AGE ?4th_grade_teacher"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get_now().term is QueryTerm.SELECT
    var1: Token = tokens.get_now()
    assert var1.term == QueryTerm.VARIABLE
    assert var1.content == "first_name"
    var2: Token = tokens.get_now()
    assert var2.term == QueryTerm.VARIABLE
    assert var2.content == "_AGE"
    var3: Token = tokens.get_now()
    assert var3.term == QueryTerm.VARIABLE
    assert var3.content == "4th_grade_teacher"
    assert tokens.get_now().term is QueryTerm.EOF

def test_tokenizer_select_distinct() -> None:
    query_str: str = "SELECT DISTINCT ?first_name"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get_now().term is QueryTerm.SELECT
    assert tokens.get_now().term is QueryTerm.DISTINCT
    var1: Token = tokens.get_now()
    assert var1.term == QueryTerm.VARIABLE
    assert var1.content == "first_name"
    assert tokens.get_now().term is QueryTerm.EOF

def test_tokenizer_select_all() -> None:
    query_str: str = "SELECT *"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get_now().term is QueryTerm.SELECT
    assert tokens.get_now().term is QueryTerm.ASTERISK
    assert tokens.get_now().term is QueryTerm.EOF

def test_tokenizer_derived_var() -> None:
    query_str: str = "SELECT (UCASE(?first_name) AS ?uppercase_fname)"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get_now().term is QueryTerm.SELECT
    assert tokens.get_now().term is QueryTerm.LPAREN
    assert tokens.get_now().term is QueryTerm.UCASE
    assert tokens.get_now().term is QueryTerm.LPAREN
    var1: Token = tokens.get_now()
    assert var1.term == QueryTerm.VARIABLE
    assert var1.content == "first_name"
    assert tokens.get_now().term is QueryTerm.RPAREN
    assert tokens.get_now().term is QueryTerm.AS
    var2: Token = tokens.get_now()
    assert var2.term == QueryTerm.VARIABLE
    assert var2.content == "uppercase_fname"
    assert tokens.get_now().term is QueryTerm.RPAREN
    assert tokens.get_now().term is QueryTerm.EOF

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

    assert tokens.get_now().term is QueryTerm.FROM
    assert tokens.get_now().term is QueryTerm.NAMED
    prefix_name: Token = tokens.get_now()
    assert prefix_name.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix_name.content == "ex"
    assert tokens.get_now().term == QueryTerm.COLON
    local_name: Token = tokens.get_now()
    assert local_name.term == QueryTerm.PREFIXED_NAME_LOCAL
    assert local_name.content == "MyGraph-uuid"
    assert tokens.get_now().term is QueryTerm.EOF

def test_tokenizer_where() -> None:
    query_str: str = "WHERE { }"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get_now().term is QueryTerm.WHERE
    assert tokens.get_now().term is QueryTerm.LBRACKET
    assert tokens.get_now().term is QueryTerm.RBRACKET
    assert tokens.get_now().term is QueryTerm.EOF

def test_tokenizer_optional() -> None:
    query_str: str = "OPTIONAL { }"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get_now().term is QueryTerm.OPTIONAL
    assert tokens.get_now().term is QueryTerm.LBRACKET
    assert tokens.get_now().term is QueryTerm.RBRACKET
    assert tokens.get_now().term is QueryTerm.EOF

def test_tokenizer_specify_graph() -> None:
    query_str: str = "GRAPH ex:MyGraph-uuid { }"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get_now().term is QueryTerm.GRAPH
    prefix_name: Token = tokens.get_now()
    assert prefix_name.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix_name.content == "ex"
    assert tokens.get_now().term == QueryTerm.COLON
    local_name: Token = tokens.get_now()
    assert local_name.term == QueryTerm.PREFIXED_NAME_LOCAL
    assert local_name.content == "MyGraph-uuid"
    assert tokens.get_now().term is QueryTerm.LBRACKET
    assert tokens.get_now().term is QueryTerm.RBRACKET
    assert tokens.get_now().term is QueryTerm.EOF

def test_tokenizer_comments() -> None:
    query_str: str = '''
        # My Query
        ?var1 # ex:hasId
        # Comments
        ?var2 # ?var3 ## . ()
    '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    var1: Token = tokens.get_now()
    assert var1.term == QueryTerm.VARIABLE
    assert var1.content == "var1"
    var2: Token = tokens.get_now()
    assert var2.term == QueryTerm.VARIABLE
    assert var2.content == "var2"
    assert tokens.get_now().term is QueryTerm.EOF

def test_tokenizer_number_literal() -> None:
    query_str: str = '''
        67 +67 -67 -67.0 +67.0 0.1415
    '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    num1: Token = tokens.get_now()
    assert num1.term == QueryTerm.NUMBER_LITERAL
    assert num1.content == "67"
    num2: Token = tokens.get_now()
    assert num2.term == QueryTerm.NUMBER_LITERAL
    assert num2.content == "+67"
    num3: Token = tokens.get_now()
    assert num3.term == QueryTerm.NUMBER_LITERAL
    assert num3.content == "-67"
    num4: Token = tokens.get_now()
    assert num4.term == QueryTerm.NUMBER_LITERAL
    assert num4.content == "-67.0"
    num5: Token = tokens.get_now()
    assert num5.term == QueryTerm.NUMBER_LITERAL
    assert num5.content == "+67.0"
    num6: Token = tokens.get_now()
    assert num6.term == QueryTerm.NUMBER_LITERAL
    assert num6.content == "0.1415"
    assert tokens.get_now().term is QueryTerm.EOF

def test_tokenizer_string_literal() -> None:
    query_str: str = '''
        "Son of a !@#$%^&*()_-+={[]}|;.,<>?/" "87.2" """Multi
        Line
        Literal""" 'Son of a !@#$%^&*()_-+={[]}|;.,<>?/' '87.2' \'\'\'Multi
        Line
        Literal\'\'\'
    '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    lit1: Token = tokens.get_now()
    assert lit1.term == QueryTerm.STRING_LITERAL
    assert lit1.content == "Son of a !@#$%^&*()_-+={[]}|;.,<>?/"
    lit2: Token = tokens.get_now()
    assert lit2.term == QueryTerm.STRING_LITERAL
    assert lit2.content == "87.2"
    lit3: Token = tokens.get_now()
    assert lit3.term == QueryTerm.STRING_LITERAL
    assert lit3.content.replace(" ", "") == "Multi\nLine\nLiteral"
    lit4: Token = tokens.get_now()
    assert lit4.term == QueryTerm.STRING_LITERAL
    assert lit4.content == "Son of a !@#$%^&*()_-+={[]}|;.,<>?/"
    lit5: Token = tokens.get_now()
    assert lit5.term == QueryTerm.STRING_LITERAL
    assert lit5.content == "87.2"
    lit6: Token = tokens.get_now()
    assert lit6.term == QueryTerm.STRING_LITERAL
    assert lit6.content.replace(" ", "") == "Multi\nLine\nLiteral"
    assert tokens.get_now().term is QueryTerm.EOF

def test_tokenizer_expected_failures() -> None:
    queries: List[str] = ["EOF", "PREFIXED_NAME_PREFIX", "PREFIXED_NAME_LOCAL",
                          "IRIREF", "VARIABLE", "NUMBER_LITERAL", "STRING_LITERAL"]
    
    for query_str in queries:
        tokenizer: Tokenizer = Tokenizer()
        try:
            tokenizer.tokenize(query_str)
            assert False
        except ValueError:
            continue

def test_tokenizer_path_primaries() -> None:
    query_str: str = '''
        ?entity !a ex:Place
    '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    var: Token = tokens.get_now()
    assert var.term == QueryTerm.VARIABLE
    assert var.content == "entity"
    assert tokens.get_now().term == QueryTerm.EXCLAMATION
    assert tokens.get_now().term == QueryTerm.A
    prefix: Token = tokens.get_now()
    assert prefix.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix.content == "ex"
    assert tokens.get_now().term == QueryTerm.COLON
    local_name: Token = tokens.get_now()
    assert local_name.term == QueryTerm.PREFIXED_NAME_LOCAL
    assert local_name.content == "Place"
    assert tokens.get_now().term is QueryTerm.EOF

def test_tokenizer_extra_stuff() -> None:
    COMMA = ","
    EQUALS = "="
    SEPARATOR = "SEPARATOR"
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNION = "UNION"
    MINUS = "MINUS"
    SERVICE = "SERVICE"
    SILENT = "SILENT"
    FILTER = "FILTER"
    BIND = "BIND"
    GROUP = "GROUP"
    BY = "BY"
    HAVING = "HAVING"
    ORDER = "ORDER"
    ASC = "ASC"
    DESC = "DESC"
    LIMIT = "LIMIT"
    OFFSET = "OFFSET"
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

    assert tokens.get_now().term is QueryTerm.PREFIX
    prefix_name: Token = tokens.get_now()
    assert prefix_name.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix_name.content == "foaf"
    assert tokens.get_now().term == QueryTerm.COLON
    iriref: Token = tokens.get_now()
    assert iriref.term == QueryTerm.IRIREF
    assert iriref.content == "http://xmlns.com/foaf/0.1/"

    assert tokens.get_now().term is QueryTerm.SELECT
    assert tokens.get_now().term is QueryTerm.ASTERISK
    assert tokens.get_now().term is QueryTerm.WHERE
    assert tokens.get_now().term is QueryTerm.LBRACKET
    var1: Token = tokens.get_now()
    assert var1.term == QueryTerm.VARIABLE
    assert var1.content == "person"
    prefix_name: Token = tokens.get_now()
    assert prefix_name.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix_name.content == "foaf"
    assert tokens.get_now().term is QueryTerm.COLON
    local_name: Token = tokens.get_now()
    assert local_name.term == QueryTerm.PREFIXED_NAME_LOCAL
    assert local_name.content == "givenName"
    string_literal: Token = tokens.get_now()
    assert string_literal.term == QueryTerm.STRING_LITERAL
    assert string_literal.content == "Eric"

    assert tokens.get_now().term is QueryTerm.SEMI_COLON
    prefix_name: Token = tokens.get_now()
    assert prefix_name.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix_name.content == "foaf"
    assert tokens.get_now().term is QueryTerm.COLON
    local_name: Token = tokens.get_now()
    assert local_name.term == QueryTerm.PREFIXED_NAME_LOCAL
    assert local_name.content == "age"
    string_literal: Token = tokens.get_now()
    assert string_literal.term == QueryTerm.NUMBER_LITERAL
    assert string_literal.content == "26"

    assert tokens.get_now().term is QueryTerm.PERIOD
    assert tokens.get_now().term is QueryTerm.RBRACKET
    assert tokens.get_now().term is QueryTerm.EOF
