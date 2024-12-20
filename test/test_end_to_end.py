from src import QueryParser, Tokenizer, Query
import re
from re import Match
from typing import List, Dict
from collections import defaultdict


def test_strip_comments() -> None:
    query_str: str = '''
    prefix #foaf: <http://xmlns.com/foaf/0.1/#>
    prefix ex: <http://bbn.com/ami/ix/ce#> # A comment
    # Entire line comment
    This <is> a <test#> # for <comments#>!
    '''
    expected: str = '''
    prefix
    prefix ex: <http://bbn.com/ami/ix/ce#>
    This <is> a <test#>
    '''
    assert expected.lstrip("\n").rstrip(" ") == strip_comments(query_str)

def test_remove_whitespace() -> None:
    query_str: str = '''
    Test string!      <-spaces    <-tab trailing_spaces->    
    
    
    More
        stuff
            to
                test.  Good  work.
    '''
    expected: str = "Test string! <-spaces <-tab trailing_spaces-> More stuff to test. Good work."
    assert expected == remove_whitespace(query_str)

def test_empty() -> None:
    query_str: str = '''
    SELECT *
    WHERE {

    }
    '''
    
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert str(query) == remove_whitespace(strip_comments(query_str))

def test_select_all() -> None:
    query_str: str = '''
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    prefix ex: <http://bbn.com/ami/ix/ce#>

    SELECT *
    WHERE {
        ?person foaf:knows "Albert" ;
                ex:fname ?fname .
    }
    '''
    
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert str(query) == remove_whitespace(strip_comments(query_str))

def test_select_by_name() -> None:
    query_str: str = '''
    prefix foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?person ?fname ?age ?area
    WHERE {
        ?person foaf:knows "Albert" ;
                foaf:givenName ?fname ;
                foaf:age ?age ;
                foaf:based_near ?area .
    }
    '''
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert str(query) == remove_whitespace(strip_comments(query_str))

def test_select_with_derived_vars() -> None:
    query_str: str = '''
    prefix ex: <http://bbn.com/ami/ix/ce#>

    SELECT ?person
        (SUM(?publishedCount, ?draftCount) AS ?total_count)
    WHERE {
        ?person a ex:Author ;
                ex:publishedCount ?publishedCount ;
                ex:draftCount ?draftCount .
    }
    '''
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert str(query) == remove_whitespace(strip_comments(query_str))

# def test_select_with_optionals() -> None:
#     query_str: str = '''
#     prefix foaf: <http://xmlns.com/foaf/0.1/>
#     prefix ex: <http://bbn.com/ami/ix/ce#>

#     SELECT *
#     WHERE {
#         ?person foaf:knows "Albert" ;
#                 ex:fname ?fname .
#         OPTIONAL {
#             ?person ex:age ?age .
#         }
#     }
#     '''
#     query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
#     assert str(query) == remove_whitespace(strip_comments(query_str))

# def test_select_from_named_graph() -> None:
#     query_str: str = '''
#     prefix foaf: <http://xmlns.com/foaf/0.1/>
#     prefix ex: <http://bbn.com/ami/ix/ce#>
#     prefix abox: <http://www.bbn.com/abox/rush/decomposer#>

#     SELECT ?person ?fname
#     WHERE {
#         GRAPH abox:GraphInstance-1234 {
#             ?person foaf:knows "Albert" ;
#                     ex:fname ?fname .
#         }
#     }
#     '''
#     query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
#     assert str(query) == remove_whitespace(strip_comments(query_str))

def strip_comments(query_str: str) -> str:
    # query_str = query_str.lstrip("\n")
    output: str = ""
    for line in query_str.split('\n'):
        comment_indxs: List[int] = [match.start() for match in re.finditer("#", line)]
        inside_iri_lookup: Dict[int, bool] = defaultdict(bool)
        # iriref_indxs: List[Tuple[int, int]] = \
        for match in re.finditer("<[^<>\"{}|^`\\]\\s]*>", line):
            update_truth_lookup(inside_iri_lookup, match)
        line_terminus: int = len(line)
        for indx in comment_indxs:
            if not inside_iri_lookup[indx]:
                line_terminus = indx
                break
        valid_part: str = line[:line_terminus].rstrip()
        valid_part += "\n" if len(valid_part) != 0 else ""
        output += valid_part
    return output

def inside_iriref(iriref_indxs: List) -> bool:
    raise NotImplementedError()

def update_truth_lookup(inside_iri_lookup: Dict[int, bool], match: Match) -> None:
    for i in range(match.start(), match.end()):
        inside_iri_lookup[i] = True

def remove_whitespace(input: str) -> str:
    return re.sub("( |\n|\t)+", " ", input.strip())
    
