from src import Prologue, DatasetClause, SelectClause, GraphGraphPattern, \
    GroupGraphPatternSub, UnionGraphPattern, ServiceGraphPattern, OptionalGraphPattern, \
    MinusGraphPattern, Bind, Filter, SolnModifier, MultiExprExpr, Function, \
    AggregateFunction, IdentityFunction, ExistenceExpr, TriplesBlock, \
    TriplesSameSubj, ElementVerbPath, InverseVerbPath, IdentityVerbPath, \
    TerminalVerbPath, MultiPathVerbPath, TerminalExpr, GroupClause, HavingClause, \
    LimitOffsetClause, OrderClause, Expression, ExprOp, Verb, VarVerb, VerbPath, \
    PathOp, PathMod, NegationExpr, GroupConcatFunction, SubSelect, WhereClause
from typing import List, Dict, Set
from .utilities_for_test import remove_whitespace
from copy import deepcopy

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
    expected: str = "SELECT *\n"
    assert expected == str(select)

    altitude, temp, avg_temp = "?altitude", "?temp", "?avg_temp"
    select = SelectClause()
    select.add_explicit_vars(set([altitude, temp]))
    select.set_derived_var(avg_temp, Function("AVG", [TerminalExpr(temp)]))
    select.make_distinct()
    expected: str = f"SELECT DISTINCT {altitude} (AVG({temp}) AS {avg_temp}) {temp}"
    assert expected == remove_whitespace(str(select))

def test_dataset_clause_to_str() -> None:
    ds_id = "<http://ex.com/GraphInstance-1234>"
    dataset: DatasetClause = DatasetClause(ds_id, is_named=True)
    expected: str = f"FROM NAMED {ds_id}\n"
    assert expected == str(dataset)

def test_ggp_sub_to_str() -> None:
    iri = "ex:GraphInstance-1234"
    graph_graph: GraphGraphPattern = GraphGraphPattern(iri)
    expected: str = f"GRAPH {iri} {{ }}"
    assert expected == remove_whitespace(str(graph_graph))

    union: UnionGraphPattern = UnionGraphPattern([GroupGraphPatternSub(), GroupGraphPatternSub()])
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
    expected: str = f"BIND(UCASE({lc_var}) AS {uc_var})"
    assert expected == str(bind)

def test_triples_block_to_str() -> None:
    ''' ?sub1 ex:pred1 "literal1", "literal2" .
        ?sub2 ex:pred2 ex:Entity-1234 .
        ?sub3 ex:pred3_1 ?obj3_1 ;
                ex:pred3_2 ?obj3_2 .
    '''
    s1, s2, s3, p1, p2 = "?sub1", "?sub2", "?sub3", "ex:pred1", "ex:pred2"
    objs1_list, p3_1, p3_2 = ["literal1", "literal2"], "ex:pred3_1", "ex:pred3_2"
    objs1, objs2, objs3_1, objs3_2 = set(objs1_list), set(["ex:Entity-1234"]), set(["?obj3_1"]), set(["?obj3_2"])
    pred_objs: List[Dict[Verb, Set[str]]] = [
        {TerminalVerbPath(p1): objs1}, {TerminalVerbPath(p2): objs2}, {TerminalVerbPath(p3_1): objs3_1,
                                                                       TerminalVerbPath(p3_2): objs3_2}
    ]
    unique_subj_trips: List[TriplesSameSubj] = []
    for s, po in zip([s1, s2, s3], pred_objs):
        tss = TriplesSameSubj(s)
        tss.add_po_dict(deepcopy(po))
        unique_subj_trips.append(tss)
    triples_block: TriplesBlock = TriplesBlock()
    triples_block.add_unique_subj_triples(unique_subj_trips)
    expected: str = f'''
    {s1} {p1} {", ".join(objs1_list)} .
    {s2} {p2} {objs2.pop()} .
    {s3} {p3_1} {objs3_1.pop()} ;
        {p3_2} {objs3_2.pop()} .
    '''
    assert remove_whitespace(expected) == remove_whitespace(str(triples_block))

