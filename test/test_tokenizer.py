from src.tokens import Tokenizer, Token, QueryTerm
from src.LookaheadQueue import LookaheadQueue
from typing import List, Tuple

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
    assert iriref.content == "<http://www.w3.org/2001/XMLSchema#>"

    assert tokens.get_now().term == QueryTerm.PREFIX
    prefix_name: Token = tokens.get_now()
    assert prefix_name.term == QueryTerm.PREFIXED_NAME_PREFIX
    assert prefix_name.content == "rdf"
    assert tokens.get_now().term == QueryTerm.COLON
    iriref: Token = tokens.get_now()
    assert iriref.term == QueryTerm.IRIREF
    assert iriref.content == "<http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
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
    assert iriref1.content == "<http://example1-company.org/>"
    assert tokens.get_now().term == QueryTerm.BASE
    iriref2: Token = tokens.get_now()
    assert iriref2.term == QueryTerm.IRIREF
    assert iriref2.content == "<http://example2-company.org/>"
    assert tokens.get_now().term == QueryTerm.EOF

def test_tokenizer_prefixed_names() -> None:
    query_str: str = '''
        ex: : :pred ex:pred
        '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get_now().term is QueryTerm.PREFIXED_NAME_PREFIX
    assert tokens.get_now().term is QueryTerm.COLON
    assert tokens.get_now().term is QueryTerm.COLON
    assert tokens.get_now().term is QueryTerm.PREFIXED_NAME_LOCAL
    assert tokens.get_now().term is QueryTerm.PREFIXED_NAME_PREFIX
    assert tokens.get_now().term is QueryTerm.COLON
    assert tokens.get_now().term is QueryTerm.PREFIXED_NAME_LOCAL
    assert tokens.get_now().term == QueryTerm.EOF

def test_tokenizer_boolean_literals() -> None:
    query_str: str = '''
        (true) TrUe=FALSE trUe&&TRUE false||true FALSE
        '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get_now().term is QueryTerm.LPAREN
    assert tokens.get_now().term is QueryTerm.TRUE
    assert tokens.get_now().term is QueryTerm.RPAREN
    assert tokens.get_now().term is QueryTerm.TRUE
    assert tokens.get_now().term is QueryTerm.EQUALS
    assert tokens.get_now().term is QueryTerm.FALSE
    assert tokens.get_now().term is QueryTerm.TRUE
    assert tokens.get_now().term is QueryTerm.LOGICAL_AND
    assert tokens.get_now().term is QueryTerm.TRUE
    assert tokens.get_now().term is QueryTerm.FALSE
    assert tokens.get_now().term is QueryTerm.LOGICAL_OR
    assert tokens.get_now().term is QueryTerm.TRUE
    assert tokens.get_now().term is QueryTerm.FALSE
    assert tokens.get_now().term == QueryTerm.EOF

