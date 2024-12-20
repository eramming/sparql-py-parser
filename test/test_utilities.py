from .utilities_for_test import strip_comments, remove_whitespace

def test_strip_comments() -> None:
    query_str: str = '''
    prefix #foaf: <http://xmlns.com/foaf/0.1/#>
    prefix ex: <http://ex.com/department/#> # A comment
    # Entire line comment
    This <is> a <test#> # for <comments#>!
    '''
    expected: str = '''
    prefix
    prefix ex: <http://ex.com/department/#>
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
