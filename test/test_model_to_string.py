from src import Prologue, DatasetClause, SelectClause, GraphGraphPattern, \
    GroupGraphPatternSub, UnionGraphPattern, ServiceGraphPattern, OptionalGraphPattern, \
    MinusGraphPattern, Bind, Filter, SolnModifier, MultiExprExpr, Function, \
    AggregateFunction, IdentityFunction, ExistenceExpr, TriplesBlock, \
    TriplesSameSubj, ElementVerbPath, InverseVerbPath, IdentityVerbPath, \
    TerminalVerbPath, MultiPathVerbPath, TerminalExpr, GroupClause, HavingClause, \
    LimitOffsetClause, OrderClause, Expression, ExprOp
from typing import List
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
    iri = "ex:GraphInstance-1234"
    graph_graph: GraphGraphPattern = GraphGraphPattern(iri)
    expected: str = f"GRAPH {iri} {{ }}"
    assert expected == remove_whitespace(str(graph_graph))

    union: UnionGraphPattern = UnionGraphPattern()
    expected: str = "{ } UNION { }"
    assert expected == remove_whitespace(str(union))
    
    optional: OptionalGraphPattern = OptionalGraphPattern()
    expected: str = "OPTIONAL { }"
    assert expected == remove_whitespace(str(optional))

    minus: MinusGraphPattern = MinusGraphPattern()
    expected: str = "MINUS { }"
    assert expected == remove_whitespace(str(minus))

    is_silent: bool = True
    service: ServiceGraphPattern = ServiceGraphPattern(is_silent, iri)
    expected: str = f"SERVICE SILENT {iri} {{ }}"
    assert expected == remove_whitespace(str(service))

def test_pattern_mods() -> None:
    t = "true"
    filter: Filter = Filter(IdentityFunction(TerminalExpr(t)))
    expected: str = f"FILTER ({t})"
    assert expected == str(filter)

    lc_var, uc_var = "?lc_var", "?uc_var"
    bind: Bind = Bind(Function("UCASE", [TerminalExpr(lc_var)]), uc_var)
    expected: str = f"BIND (UCASE({lc_var}) AS {uc_var})"
    assert expected == str(bind)

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
    limit, offset, x, y, zero, hundred = 20, 1, "?x", "?y", "0" "100"
    soln_mod: SolnModifier = SolnModifier()
    gc: GroupClause = GroupClause()
    gc.add_var(x)
    gc.add_expr(Function("ROUND", y))
    soln_mod.set_group_clause(gc)
    having_exprs: List[Expression] = [
        IdentityFunction(MultiExprExpr(TerminalExpr(y), zero, ExprOp(">"))),
        IdentityFunction(MultiExprExpr(TerminalExpr(y), hundred, ExprOp("<")))]
    soln_mod.set_having_clause(HavingClause(having_exprs))
    soln_mod.set_order_clause(OrderClause([Function("ASC", [TerminalExpr(x)]), TerminalExpr(y)]))
    soln_mod.set_limit_offset_clause(LimitOffsetClause(limit, offset, False))
    
    expected: str = f'''
    GROUP BY {x} ROUND({y})
    HAVING ({y} > {zero}) ({y} < {hundred})
    ORDER BY ASC({x}) {y}
    OFFSET {offset}
    LIMIT {limit}
    '''
    assert remove_whitespace(expected) == remove_whitespace(str(soln_mod))