def test_tokenizer_unusual_iriref() -> None:
    query_str: str = '''
        PREFIX xsd: <UCASE(?var)7+8-10/1#> '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)
    
    assert tokens.get_now().term is QueryTerm.PREFIX
    prefix: Token = tokens.get_now()
    assert prefix.term == QueryTerm.PREFIXED_NAME_PREFIX and prefix.content == "xsd"
    assert tokens.get_now().term == QueryTerm.COLON
    iriref: Token = tokens.get_now()
    assert iriref.term == QueryTerm.IRIREF and iriref.content == "<UCASE(?var)7+8-10/1#>"
    assert tokens.get_now().term is QueryTerm.EOF

def test_tokenizer_select_variables() -> None:
    query_str: str = "SELECT ?first_name ?_AGE ?4th_grade_teacher"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get_now().term is QueryTerm.SELECT
    var1: Token = tokens.get_now()
    assert var1.term == QueryTerm.VARIABLE
    assert var1.content == "?first_name"
    var2: Token = tokens.get_now()
    assert var2.term == QueryTerm.VARIABLE
    assert var2.content == "?_AGE"
    var3: Token = tokens.get_now()
    assert var3.term == QueryTerm.VARIABLE
    assert var3.content == "?4th_grade_teacher"
    assert tokens.get_now().term is QueryTerm.EOF

def test_tokenizer_select_distinct() -> None:
    query_str: str = "SELECT DISTINCT ?first_name"
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get_now().term is QueryTerm.SELECT
    assert tokens.get_now().term is QueryTerm.DISTINCT
    var1: Token = tokens.get_now()
    assert var1.term == QueryTerm.VARIABLE
    assert var1.content == "?first_name"
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
    assert var1.content == "?first_name"
    assert tokens.get_now().term is QueryTerm.RPAREN
    assert tokens.get_now().term is QueryTerm.AS
    var2: Token = tokens.get_now()
    assert var2.term == QueryTerm.VARIABLE
    assert var2.content == "?uppercase_fname"
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
        SEPARATOR=","
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
        QueryTerm.SEPARATOR, QueryTerm.EQUALS, QueryTerm.STRING_LITERAL,
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
    assert var1.content == "?var1"
    var2: Token = tokens.get_now()
    assert var2.term == QueryTerm.VARIABLE
    assert var2.content == "?var2"
    assert tokens.get_now().term is QueryTerm.EOF

def test_tokenizer_number_literal() -> None:
    query_str: str = '''
        67 +67 -67 -67.0 +67.0 0.1415
    '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    num1: Token = tokens.get_now()
    assert num1.term == QueryTerm.U_NUMBER_LITERAL and num1.content == "67"
    assert tokens.get_now().term is QueryTerm.ADD
    num2: Token = tokens.get_now()
    assert num2.term == QueryTerm.U_NUMBER_LITERAL and num2.content == "67"
    assert tokens.get_now().term is QueryTerm.SUB
    num3: Token = tokens.get_now()
    assert num3.term == QueryTerm.U_NUMBER_LITERAL and num3.content == "67"
    assert tokens.get_now().term is QueryTerm.SUB
    num4: Token = tokens.get_now()
    assert num4.term == QueryTerm.U_NUMBER_LITERAL and num4.content == "67.0"
    assert tokens.get_now().term is QueryTerm.ADD
    num5: Token = tokens.get_now()
    assert num5.term == QueryTerm.U_NUMBER_LITERAL and num5.content == "67.0"
    num6: Token = tokens.get_now()
    assert num6.term == QueryTerm.U_NUMBER_LITERAL and num6.content == "0.1415"
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
                          "IRIREF", "VARIABLE", "NUMBER_LITERAL", "STRING_LITERAL",
                          "WHERE=", "WHERE(" "a(", "a{", "<http:// ex.com/#>"]
    
    for query_str in queries:
        tokenizer: Tokenizer = Tokenizer()
        try:
            tokenizer.tokenize(query_str)
            raise ValueError(f"Expected a runtime error at token: {query_str}")
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
    assert var.content == "?entity"
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
    
def test_tokenizer_ggp_terms() -> None:
    query_str: str = '''
        UNION MINUS SERVICE SILENT FILTER BIND GROUP
        BY HAVING ORDER ASC DESC LIMIT OFFSET'''
    
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    expected: List[QueryTerm] = [
        QueryTerm.UNION, QueryTerm.MINUS, QueryTerm.SERVICE,
        QueryTerm.SILENT, QueryTerm.FILTER, QueryTerm.BIND,
        QueryTerm.GROUP, QueryTerm.BY, QueryTerm.HAVING,
        QueryTerm.ORDER, QueryTerm.ASC, QueryTerm.DESC,
        QueryTerm.LIMIT, QueryTerm.OFFSET, QueryTerm.EOF
    ]
    assert expected == [token.term for token in tokens.get_all()]

def test_tokenizer_verb_path_symbols() -> None:
    query_str: str = '''(ex:has_child+|ex:has_sibling*)
                        /ex:legal_name?/^<http://ex.com/has_employee>/!a'''

    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)
    expected: List[Tuple[QueryTerm, str]] = [
        (QueryTerm.LPAREN, None), (QueryTerm.PREFIXED_NAME_PREFIX, "ex"),
        (QueryTerm.COLON, None), (QueryTerm.PREFIXED_NAME_LOCAL, "has_child"),
        (QueryTerm.ADD, None), (QueryTerm.PIPE, None), (QueryTerm.PREFIXED_NAME_PREFIX, "ex"),
        (QueryTerm.COLON, None), (QueryTerm.PREFIXED_NAME_LOCAL, "has_sibling"),
        (QueryTerm.ASTERISK, None), (QueryTerm.RPAREN, None), (QueryTerm.DIV, None),
        (QueryTerm.PREFIXED_NAME_PREFIX, "ex"), (QueryTerm.COLON, None),
        (QueryTerm.PREFIXED_NAME_LOCAL, "legal_name"), (QueryTerm.QUESTION, None),
        (QueryTerm.DIV, None), (QueryTerm.CARAT, None), (QueryTerm.IRIREF, "<http://ex.com/has_employee>"),
        (QueryTerm.DIV, None), (QueryTerm.EXCLAMATION, None), (QueryTerm.A, None), (QueryTerm.EOF, None)
    ]
    result_toks: List[Tuple[QueryTerm, str]] = [(tok.term, tok.content) for tok in tokens.get_all()]
    assert result_toks == expected