def test_ggp_to_str() -> None:
    '''
    {
        {
            SELECT *
            WHERE {
                GRAPH ex:MyGraph {
                    ?person a ex:Human .
                    OPTIONAL {
                        ?person ex:hasAge ?age .
                    }
                    FILTER(?age < 18)
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
    }
    '''
    person, human, has_age, age, val = "?person", "ex:Human", "ex:hasAge", "?age", "?val"
    s, p, o, iri2, has_pet, pet = "?subj", "ex:pred", "?obj", "ex:GraphInstance-1234", "ex:hasPet", "?pet"
    name, pet_name, iri1 = "ex:name", "?pet_name", "ex:MyGraph"

    tb = TriplesBlock()
    tss = TriplesSameSubj(person)
    tss.add_po(TerminalVerbPath("a"), human)
    tb.add_same_subj_triples(tss)
    gr_gr_1 = GraphGraphPattern(iri1)
    gr_gr_1.add_triples_block(tb)
    opt = OptionalGraphPattern()
    tb = TriplesBlock()
    tss = TriplesSameSubj(person)
    tss.add_po(TerminalVerbPath(has_age), age)
    tb.add_same_subj_triples(tss)
    opt.add_triples_block(tb)
    gr_gr_1.add_pattern(opt)
    filt = Filter(IdentityFunction(MultiExprExpr(TerminalExpr(age), TerminalExpr("18"), ExprOp("<"))))
    gr_gr_1.add_modifier(filt)

    sub_sel, sel_clause = SubSelect(), SelectClause()
    sel_clause.set_select_all()
    sub_sel.set_select_clause(sel_clause)
    sub_sel.set_where_clause(WhereClause(GroupGraphPatternSub(patterns=[gr_gr_1]), True))
    r_union = GroupGraphPatternSub()
    r_union.add_modifier(Bind(TerminalExpr("-23.1"), val))
    l_union = GroupGraphPatternSub()
    l_union.add_pattern(sub_sel)
    top_lvl = GroupGraphPatternSub()
    top_lvl.add_pattern(UnionGraphPattern([l_union, r_union]))

    gr_gr_2 = GraphGraphPattern(iri2)
    tb = TriplesBlock()
    tss1, tss2 = TriplesSameSubj(person), TriplesSameSubj(pet)
    tss1.add_po(TerminalVerbPath(has_pet), pet)
    tss2.add_po(TerminalVerbPath(name), pet_name)
    tb.add_unique_subj_triples([tss1, tss2])
    gr_gr_2.add_triples_block(tb)
    tb = TriplesBlock()
    tss = TriplesSameSubj(s)
    tss.add_po(TerminalVerbPath(p), o)
    tb.add_same_subj_triples(tss)
    top_lvl.add_triples_block(tb)
    top_lvl.add_pattern(gr_gr_2)
    expected: str = f'''
    {{
        {{
            SELECT *
            WHERE {{
                GRAPH {iri1} {{
                    {person} a {human} .
                    OPTIONAL {{
                        {person} {has_age} {age} .
                    }}
                    FILTER ({age} < 18)
                }}
            }}
        }}
        UNION
        {{
            BIND(-23.1 AS {val})
        }}
        {s} {p} {o} .
        GRAPH {iri2} {{
            {person} {has_pet} {pet} .
            {pet} {name} {pet_name} .
        }}
    }}
    '''
    assert remove_whitespace(expected) == remove_whitespace(str(top_lvl))

