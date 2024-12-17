from src import QueryParser, Query, LookaheadQueue, Prologue, SelectClause, \
    GroupConcatFunction, TerminalExpr, Token, QueryTerm as qt, \
    DatasetClause, WhereClause, GroupGraphPatternSub, TriplesBlock, Filter, \
    GraphGraphPattern, SubSelect, MultiExprExpr, IdentityFunction, SolnModifier, \
    GroupClause, Function, OrderClause, LimitOffsetClause, HavingClause, ExprOp
from typing import List, Any

SIMPLE_SELECT: List[Token] = [Token(qt.SELECT), Token(qt.ASTERISK)]
SIMPLE_WHERE: List[Token] = [Token(qt.WHERE), Token(qt.LBRACKET),
                             Token(qt.RBRACKET), Token(qt.EOF)]

def test_parser_prologue() -> None:
    '''BASE <base_iri> PREFIX foaf:<foaf_iri> PREFIX rdf:<rdf_iri>'''

    base_iri: str = "http://ex.com/"
    foaf: str = "http://xmlns.com/foaf/0.1/"
    rdf: str = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    tokens: List[Token] = [
        Token(qt.BASE), Token(qt.IRIREF, base_iri), Token(qt.PREFIX),
        Token(qt.PREFIXED_NAME_PREFIX, "foaf"), Token(qt.COLON),
        Token(qt.IRIREF, foaf), Token(qt.PREFIX),
        Token(qt.PREFIXED_NAME_PREFIX, "rdf"), Token(qt.COLON),
        Token(qt.IRIREF, rdf)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    for token in (tokens + SIMPLE_SELECT + SIMPLE_WHERE):
        tok_queue.put(token)
    prologue: Prologue = QueryParser().parse(tok_queue).prologue
    assert prologue.base_iri == base_iri
    assert len(prologue.prefixes) == 2
    assert prologue.prefixes["foaf"] == foaf
    assert prologue.prefixes["rdf"] == rdf

def test_parser_select_clause() -> None:
    '''SELECT DISTINCT ?fName ?age
        (GROUP_CONCAT(DISTINCT ?concat_subject_attribute; SEPARATOR=" ~~~~ ") AS ?subject_attributes)
        ?lName
    '''
    fname, age, concat_subj_attr, sep = "?fName", "?age", "?concat_subject_attribute", " ~~~~ "
    sub_attr, lname = "?subject_attributes", "?lName"
    tokens: List[Token] = [
        Token(qt.SELECT), Token(qt.DISTINCT), Token(qt.VARIABLE, fname),
        Token(qt.VARIABLE, age), Token(qt.LPAREN), Token(qt.GROUP_CONCAT),
        Token(qt.LPAREN), Token(qt.DISTINCT), Token(qt.VARIABLE, concat_subj_attr),
        Token(qt.SEMI_COLON), Token(qt.SEPARATOR), Token(qt.EQUALS),
        Token(qt.STRING_LITERAL, sep), Token(qt.RPAREN), Token(qt.AS),
        Token(qt.VARIABLE, sub_attr), Token(qt.RPAREN), Token(qt.VARIABLE, lname)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    for token in (tokens + SIMPLE_WHERE):
        tok_queue.put(token)
    query: Query = QueryParser().parse(tok_queue)
    select_clause: SelectClause = query.select_query.select_clause
    assert query.prologue is None
    assert select_clause.explicit_vars == set([fname, age, lname])
    assert select_clause.is_distinct
    assert not select_clause.is_select_all
    assert len(select_clause.derived_vars) == 1
    assert sub_attr in select_clause.derived_vars
    gc_func: GroupConcatFunction = select_clause.derived_vars[sub_attr]
    assert isinstance(gc_func, GroupConcatFunction)
    assert gc_func.is_distinct
    assert isinstance(gc_func.args[0], TerminalExpr)
    assert gc_func.args[0].stringified_val == concat_subj_attr
    assert gc_func.separator == sep


def test_parser_dataset_clause() -> None:
    '''FROM NAMED ex:Graph-uuid'''

    prefix, graph_uuid = "ex", "Graph-uuid"
    tokens: List[Token] = [
        Token(qt.FROM), Token(qt.NAMED), Token(qt.PREFIXED_NAME_PREFIX, prefix),
        Token(qt.COLON), Token(qt.PREFIXED_NAME_LOCAL, graph_uuid)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    for token in (SIMPLE_SELECT + tokens + SIMPLE_WHERE):
        tok_queue.put(token)
    dataset_clause: DatasetClause = QueryParser().parse(tok_queue).select_query.dataset_clause
    assert dataset_clause.is_named
    assert dataset_clause.dataset == f"{prefix}:{graph_uuid}"

def test_parser_where_clause() -> None:
    '''WHERE {
        {
            SELECT *
            WHERE {}
        }
        ?person1 foaf:firstName "Bob" ;
                foaf:age ?age .
        ?person2 foaf:nick "Sqeej" .
        FILTER (?age = 26)
        GRAPH ?my_graph {}
        ?person3 foaf:nick "Lucky" .
    }'''
    p1, p2, p3, foaf, fName = "?person1", "?person2", "person3", "foaf", "firstName"
    nick, sqeej, my_graph = "nick", "Sqeej", "my_graph"
    age, age_var, lucky, bob, number = "age", "?age", "Lucky", "Bob", "26"
    tokens: List[Token] = [
        Token(qt.WHERE), Token(qt.LBRACKET), Token(qt.LBRACKET), Token(qt.SELECT),
        Token(qt.ASTERISK), Token(qt.WHERE), Token(qt.LBRACKET), Token(qt.RBRACKET),
        Token(qt.RBRACKET), Token(qt.VARIABLE, p1), Token(qt.PREFIXED_NAME_PREFIX, foaf),
        Token(qt.COLON), Token(qt.PREFIXED_NAME_LOCAL, fName), Token(qt.STRING_LITERAL, bob),
        Token(qt.SEMI_COLON), Token(qt.PREFIXED_NAME_PREFIX, foaf), Token(qt.COLON),
        Token(qt.PREFIXED_NAME_LOCAL, age), Token(qt.VARIABLE, age_var), Token(qt.PERIOD),
        Token(qt.VARIABLE, p2), Token(qt.PREFIXED_NAME_PREFIX, foaf), Token(qt.COLON),
        Token(qt.PREFIXED_NAME_LOCAL, nick), Token(qt.STRING_LITERAL, sqeej), Token(qt.PERIOD),
        Token(qt.FILTER), Token(qt.LPAREN), Token(qt.VARIABLE, age_var), Token(qt.EQUALS),
        Token(qt.NUMBER_LITERAL, number), Token(qt.RPAREN), Token(qt.GRAPH), Token(qt.VARIABLE, my_graph),
        Token(qt.LBRACKET), Token(qt.RBRACKET), Token(qt.VARIABLE, p3),
        Token(qt.PREFIXED_NAME_PREFIX, foaf), Token(qt.COLON), Token(qt.PREFIXED_NAME_LOCAL, nick),
        Token(qt.STRING_LITERAL, lucky), Token(qt.PERIOD), Token(qt.RBRACKET), Token(qt.EOF)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    for token in (SIMPLE_SELECT + tokens):
        tok_queue.put(token)
    where_clause: WhereClause = QueryParser().parse(tok_queue).select_query.where_clause
    assert where_clause.uses_keyword
    ggp_sub: GroupGraphPatternSub = where_clause.ggp
    assert isinstance(ggp_sub, GroupGraphPatternSub)
    assert [len(ggp_sub.triples_blocks), len(ggp_sub.patterns), len(ggp_sub.modifiers)] == [2, 2, 1]
    elements: List[Any] = ggp_sub.elements_in_order()
    assert isinstance(elements[0], SubSelect)
    assert isinstance(elements[1], TriplesBlock)
    assert isinstance(elements[2], Filter)
    assert isinstance(elements[3], GraphGraphPattern)
    assert isinstance(elements[4], TriplesBlock)
    assert [elements[1].triples_same_subj[0].subj, elements[1].triples_same_subj[1].subj] == [p1, p2]
    assert isinstance(elements[2].expr, IdentityFunction)
    assert isinstance(elements[2].expr.args[0], MultiExprExpr)
    assert elements[3].var_or_iri == my_graph
    assert elements[4].triples_same_subj[0].subj == p3

def test_parser_where_clause_sub_select() -> None:
    '''WHERE {
        SELECT DISTINCT ?var
        WHERE {
            ?var a ex:Person
        }
    }'''
    var, ex, person = "?var", "ex", "Person"
    tokens: List[Token] = [
        Token(qt.WHERE), Token(qt.LBRACKET), Token(qt.SELECT), Token(qt.DISTINCT),
        Token(qt.VARIABLE, var), Token(qt.WHERE), Token(qt.LBRACKET), Token(qt.VARIABLE, var),
        Token(qt.A), Token(qt.PREFIXED_NAME_PREFIX, ex), Token(qt.COLON),
        Token(qt.PREFIXED_NAME_LOCAL, person), Token(qt.RBRACKET), Token(qt.RBRACKET), Token(qt.EOF)
    ]
    tok_queue: LookaheadQueue = LookaheadQueue()
    for token in (SIMPLE_SELECT + tokens):
        tok_queue.put(token)
    where_clause: WhereClause = QueryParser().parse(tok_queue).select_query.where_clause
    assert where_clause.uses_keyword
    sub_select: SubSelect = where_clause.ggp
    assert isinstance(sub_select, SubSelect)
    assert sub_select.select_clause.is_distinct
    assert len(sub_select.select_clause.explicit_vars) == 1
    assert sub_select.select_clause.explicit_vars == set([var])
    assert sub_select.where_clause.uses_keyword
    ggp_sub: GroupGraphPatternSub = sub_select.where_clause.ggp
    assert isinstance(ggp_sub, GroupGraphPatternSub)
    assert [len(ggp_sub.order_of_elements), len(ggp_sub.triples_blocks)] == [1, 1]
    assert len(ggp_sub.triples_blocks[ggp_sub.order_of_elements[0]].triples_same_subj) == 1
    assert ggp_sub.triples_blocks[ggp_sub.order_of_elements[0]].triples_same_subj[0].subj == var

def test_parser_soln_modifiers() -> None:
    '''
        GROUP BY ?var1 UCASE(?var2) (?count1 + ?count2 AS ?count) ?var3
        HAVING (SUM(?price) > 10)
        ORDER BY DESC(SUM(?price))
        LIMIT 10
        OFFSET 1
    '''
    var1, var2, c1, c2, c = "?var1", "?var2", "?count1", "?count2", "?count"
    price, ten, one, var3 = "?price", "10", "1", "?var3"
    tokens: List[Token] = [
        Token(qt.GROUP), Token(qt.BY), Token(qt.VARIABLE, var1), Token(qt.UCASE),
        Token(qt.LPAREN), Token(qt.VARIABLE, var2), Token(qt.RPAREN), Token(qt.LPAREN),
        Token(qt.VARIABLE, c1), Token(qt.ADD), Token(qt.VARIABLE, c2), Token(qt.AS),
        Token(qt.VARIABLE, c), Token(qt.RPAREN), Token(qt.VARIABLE, var3), Token(qt.HAVING),
        Token(qt.LPAREN), Token(qt.SUM), Token(qt.LPAREN), Token(qt.VARIABLE, price),
        Token(qt.RPAREN), Token(qt.GT), Token(qt.NUMBER_LITERAL, ten), Token(qt.RPAREN),
        Token(qt.ORDER), Token(qt.BY), Token(qt.DESC), Token(qt.LPAREN), Token(qt.SUM),
        Token(qt.LPAREN), Token(qt.VARIABLE, price), Token(qt.RPAREN), Token(qt.RPAREN),
        Token(qt.LIMIT), Token(qt.NUMBER_LITERAL, ten),
        Token(qt.OFFSET), Token(qt.NUMBER_LITERAL, one), Token(qt.EOF)
    ]
    tok_queue: LookaheadQueue = LookaheadQueue()
    for token in (SIMPLE_SELECT + [Token(qt.LBRACKET), Token(qt.RBRACKET)] + tokens):
        tok_queue.put(token)
    s_mod: SolnModifier = QueryParser().parse(tok_queue).select_query.soln_modifier
    gc: GroupClause = s_mod.group_clause
    assert [len(gc.built_in_calls), len(gc.derived_vars), len(gc.vars)] == [1, 1, 2]
    assert isinstance(gc.built_in_calls[0], Function) and gc.built_in_calls[0].func_name == "UCASE"
    add_expr: MultiExprExpr = gc.derived_vars[c]
    assert isinstance(add_expr, MultiExprExpr)
    assert add_expr.l_expr.stringified_val == c1 and add_expr.r_expr.stringified_val == c2
    assert gc.vars[0] == var1 and gc.vars[1] == var3
    hc_expr: HavingClause = s_mod.having_clause.expressions[0]
    assert isinstance(hc_expr, IdentityFunction) and isinstance(hc_expr.args[0], MultiExprExpr)
    assert isinstance(hc_expr.args[0].l_expr, Function) and isinstance(hc_expr.args[0].r_expr, TerminalExpr)
    assert isinstance(hc_expr.args[0].l_expr.args[0], TerminalExpr)
    assert hc_expr.args[0].r_expr.stringified_val == ten and hc_expr.args[0].expr_op == ExprOp.GT
    assert hc_expr.args[0].l_expr.func_name == "SUM" and hc_expr.args[0].l_expr.args[0].stringified_val == price
    oc_expr: OrderClause = s_mod.order_clause.expressions[0]
    assert isinstance(oc_expr, Function) and oc_expr.func_name == "DESC" and len(oc_expr.args) == 1
    assert isinstance(oc_expr.args[0], Function) and oc_expr.args[0].func_name == "SUM"
    assert isinstance(oc_expr.args[0].args[0], TerminalExpr) and oc_expr.args[0].args[0].stringified_val == price
    loc: LimitOffsetClause = s_mod.limit_offset_clause
    assert loc.limit_first
    assert loc.limit == int(ten)
    assert loc.offset == int(one)
