from src import QueryParser, Query, LookaheadQueue, Prologue, SelectClause, \
    GroupConcatFunction, TerminalExpr, Tokenizer, Token, QueryTerm as qt, \
    DatasetClause, WhereClause, GroupGraphPatternSub, TriplesBlock, Filter, \
    GraphGraphPattern, SubSelect, MultiExprExpr, IdentityFunction, SolnModifier, \
    GroupClause, Function, OrderClause, LimitOffsetClause, HavingClause, ExprOp, \
    ExistenceExpr, AggregateFunction
from typing import List, Any

def test_parser_base_decl() -> None:
    '''BASE <http://ex.com/>'''

    base_iri: str = "<http://ex.com/>"
    tokens: List[Token] = [Token(qt.BASE), Token(qt.IRIREF, base_iri)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    prologue: Prologue = Prologue()
    QueryParser().base_decl(tok_queue, prologue)
    assert prologue.base_iri == base_iri

def test_parser_prefix_decl() -> None:
    ''' PREFIX foaf: <http://xmlns.com/foaf/0.1/>'''

    foaf: str = "<http://xmlns.com/foaf/0.1/>"
    tokens: List[Token] = [
        Token(qt.PREFIX), Token(qt.PREFIXED_NAME_PREFIX, "foaf"), Token(qt.COLON),
        Token(qt.IRIREF, foaf)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    prologue: Prologue = Prologue()
    QueryParser().prefix_decl(tok_queue, prologue)
    assert len(prologue.prefixes) == 1 and prologue.prefixes["foaf"] == foaf

def test_parser_derived_var() -> None:
    ''' ((?old_name) AS ?new_name)'''

    old_name, new_name = "?old_name", "?new_name"
    tokens: List[Token] = [
        Token(qt.LPAREN), Token(qt.LPAREN), Token(qt.VARIABLE, old_name), Token(qt.RPAREN),
        Token(qt.AS), Token(qt.VARIABLE, new_name), Token(qt.RPAREN)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    var, expr = QueryParser().derived_var(tok_queue)
    assert var == new_name
    assert isinstance(expr, IdentityFunction)
    assert expr.args[0].stringified_val == old_name

def test_parser_built_in_call_existence() -> None:
    ''' NOT EXISTS {?s foaf:nick "Squeej"}
        EXISTS {?s foaf:nick "Squeej"}'''
    var, foaf, nick, sqeej = "?s", "foaf", "nick", "Squeej"
    tokens: List[Token] = [
        Token(qt.NOT), Token(qt.EXISTS), Token(qt.LBRACKET), Token(qt.VARIABLE, var),
        Token(qt.PREFIXED_NAME_PREFIX, foaf), Token(qt.COLON), Token(qt.PREFIXED_NAME_LOCAL, nick),
        Token(qt.STRING_LITERAL, sqeej), Token(qt.RBRACKET)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    ex_expr = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(ex_expr, ExistenceExpr)
    assert ex_expr.not_exists
    ggp_elems: List[Any] = ex_expr.ggp.elements_in_order()
    assert len(ggp_elems) == 1 and isinstance(ggp_elems[0], TriplesBlock)

    tokens, tok_queue = tokens[1:], LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    ex_expr = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(ex_expr, ExistenceExpr)
    assert not ex_expr.not_exists
    ggp_elems: List[Any] = ex_expr.ggp.elements_in_order()
    assert len(ggp_elems) == 1 and isinstance(ggp_elems[0], TriplesBlock)
    
def test_parser_built_in_call_concat() -> None:
    ''' CONCAT(?fName, " ", ?mInit, ". ", ?lName)'''
    ele1, ele2, ele3, ele4, ele5 = "?fname", " ", "?mInit", ". ", "?lName"
    tokens: List[Token] = [
        Token(qt.CONCAT), Token(qt.LPAREN), Token(qt.VARIABLE, ele1), Token(qt.COMMA),
        Token(qt.STRING_LITERAL, ele2), Token(qt.COMMA), Token(qt.VARIABLE, ele3),
        Token(qt.COMMA), Token(qt.STRING_LITERAL, ele4), Token(qt.COMMA),
        Token(qt.VARIABLE, ele5), Token(qt.RPAREN)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    func = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(func, Function)
    assert func.func_name == "CONCAT"
    assert [v.stringified_val for v in func.args] == [ele1, ele2, ele3, ele4, ele5]

def test_parser_built_in_call_regex() -> None:
    ''' REGEX(?name, "^Ali")
        REGEX(?name, "^ali", "i")'''
    name, pat1, pat2, flag = "?name", "^Ali", "^ali", "-i"
    tokens: List[Token] = [
        Token(qt.REGEX), Token(qt.LPAREN), Token(qt.VARIABLE, name), Token(qt.COMMA),
        Token(qt.STRING_LITERAL, pat1), Token(qt.RPAREN)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    func = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(func, Function)
    assert func.func_name == "REGEX"
    assert [v.stringified_val for v in func.args] == [name, pat1]

    tokens = tokens[:len(tokens) - 2] + [Token(qt.STRING_LITERAL, pat2), Token(qt.COMMA),
                                         Token(qt.STRING_LITERAL, flag), Token(qt.RPAREN)]
    tok_queue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    func = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(func, Function)
    assert func.func_name == "REGEX"
    assert [v.stringified_val for v in func.args] == [name, pat2, flag]

def test_parser_built_in_call_substr() -> None:
    ''' SUBSTR("HiddenHi!", 7)
        SUBSTR("HidHi!den", 4, 3)'''
    word1, word2, start1, start2, length = "HiddenHi!", "HidHi!den", "7", "4", "3"
    tokens: List[Token] = [
        Token(qt.SUBSTR), Token(qt.LPAREN), Token(qt.STRING_LITERAL, word1), Token(qt.COMMA),
        Token(qt.NUMBER_LITERAL, start1), Token(qt.RPAREN)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    func = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(func, Function)
    assert func.func_name == "SUBSTR"
    assert [v.stringified_val for v in func.args] == [word1, start1]

    tokens = [Token(qt.SUBSTR), Token(qt.LPAREN), Token(qt.STRING_LITERAL, word2),
              Token(qt.COMMA), Token(qt.NUMBER_LITERAL, start2), Token(qt.COMMA),
              Token(qt.NUMBER_LITERAL, length), Token(qt.RPAREN)]
    tok_queue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    func = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(func, Function)
    assert func.func_name == "SUBSTR"
    assert [v.stringified_val for v in func.args] == [word2, start2, length]
    
def test_parser_built_in_call_replace() -> None:
    ''' REPLACE(?var, " ", "")
        REPLACE(?var, "REMOVE", "", "i")'''
    var, space, empty, remove, flag = "?var", " ", "", "REMOVE", "i"
    tokens: List[Token] = [
        Token(qt.REPLACE), Token(qt.LPAREN), Token(qt.VARIABLE, var), Token(qt.COMMA),
        Token(qt.STRING_LITERAL, space), Token(qt.COMMA), Token(qt.STRING_LITERAL, empty),
        Token(qt.RPAREN)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    func = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(func, Function)
    assert func.func_name == "REPLACE"
    assert [v.stringified_val for v in func.args] == [var, space, empty]

    tokens = [
        Token(qt.REPLACE), Token(qt.LPAREN), Token(qt.VARIABLE, var), Token(qt.COMMA),
        Token(qt.STRING_LITERAL, remove), Token(qt.COMMA), Token(qt.STRING_LITERAL, empty),
        Token(qt.COMMA), Token(qt.STRING_LITERAL, flag), Token(qt.RPAREN)]
    tok_queue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    func = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(func, Function)
    assert func.func_name == "REPLACE"
    assert [v.stringified_val for v in func.args] == [var, remove, empty, flag]
    
def test_parser_built_in_call_unary_function() -> None:
    ''' CEIL(?price)'''
    price = "?price"
    tokens: List[Token] = [
        Token(qt.CEIL), Token(qt.LPAREN), Token(qt.VARIABLE, price), Token(qt.RPAREN)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    func = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(func, Function)
    assert func.func_name == "CEIL"
    assert [v.stringified_val for v in func.args] == [price]

def test_parser_aggregate_count() -> None:
    ''' COUNT(DISTINCT *)
        COUNT(?names)'''
    names = "?names"
    tokens: List[Token] = [
        Token(qt.COUNT), Token(qt.LPAREN), Token(qt.DISTINCT), Token(qt.ASTERISK),
        Token(qt.RPAREN)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    aggr = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(aggr, AggregateFunction)
    assert aggr.func_name == "COUNT"
    assert aggr.is_distinct
    assert [v.stringified_val for v in aggr.args] == ["*"]

    tokens = [
        Token(qt.COUNT), Token(qt.LPAREN), Token(qt.VARIABLE, names),
        Token(qt.RPAREN)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    aggr = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(aggr, AggregateFunction)
    assert aggr.func_name == "COUNT"
    assert not aggr.is_distinct
    assert [v.stringified_val for v in aggr.args] == [names]

def test_parser_aggregate_sum() -> None:
    ''' SUM(?fees + (?cost * ?int_rate))'''
    fees, cost, int_rate = "?fees", "?cost", "?int_rate"
    tokens: List[Token] = [
        Token(qt.SUM), Token(qt.LPAREN), Token(qt.VARIABLE, fees),
        Token(qt.ADD), Token(qt.LPAREN), Token(qt.VARIABLE, cost), Token(qt.ASTERISK),
        Token(qt.VARIABLE, int_rate), Token(qt.RPAREN), Token(qt.RPAREN)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    aggr = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(aggr, AggregateFunction)
    assert aggr.func_name == "SUM"
    assert not aggr.is_distinct
    assert len(aggr.args) == 1 and isinstance(aggr.args[0], MultiExprExpr)
    assert aggr.args[0].l_expr.stringified_val == fees
    assert aggr.args[0].expr_op is ExprOp.ADD
    assert isinstance(aggr.args[0].r_expr, IdentityFunction) and isinstance(aggr.args[0].r_expr.args[0], MultiExprExpr)
    assert aggr.args[0].r_expr.args[0].l_expr.stringified_val == cost
    assert aggr.args[0].r_expr.args[0].expr_op is ExprOp.MULT
    assert aggr.args[0].r_expr.args[0].r_expr.stringified_val == int_rate
    
def test_parser_aggregate_min() -> None:
    ''' MIN(DISTINCT FLOOR(?cost))'''
    cost = "?cost"
    tokens: List[Token] = [
        Token(qt.MIN), Token(qt.LPAREN), Token(qt.DISTINCT), Token(qt.FLOOR),
        Token(qt.LPAREN), Token(qt.VARIABLE, cost), Token(qt.RPAREN), Token(qt.RPAREN)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    aggr = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(aggr, AggregateFunction)
    assert aggr.func_name == "MIN"
    assert aggr.is_distinct
    assert isinstance(aggr.args[0], Function) and aggr.args[0].func_name == "FLOOR"
    assert [v.stringified_val for v in aggr.args[0].args] == [cost]

def test_parser_aggregate_max() -> None:
    ''' MAX(STRLEN(?names))'''
    names = "?names"
    tokens: List[Token] = [
        Token(qt.MAX), Token(qt.LPAREN), Token(qt.STRLEN), Token(qt.LPAREN),
        Token(qt.VARIABLE, names), Token(qt.RPAREN), Token(qt.RPAREN)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    aggr = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(aggr, AggregateFunction)
    assert aggr.func_name == "MAX"
    assert not aggr.is_distinct
    assert isinstance(aggr.args[0], Function) and aggr.args[0].func_name == "STRLEN"
    assert [v.stringified_val for v in aggr.args[0].args] == [names]

def test_parser_aggregate_avg() -> None:
    ''' AVG(DISTINCT ?int_rate)'''
    int_rate = "?int_rate"
    tokens: List[Token] = [
        Token(qt.AVG), Token(qt.LPAREN), Token(qt.DISTINCT),
        Token(qt.VARIABLE, int_rate), Token(qt.RPAREN)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    aggr = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(aggr, AggregateFunction)
    assert aggr.func_name == "AVG"
    assert aggr.is_distinct
    assert [v.stringified_val for v in aggr.args] == [int_rate]

def test_parser_aggregate_sample() -> None:
    ''' SAMPLE(DISTINCT ((?names)))'''
    names = "?names"
    tokens: List[Token] = [
        Token(qt.SAMPLE), Token(qt.LPAREN), Token(qt.DISTINCT),
        Token(qt.LPAREN), Token(qt.LPAREN), Token(qt.VARIABLE, names),
        Token(qt.RPAREN), Token(qt.RPAREN), Token(qt.RPAREN)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    aggr = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(aggr, AggregateFunction)
    assert aggr.func_name == "SAMPLE"
    assert aggr.is_distinct
    assert isinstance(aggr.args[0], IdentityFunction) and isinstance(aggr.args[0].args[0], IdentityFunction)
    assert [v.stringified_val for v in aggr.args[0].args[0].args] == [names]

def test_parser_aggregate_group_concat() -> None:
    ''' GROUP_CONCAT(?names;SEPARATOR="->")'''
    names, sep = "?names", "->"
    tokens: List[Token] = [
        Token(qt.GROUP_CONCAT), Token(qt.LPAREN), Token(qt.VARIABLE, names),
        Token(qt.SEMI_COLON), Token(qt.SEPARATOR), Token(qt.EQUALS),
        Token(qt.STRING_LITERAL, sep), Token(qt.RPAREN)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    built_in_term: qt = tok_queue.get_now().term
    gc_func = QueryParser().built_in_call(built_in_term, tok_queue)
    assert isinstance(gc_func, GroupConcatFunction)
    assert gc_func.func_name == "GROUP_CONCAT"
    assert not gc_func.is_distinct
    assert [v.stringified_val for v in gc_func.args] == [names]
    assert gc_func.separator == sep

def test_parser_expr_list() -> None:
    raise NotImplementedError()

def test_parser_iri() -> None:
    raise NotImplementedError()

def test_parser_var_or_term() -> None:
    raise NotImplementedError()

def test_parser_property_list_path_not_empty() -> None:
    raise NotImplementedError()

def test_parser_group_condition() -> None:
    ''' GROUP BY (UCASE(?lName)) FLOOR(?age)  ?country (?x + ?y AS ?z)'''
    l_name, age, country, x, y, z = "?lName", "?age", "?country", "?x", "?y", "?z"
    tokens: List[Token] = [
        Token(qt.GROUP), Token(qt.BY), Token(qt.LPAREN), Token(qt.UCASE), Token(qt.LPAREN),
        Token(qt.VARIABLE, l_name), Token(qt.RPAREN), Token(qt.RPAREN),
        Token(qt.FLOOR), Token(qt.LPAREN), Token(qt.VARIABLE, age), Token(qt.RPAREN),
        Token(qt.VARIABLE, country), Token(qt.LPAREN), Token(qt.VARIABLE, x),
        Token(qt.ADD), Token(qt.VARIABLE, y), Token(qt.AS), Token(qt.VARIABLE, z),
        Token(qt.RPAREN), Token(qt.EOF)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    s_mod: SolnModifier = QueryParser().solution_modifier(tok_queue)
    assert [None, None, None] == [s_mod.having_clause, s_mod.order_clause, s_mod.limit_offset_clause]
    gc: GroupClause = s_mod.group_clause
    assert gc.vars == [country]
    assert len(gc.derived_vars) == 1 and len(gc.expressions) == 2
    assert isinstance(gc.derived_vars[z], MultiExprExpr) and gc.derived_vars[z].expr_op is ExprOp.ADD
    assert isinstance(gc.expressions[0], IdentityFunction) and isinstance(gc.expressions[1], Function)
    assert gc.expressions[0].args[0].func_name == "UCASE" and gc.expressions[1].func_name == "FLOOR"

def test_parser_having_condition() -> None:
    ''' HAVING (UCASE(?lName)) FLOOR(?age)  (?country)'''
    l_name, age, country = "?lName", "?age", "?country"
    tokens: List[Token] = [
        Token(qt.HAVING), Token(qt.LPAREN), Token(qt.UCASE), Token(qt.LPAREN),
        Token(qt.VARIABLE, l_name), Token(qt.RPAREN), Token(qt.RPAREN),
        Token(qt.FLOOR), Token(qt.LPAREN), Token(qt.VARIABLE, age), Token(qt.RPAREN),
        Token(qt.LPAREN), Token(qt.VARIABLE, country), Token(qt.RPAREN), Token(qt.EOF)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    s_mod: SolnModifier = QueryParser().solution_modifier(tok_queue)
    assert [None, None, None] == [s_mod.group_clause, s_mod.order_clause, s_mod.limit_offset_clause]
    hc: HavingClause = s_mod.having_clause
    assert len(hc.expressions) == 3 and isinstance(hc.expressions[0], IdentityFunction)
    assert isinstance(hc.expressions[1], Function) and isinstance(hc.expressions[2], IdentityFunction)
    assert hc.expressions[0].args[0].func_name == "UCASE" and hc.expressions[1].func_name == "FLOOR"
    assert hc.expressions[2].args[0].stringified_val == country

def test_parser_order_condition() -> None:
    ''' ORDER BY (UCASE(?lName)) FLOOR(?age)  ?country ASC(?dob)'''
    l_name, age, country, dob = "?lName", "?age", "?country", "?dob"
    tokens: List[Token] = [
        Token(qt.ORDER), Token(qt.BY), Token(qt.LPAREN), Token(qt.UCASE), Token(qt.LPAREN),
        Token(qt.VARIABLE, l_name), Token(qt.RPAREN), Token(qt.RPAREN),
        Token(qt.FLOOR), Token(qt.LPAREN), Token(qt.VARIABLE, age), Token(qt.RPAREN),
        Token(qt.VARIABLE, country), Token(qt.ASC), Token(qt.LPAREN), Token(qt.VARIABLE, dob),
        Token(qt.RPAREN), Token(qt.EOF)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    s_mod: SolnModifier = QueryParser().solution_modifier(tok_queue)
    assert [None, None, None] == [s_mod.group_clause, s_mod.having_clause, s_mod.limit_offset_clause]
    oc: OrderClause = s_mod.order_clause
    assert len(oc.expressions) == 4 and isinstance(oc.expressions[0], IdentityFunction)
    assert isinstance(oc.expressions[1], Function) and isinstance(oc.expressions[3], Function)
    assert oc.expressions[0].args[0].func_name == "UCASE" and oc.expressions[1].func_name == "FLOOR"
    assert oc.expressions[2].stringified_val == country and oc.expressions[3].func_name == "ASC"

def test_parser_limit_offset_condition() -> None:
    ''' LIMIT 100 OFFSET 10'''
    limit_val, offset_val = "100", "10"
    tokens: List[Token] = [
        Token(qt.LIMIT), Token(qt.NUMBER_LITERAL, limit_val), Token(qt.OFFSET),
        Token(qt.NUMBER_LITERAL, offset_val), Token(qt.EOF)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    s_mod: SolnModifier = QueryParser().solution_modifier(tok_queue)
    assert [None, None, None] == [s_mod.group_clause, s_mod.having_clause, s_mod.order_clause]
    loc: LimitOffsetClause = s_mod.limit_offset_clause
    assert loc.limit_first
    assert loc.limit == int(limit_val) and loc.offset == int(offset_val)

    ''' OFFSET 10 LIMIT 100'''
    limit_val, offset_val = "100", "10"
    tokens: List[Token] = [
        Token(qt.OFFSET), Token(qt.NUMBER_LITERAL, offset_val), Token(qt.LIMIT),
        Token(qt.NUMBER_LITERAL, limit_val), Token(qt.EOF)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    s_mod: SolnModifier = QueryParser().solution_modifier(tok_queue)
    assert [None, None, None] == [s_mod.group_clause, s_mod.having_clause, s_mod.order_clause]
    loc: LimitOffsetClause = s_mod.limit_offset_clause
    assert not loc.limit_first
    assert loc.limit == int(limit_val) and loc.offset == int(offset_val)

    ''' LIMIT 100'''
    limit_val = "100"
    tokens: List[Token] = [
        Token(qt.LIMIT), Token(qt.NUMBER_LITERAL, limit_val), Token(qt.EOF)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    s_mod: SolnModifier = QueryParser().solution_modifier(tok_queue)
    assert [None, None, None] == [s_mod.group_clause, s_mod.having_clause, s_mod.order_clause]
    loc: LimitOffsetClause = s_mod.limit_offset_clause
    assert loc.limit_first
    assert loc.limit == int(limit_val) and loc.offset is None

    ''' OFFSET 10'''
    offset_val = "10"
    tokens: List[Token] = [
        Token(qt.OFFSET), Token(qt.NUMBER_LITERAL, offset_val), Token(qt.EOF)]
    tok_queue: LookaheadQueue = LookaheadQueue()
    tok_queue.put_all(tokens)
    s_mod: SolnModifier = QueryParser().solution_modifier(tok_queue)
    assert [None, None, None] == [s_mod.group_clause, s_mod.having_clause, s_mod.order_clause]
    loc: LimitOffsetClause = s_mod.limit_offset_clause
    assert not loc.limit_first
    assert loc.limit is None and loc.offset == int(offset_val)
