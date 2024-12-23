from src import QueryParser, Tokenizer, Query
from .utilities_for_test import standardize_whitespace, strip_comments

def test_empty() -> None:
    query_str: str = '''
    SELECT *
    WHERE {

    }
    '''
    
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert standardize_whitespace(str(query)) == standardize_whitespace(strip_comments(query_str))

def test_select_all() -> None:
    query_str: str = '''
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX ex: <http://ex.com/department/#>

    SELECT *
    WHERE {
        ?person foaf:knows "Albert" ;
                ex:fname ?fname .
    }
    '''
    
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert standardize_whitespace(str(query)) == standardize_whitespace(strip_comments(query_str))

def test_select_by_name() -> None:
    query_str: str = '''
    BASE <http://ex.com/#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?age ?area ?fname ?person
    WHERE {
        ?person foaf:knows "Albert" ;
                foaf:givenName ?fname ;
                foaf:age ?age ;
                foaf:based_near ?area .
    }
    '''
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert standardize_whitespace(str(query)) == standardize_whitespace(strip_comments(query_str))

def test_select_with_derived_vars() -> None:
    query_str: str = '''
    PREFIX ex: <http://ex.com/department/#>

    SELECT DISTINCT ?person
        (SUM(?publishedCount + ?draftCount) AS ?total_count)
    WHERE {
        ?person a ex:Author ;
                ex:publishedCount ?publishedCount ;
                ex:draftCount ?draftCount .
    }
    '''
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert standardize_whitespace(str(query)) == standardize_whitespace(strip_comments(query_str))

def test_optionals() -> None:
    query_str: str = '''
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX ex: <http://ex.com/department/#>

    SELECT *
    WHERE {
        ?person foaf:based_near "Pennsylvania" ;
                ex:fname ?fname .
        OPTIONAL {
            ?person ex:age ?age .
        }
        ?person a ex:Employee .
        OPTIONAL {
            ?person ex:works_at ?company ;
                    ex:has_salary ?salary .
        }
    }
    '''
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert standardize_whitespace(str(query)) == standardize_whitespace(strip_comments(query_str))

def test_graph_graph_pattern() -> None:
    query_str: str = '''
    PREFIX ex: <http://ex0.com/department/#>
    PREFIX pets: <http://ex1.com/rdf/pet_owners/#>
    PREFIX med: <http://ex2.com/rdf/medical/animal/#>

    SELECT ?animal ?graph ?person
    WHERE {
        ?person a ex:PetOwner .
        GRAPH pets:GraphInstance-1234 {
            ?person pets:hasPet ?pet .
            ?pet pets:animal_type ?animal .
        }
        GRAPH ?graph {
            ?animal med:commonHealthIssues "hips" .
        }
    }
    '''
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert standardize_whitespace(str(query)) == standardize_whitespace(strip_comments(query_str))

def test_dataset_clause() -> None:
    query_str: str = '''
    PREFIX ex: <http://ex.com/department/#>

    SELECT ?person
    FROM NAMED <http://ex2.com/pet_owners/Graph-1234>
    WHERE {
        ?person ex:has_pet "Chinchilla" .
    }
    '''
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert standardize_whitespace(str(query)) == standardize_whitespace(strip_comments(query_str))

def test_built_in_calls() -> None:
    query_str: str = '''
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX ns: <http://example.org/ns#>

    SELECT ?lc_title ?max_discount ?oneliner
    {
        ?x ns:price ?p .
        ?x ns:discount ?discount .
        ?x dc:title ?title . 
        BIND(ROUND(?p) AS ?price)
        BIND(ABS(?discount) AS ?pos_discount)
        FILTER (STRLEN(?title) < 20)
        BIND(LCASE(?title) AS ?lc_title)
        BIND(CONCAT(?lc_title, " for ", ?price) AS ?oneliner)
        BIND(MAX(?pos_discount) AS ?max_discount)
    }
    '''
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert standardize_whitespace(str(query)) == standardize_whitespace(strip_comments(query_str))

def test_multi_exprs() -> None:
    query_str: str = '''
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX ns: <http://example.org/ns#>

    SELECT ?fname ?person
    WHERE {
        ?x ns:price ?p .
        ?x ns:discount ?discount .
        BIND(ROUND(?p) * (1 - ABS(?discount)) AS ?price)
        ?x dc:title ?title .
        FILTER (((?price / (0.9 + 0.1) != -50.0) || false) && STRLEN(?title) <= (20))
    }
    '''
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert standardize_whitespace(str(query)) == standardize_whitespace(strip_comments(query_str))

def test_subselect() -> None:
    query_str: str = '''
    PREFIX ex: <http://ex.com/department/#>

    SELECT ?name_upper
    WHERE {
        SELECT (UCASE(?fname) AS ?name_upper)
        WHERE {
            ?person a ex:Person ;
                    ex:fname ?fname .
        }
        LIMIT 10
    }
    '''
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert standardize_whitespace(str(query)) == standardize_whitespace(strip_comments(query_str))

def test_complex_ggp() -> None:
    query_str: str = '''
    PREFIX ex: <http://ex.com/department/#>

    SELECT ?age ?obj3 ?person ?pet_name ?val
    WHERE {
        {
            SELECT ?age ?person
            WHERE {
                GRAPH ex:MyGraph {
                    ?person a ex:Person .
                    OPTIONAL {
                        ?person ex:age ?age .
                    }
                    FILTER (?age < 18)
                }
            }
        }
        UNION
        {
            BIND(-23.1 AS ?val)
        }
        ?subj ex:pred ?obj .
        GRAPH ex:GraphInstance-1234 {
            ?person ex:hasPet ?pet .
            ?pet ex:name ?pet_name .
        }
        ?subj2 ex:pred2 ?obj2 ;
                ex:pred3 ?obj3 .
    }
    '''
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert standardize_whitespace(str(query)) == standardize_whitespace(strip_comments(query_str))

def test_verb_paths() -> None:
    query_str: str = '''
    PREFIX ex: <http://ex.com/#>

    SELECT ?pet_name
    WHERE {
        ?company ((ex:alias? / ex:hasDepartment / ex:subDept* / ex:member) | ex:owner) / ex:hasPet ?pet .
        ?pet a ex:Chinchilla ;
            ex:named ?pet_name .
    }
    '''
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert standardize_whitespace(str(query)) == standardize_whitespace(strip_comments(query_str))

def test_soln_modifiers() -> None:
    query_str: str = '''
    PREFIX ex: <http://ex.com/department/#>

    SELECT ?fname ?person
    WHERE {
        ?a :x ?x ;
           :y ?y .
    }
    GROUP BY ?x
    HAVING (AVG(?y) > 0)
    ORDER BY DESC(?x)
    OFFSET 5
    LIMIT 100
    '''
    query: Query = QueryParser().parse(Tokenizer().tokenize(query_str))
    assert standardize_whitespace(str(query)) == standardize_whitespace(strip_comments(query_str))    
