from src import Prologue, DatasetClause, SelectClause, GraphGraphPattern, \
    GroupGraphPatternSub, UnionGraphPattern, ServiceGraphPattern, OptionalGraphPattern, \
    MinusGraphPattern, Bind, Filter, SolnModifier, MultiExprExpr, Function, \
    AggregateFunction, IdentityFunction, ExistenceExpr, TriplesBlock, \
    TriplesSameSubj, ElementVerbPath, InverseVerbPath, IdentityVerbPath, \
    TerminalVerbPath, MultiPathVerbPath, TerminalExpr
from .utilities_for_test import remove_whitespace

def test_prologue_to_str() -> None:
    base = "<http://ex.com/#>" 
    foaf, ns = "<http://xmlns.com/foaf/0.1/>", "<http://example.org/ns#>"
    prologue: Prologue = Prologue(base, {"foaf": foaf, "ns": ns})
    expected: str = f'''
        BASE {base}
        PREFIX foaf: {foaf}
        PREFIX ns: {ns}
    '''
    assert remove_whitespace(expected) == remove_whitespace(str(prologue))

def test_select_clause_to_str() -> None:
    select: SelectClause = SelectClause()
    select.set_select_all()
    expected: str = "SELECT *"
    assert expected == str(select)

    altitude, temp, avg_temp = "?altitude", "?temp", "?avg_temp"
    select = SelectClause()
    select.add_explicit_vars(set([altitude, temp]))
    select.set_derived_var(avg_temp, Function("AVG", [TerminalExpr(temp)]))
    select.make_distinct()
    expected: str = f"SELECT {altitude} {temp} (AVG({temp}) AS {avg_temp})"
    assert expected == str(select)

def test_dataset_clause_to_str() -> None:
    ds_id = "<http://ex.com/GraphInstance-1234>"
    dataset: DatasetClause = DatasetClause(ds_id, is_named=True)
    expected: str = f"FROM NAMED {ds_id}"
    assert expected == str(dataset)

def test_ggp_sub_to_str() -> None:
    raise NotImplementedError()

def test_triples_block_to_str() -> None:
    raise NotImplementedError()

def test_ggp_to_str() -> None:
    raise NotImplementedError()

def test_simple_expr_to_str() -> None:
    raise NotImplementedError()

def test_multi_expr_to_str() -> None:
    raise NotImplementedError()

def test_verb_path_to_str() -> None:
    raise NotImplementedError()

def test_soln_modifier_to_str() -> None:
    raise NotImplementedError()