def test_tokenizer_multi_expr_symbols() -> None:
    query_str: str = ''' (3 + (?var/1.2) - 1+5-5) <= 10 &&
                        1< 2||?var>= 100&&?var!=144 '''

    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    expected: List[QueryTerm] = [
        QueryTerm.LPAREN, QueryTerm.U_NUMBER_LITERAL, QueryTerm.ADD,
        QueryTerm.LPAREN, QueryTerm.VARIABLE, QueryTerm.DIV,
        QueryTerm.U_NUMBER_LITERAL, QueryTerm.RPAREN, QueryTerm.SUB,
        QueryTerm.U_NUMBER_LITERAL, QueryTerm.ADD, QueryTerm.U_NUMBER_LITERAL,
        QueryTerm.SUB, QueryTerm.U_NUMBER_LITERAL, QueryTerm.RPAREN,
        QueryTerm.L_OR_EQ, QueryTerm.U_NUMBER_LITERAL, QueryTerm.LOGICAL_AND,
        QueryTerm.U_NUMBER_LITERAL, QueryTerm.LT, QueryTerm.U_NUMBER_LITERAL,
        QueryTerm.LOGICAL_OR, QueryTerm.VARIABLE, QueryTerm.G_OR_EQ,
        QueryTerm.U_NUMBER_LITERAL, QueryTerm.LOGICAL_AND, QueryTerm.VARIABLE,
        QueryTerm.NOT_EQ, QueryTerm.U_NUMBER_LITERAL, QueryTerm.EOF
    ]
    assert expected == [token.term for token in tokens.get_all()]

def test_tokenizer_full_query() -> None:
    query_str: str = '''
        prefix foaf: <http://xmlns.com/foaf/0.1/>
        
        # An example query
        SELECT *
        WHERE {
            ?person foaf:nick "Bobby", "Bob" ;
                    foaf:age 26 .
        }
        '''
    tokenizer: Tokenizer = Tokenizer()
    tokens: LookaheadQueue = tokenizer.tokenize(query_str)

    assert tokens.get_now().term is QueryTerm.PREFIX
    prefix: Token = tokens.get_now()
    assert prefix.term == QueryTerm.PREFIXED_NAME_PREFIX and prefix.content == "foaf"
    assert tokens.get_now().term == QueryTerm.COLON
    iriref: Token = tokens.get_now()
    assert iriref.term == QueryTerm.IRIREF
    assert iriref.content == "<http://xmlns.com/foaf/0.1/>"

    assert tokens.get_now().term is QueryTerm.SELECT
    assert tokens.get_now().term is QueryTerm.ASTERISK
    assert tokens.get_now().term is QueryTerm.WHERE
    assert tokens.get_now().term is QueryTerm.LBRACKET
    var1: Token = tokens.get_now()
    assert var1.term == QueryTerm.VARIABLE and var1.content == "?person"
    prefix: Token = tokens.get_now()
    assert prefix.term == QueryTerm.PREFIXED_NAME_PREFIX and prefix.content == "foaf"
    assert tokens.get_now().term is QueryTerm.COLON
    nick: Token = tokens.get_now()
    assert nick.term == QueryTerm.PREFIXED_NAME_LOCAL and nick.content == "nick"
    str_lit1: Token = tokens.get_now()
    assert str_lit1.term == QueryTerm.STRING_LITERAL and str_lit1.content == "Bobby"
    assert tokens.get_now().term is QueryTerm.COMMA
    str_lit2: Token = tokens.get_now()
    assert str_lit2.term == QueryTerm.STRING_LITERAL and str_lit2.content == "Bob"

    assert tokens.get_now().term is QueryTerm.SEMI_COLON
    prefix: Token = tokens.get_now()
    assert prefix.term == QueryTerm.PREFIXED_NAME_PREFIX and prefix.content == "foaf"
    assert tokens.get_now().term is QueryTerm.COLON
    age: Token = tokens.get_now()
    assert age.term == QueryTerm.PREFIXED_NAME_LOCAL and age.content == "age"
    num_lit: Token = tokens.get_now()
    assert num_lit.term == QueryTerm.U_NUMBER_LITERAL and num_lit.content == "26"

    assert tokens.get_now().term is QueryTerm.PERIOD
    assert tokens.get_now().term is QueryTerm.RBRACKET
    assert tokens.get_now().term is QueryTerm.EOF