def test_simple_expr_to_str() -> None:
    num = "-12.7"
    func: Function = Function("CEIL", [TerminalExpr(num)])
    expected: str = f"CEIL({num})"
    assert expected == str(func)

    word, indx = "Hello world", "7"
    func_2arg: Function = Function("SUBSTR", [TerminalExpr(word, is_quoted=True), TerminalExpr(indx)])
    expected: str = f"SUBSTR(\"{word}\", {indx})"
    assert expected == str(func_2arg)

    id_func: IdentityFunction = IdentityFunction(TerminalExpr(num))
    expected: str = f"({num})"
    assert expected == str(id_func)

    is_distinct = True
    agg: AggregateFunction = AggregateFunction("SUM", TerminalExpr(num), is_distinct)
    expected: str = f"SUM(DISTINCT {num})"
    assert expected == str(agg)

    sep = "~~"
    gc_func: GroupConcatFunction = GroupConcatFunction(TerminalExpr(num), is_distinct, sep)
    expected: str = f"GROUP_CONCAT(DISTINCT {num}; SEPARATOR=\"{sep}\")"
    assert expected == str(gc_func)

    neg_expr: NegationExpr = NegationExpr(TerminalExpr(num))
    expected: str = f"!{num}"
    assert expected == str(neg_expr)

    not_exists = True
    ex_expr: ExistenceExpr = ExistenceExpr(GroupGraphPatternSub(), not_exists)
    expected: str = "NOT EXISTS { }"
    assert expected == str(ex_expr)

def test_multi_expr_to_str() -> None:
    ''' ((?price/(SUM(0.9) + 0.1) != -50.0) || false) '''
    price, num1, num2, num3 = "?price", "0.9", "0.1", "-50.0"
    e_sub3 = MultiExprExpr(Function("SUM", [TerminalExpr(num1)]), TerminalExpr(num2), ExprOp("+"))
    e_sub2 = MultiExprExpr(TerminalExpr(price), IdentityFunction(e_sub3), ExprOp("/"))
    e_sub1 = MultiExprExpr(e_sub2, TerminalExpr(num3), ExprOp("!="))
    expr = IdentityFunction(MultiExprExpr(IdentityFunction(e_sub1), TerminalExpr("false"), ExprOp("||")))
    expected: str = f"(({price} / (SUM({num1}) + {num2}) != {num3}) || false)"
    assert expected == str(expr)

def test_verb_path_to_str() -> None:
    '''((ex:alias?/ex:subDept*/ex:member)|ex:owner)/ex:hasPet'''
    has_pet, owner, member, sub_dept = "ex:hasPet", "ex:owner", "ex:member", "ex:subDept"
    alias = "ex:alias"
    vp_sub5: VerbPath = ElementVerbPath(TerminalVerbPath(sub_dept), PathMod("*"))
    vp_sub4: VerbPath = MultiPathVerbPath(vp_sub5, TerminalVerbPath(member), PathOp("/"))
    vp_sub3: VerbPath = ElementVerbPath(TerminalVerbPath(alias), PathMod("?"))
    vp_sub2: VerbPath = MultiPathVerbPath(vp_sub3, vp_sub4, PathOp("/"))
    vp_sub1: VerbPath = MultiPathVerbPath(IdentityVerbPath(vp_sub2), TerminalVerbPath(owner), PathOp("|"))
    vp: VerbPath = MultiPathVerbPath(IdentityVerbPath(vp_sub1), TerminalVerbPath(has_pet), PathOp("/"))
    expected: str = f"(({alias}? / {sub_dept}* / {member}) | {owner}) / {has_pet}"
    assert expected == str(vp)

def test_soln_modifier_to_str() -> None:
    limit, offset, x, y, zero, hundred = 20, 1, "?x", "?y", "0", "100"
    soln_mod: SolnModifier = SolnModifier()
    gc: GroupClause = GroupClause()
    gc.add_var(x)
    gc.add_expr(Function("ROUND", [y]))
    soln_mod.set_group_clause(gc)
    having_exprs: List[Expression] = [
        IdentityFunction(MultiExprExpr(TerminalExpr(y), TerminalExpr(zero), ExprOp(">"))),
        IdentityFunction(MultiExprExpr(TerminalExpr(y), TerminalExpr(hundred), ExprOp("<")))]
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
