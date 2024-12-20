from .tokens import QueryTerm, Token
from .Query import Query
from .SelectQuery import SelectQuery
from .SelectClause import SelectClause
from .Expressions import Expression, IdentityFunction, MultiExprExpr, \
    Function, AggregateFunction, NegationExpr, TerminalExpr, GroupConcatFunction
from .ExistenceExpr import ExistenceExpr
from .ExprOp import ExprOp
from .GroupGraphPattern import GroupGraphPattern, GroupGraphPatternSub, GraphGraphPattern, \
    OptionalGraphPattern, MinusGraphPattern, ServiceGraphPattern, UnionGraphPattern
from .PatternModifiers import PatternModifier, Filter, Bind
from .SolnModifier import SolnModifier, GroupClause, HavingClause, OrderClause, LimitOffsetClause
from .SubSelect import SubSelect
from .TriplesBlock import TriplesBlock
from .TriplesSameSubj import TriplesSameSubj
from .Verbs import Verb, VerbPath, VarVerb, MultiPathVerbPath, IdentityVerbPath, \
    InverseVerbPath, ElementVerbPath, TerminalVerbPath
from .PathEnums import PathMod, PathOp
from .DatasetClause import DatasetClause
from .WhereClause import WhereClause
from .Prologue import Prologue
from .LookaheadQueue import LookaheadQueue
from typing import List, Tuple, Dict, Set
from collections import defaultdict

class QueryParser:

    def __init__(self) -> None:
        pass
    
    def parse(self, tokens: LookaheadQueue) -> Query:
        return self.query(tokens)

    ''' Query ::= Prologue SelectQuery '''
    def query(self, tokens: LookaheadQueue) -> Query:
        prologue_starters: List[QueryTerm] = [QueryTerm.BASE, QueryTerm.PREFIX]
        lookahead: Token = tokens.lookahead()
        prologue: Prologue = None
        select_query: SelectQuery = None
        if lookahead.term in prologue_starters:
            prologue = self.prologue(tokens, Prologue())
        if tokens.lookahead().term is QueryTerm.SELECT:
            select_query: SelectQuery = self.select_query(tokens)
        elif prologue:
            self.throw_error([QueryTerm.SELECT], lookahead)
        else:
            self.throw_error(prologue_starters + [QueryTerm.SELECT], lookahead)
        
        next_tok: Token = tokens.get_now()
        if next_tok.term is QueryTerm.EOF:
            return Query(prologue, select_query)
        else:
            self.throw_error([QueryTerm.EOF], next_tok)

    ''' Prologue ::= (BaseDecl | PrefixDecl)* '''
    def prologue(self, tokens: LookaheadQueue, prologue: Prologue) -> Prologue:
        next_tok: Token = tokens.lookahead()

        if next_tok.term is QueryTerm.PREFIX:
            self.prefix_decl(tokens, prologue)
        elif next_tok.term is QueryTerm.BASE:
            self.base_decl(tokens, prologue)
        
        lookahead: Token = tokens.lookahead()
        if lookahead.term in [QueryTerm.BASE, QueryTerm.PREFIX]:
            return self.prologue(tokens, prologue)
        return prologue

    ''' BaseDecl ::= 'BASE' IRIREF '''
    def base_decl(self, tokens: LookaheadQueue, prologue: Prologue) -> None:
        assert tokens.get_now().term is QueryTerm.BASE
        iri_ref: Token = tokens.get_now()
        if iri_ref.term is not QueryTerm.IRIREF:
            self.throw_error([QueryTerm.IRIREF], iri_ref)
        prologue.set_base(iri_ref.content)

    ''' PrefixDecl ::= 'PREFIX' PNAME_NS IRIREF '''
    def prefix_decl(self, tokens: LookaheadQueue, prologue: Prologue) -> None:
        assert tokens.get_now().term is QueryTerm.PREFIX
        expected: List[QueryTerm] = [QueryTerm.PREFIXED_NAME_PREFIX, QueryTerm.COLON]
        prefix: str = ""

        next_tok: Token = tokens.get_now()
        if next_tok.term is QueryTerm.PREFIXED_NAME_PREFIX:
            prefix = next_tok.content
            del expected[0]
            next_tok = tokens.get_now()
        if next_tok.term is QueryTerm.COLON:
            iriref: Token = tokens.get_now()
            assert iriref.term is QueryTerm.IRIREF
            prologue.set_prefix(prefix, iriref.content)
        else:
            self.throw_error([QueryTerm.COLON], next_tok)

    ''' SelectQuery ::= SelectClause DatasetClause* WhereClause SolutionModifier '''
    def select_query(self, tokens: LookaheadQueue) -> SelectQuery:
        select_query: SelectQuery = SelectQuery()
        select_query.set_select_clause(self.select_clause(tokens))
        if tokens.lookahead().term is QueryTerm.FROM:
            select_query.set_dataset_clause(self.dataset_clause(tokens))
        select_query.set_where_clause(self.where_clause(tokens))
        select_query.set_soln_modifier(self.solution_modifier(tokens))
        return select_query
    
    ''' SelectClause ::= 'SELECT' 'DISTINCT'?
                         (SelectVarList | '*')
    '''
    def select_clause(self, tokens: LookaheadQueue) -> SelectClause:
        select_clause: SelectClause = SelectClause()
        assert tokens.get_now().term is QueryTerm.SELECT
        expected: List[QueryTerm] = [QueryTerm.DISTINCT, QueryTerm.ASTERISK, QueryTerm.VARIABLE, QueryTerm.LPAREN]

        lookahead: Token = tokens.lookahead()
        if lookahead.term is QueryTerm.DISTINCT:
            tokens.get_now()
            lookahead = tokens.lookahead()
            select_clause.make_distinct()
            del expected[0]
        if lookahead.term is QueryTerm.ASTERISK:
            tokens.get_now()
            select_clause.set_select_all()
            return select_clause
        if lookahead.term in [QueryTerm.VARIABLE, QueryTerm.LPAREN]:
            select_clause = self.select_var_list(tokens, select_clause)
            while tokens.lookahead().term in [QueryTerm.LPAREN, QueryTerm.VARIABLE]:
                select_clause = self.select_var_list(tokens, select_clause)
            return select_clause
        else:
            self.throw_error(expected, lookahead)

    ''' SelectVarList ::= (Var | DerivedVar)+ '''
    def select_var_list(self, tokens: LookaheadQueue, select_clause: SelectClause) -> SelectClause:
        if tokens.lookahead().term is QueryTerm.VARIABLE:
            select_clause.add_explicit_var(tokens.get_now().content)
        elif tokens.lookahead().term is QueryTerm.LPAREN:
            var, expr = self.derived_var(tokens)
            select_clause.set_derived_var(var, expr)
        else:
            self.throw_error([QueryTerm.VARIABLE, QueryTerm.LPAREN], tokens.lookahead())
        return select_clause
    
    ''' DerivedVar ::= '(' Expression 'AS' Var ')' '''
    def derived_var(self, tokens: LookaheadQueue) -> Tuple[str, Expression]:
        assert tokens.get_now().term is QueryTerm.LPAREN
        ex: Expression = self.expression(tokens)
        assert tokens.get_now().term is QueryTerm.AS
        var: Token = tokens.get_now()
        assert var.term is QueryTerm.VARIABLE
        assert tokens.get_now().term is QueryTerm.RPAREN
        return (var.content, ex)

    ''' Expression ::= BracketedExpression | BuiltInCall | RDFLiteral | NumericLiteral | BoolLiteral | Var '''
    def expression(self, tokens: LookaheadQueue) -> Expression:
        multi_expr_terms: List[QueryTerm] = [
            QueryTerm.ASTERISK, QueryTerm.EQUALS, QueryTerm.DIV, QueryTerm.ADD,
            QueryTerm.SUB, QueryTerm.LOGICAL_AND, QueryTerm.LT, QueryTerm.GT, QueryTerm.G_OR_EQ,
            QueryTerm.L_OR_EQ, QueryTerm.NOT_EQ, QueryTerm.EXCLAMATION]
        expr: Expression = self.expression_helper(tokens)
        if tokens.lookahead().term in multi_expr_terms:
            expr_op: ExprOp = ExprOp(tokens.get_now().term.value)
            return MultiExprExpr(expr, self.expression(tokens), expr_op)
        return expr
    
    def expression_helper(self, tokens: LookaheadQueue) -> Expression:
        next_tok: Token = tokens.get_now()
        if next_tok.term is QueryTerm.LPAREN:
            ex: Expression = IdentityFunction(self.expression(tokens))
            assert tokens.get_now().term is QueryTerm.RPAREN
            return ex
        elif next_tok.term is QueryTerm.VARIABLE:
            return TerminalExpr(next_tok.content)
        elif next_tok.term.value in QueryTerm.built_in_calls():
            return self.built_in_call(next_tok.term, tokens)
        elif next_tok.term is QueryTerm.EXCLAMATION:
            return NegationExpr(self.expression())
        elif next_tok.term is QueryTerm.STRING_LITERAL:
            return TerminalExpr(next_tok.content)
        elif next_tok.term is QueryTerm.U_NUMBER_LITERAL:
            return TerminalExpr(next_tok.content)
        elif next_tok.term in [QueryTerm.TRUE, QueryTerm.FALSE]:
            return TerminalExpr(next_tok.content)
        else:
            built_in_qts: List[QueryTerm] = [QueryTerm(qt_str) for qt_str in QueryTerm.built_in_calls()]
            self.throw_error([QueryTerm.LPAREN, QueryTerm.VARIABLE] + built_in_qts, next_tok)

    '''BuiltInCall ::= 'NOT' 'EXISTS' GroupGraphPattern
                       | 'EXISTS' GroupGraph Pattern
                       | 'CONCAT' '(' ExpressionList ')'
                       | 'REGEX' '(' Expression ',' Expression (',' Expression)? ')'
                       | 'SUBSTR' '(' Expression ',' Expression (',' Expression)? ')'
                       | 'REPLACE' '(' Expression ',' Expression ',' Expression (',' Expression)? ')'
                       | Aggregate
                       | any_other_built_in '(' Expression ')' '''
    def built_in_call(self, built_in_term: QueryTerm, tokens: LookaheadQueue) -> Expression:
        if built_in_term is QueryTerm.NOT:
            assert tokens.get_now().term is QueryTerm.EXISTS
            return ExistenceExpr(self.group_graph_pattern(tokens, None), True)
        elif built_in_term is QueryTerm.EXISTS:
            return ExistenceExpr(self.group_graph_pattern(tokens, None), False)
        
        aggregates: List[QueryTerm] = [
            QueryTerm.COUNT, QueryTerm.SUM, QueryTerm.MIN, QueryTerm.MAX, QueryTerm.AVG,
            QueryTerm.SAMPLE, QueryTerm.GROUP_CONCAT]
        if built_in_term in aggregates:
            return self.aggregate(built_in_term, tokens)
        
        args: List[Expression] = None
        assert tokens.get_now().term is QueryTerm.LPAREN
        if built_in_term is QueryTerm.SUBSTR or built_in_term is QueryTerm.REGEX:
            args = self.expression_list(tokens, min=2, max=3)
        elif built_in_term is QueryTerm.REPLACE:
            args = self.expression_list(tokens, min=3, max=4)
        elif built_in_term is QueryTerm.CONCAT:
            args = self.expression_list(tokens, min=1, max=None)
        else:
            args = [self.expression(tokens)]
        assert tokens.get_now().term is QueryTerm.RPAREN
        return Function(built_in_term.value, args)
    
    def aggregate(self, agg_term: QueryTerm, tokens: LookaheadQueue) -> Expression:
        assert tokens.get_now().term is QueryTerm.LPAREN
        is_distinct: bool = False
        if tokens.lookahead().term is QueryTerm.DISTINCT:
            is_distinct = True
            tokens.get_now()
        
        arg: Expression = None
        if tokens.lookahead().term is QueryTerm.ASTERISK:
            if agg_term is QueryTerm.COUNT:
                tokens.get_now()
                arg = TerminalExpr("*")
            else:
                raise ValueError(f"Asterick followed {agg_term.value}. "
                                 f"Its only allowed for aggregate function 'count()'")
        if arg is None:
            arg = self.expression(tokens)

        if agg_term is QueryTerm.GROUP_CONCAT:
            separator: str = None
            if tokens.lookahead().term is QueryTerm.SEMI_COLON:
                tokens.get_now()
                assert tokens.get_now().term is QueryTerm.SEPARATOR
                assert tokens.get_now().term is QueryTerm.EQUALS
                str_lit: Token = tokens.get_now()
                assert str_lit.term is QueryTerm.STRING_LITERAL
                separator = str_lit.content
            assert tokens.get_now().term is QueryTerm.RPAREN
            return GroupConcatFunction(arg, is_distinct, separator)
        assert tokens.get_now().term is QueryTerm.RPAREN
        return AggregateFunction(agg_term.value, arg, is_distinct)

    '''ExpressionList ::= Expression (',' Expression)* '''
    def expression_list(self, tokens: LookaheadQueue, min: int, max: int) -> List[Expression]:
        if max is not None and min > max:
            raise ValueError("Min must be <= max")
        args: List[Expression] = [self.expression(tokens)]
        while tokens.lookahead().term is QueryTerm.COMMA:
            tokens.get_now()
            args.append(self.expression(tokens))

        if max is not None and min > len(args) > max:
            raise ValueError(f"Expected arg count in range [{min},{max}]. Found {len(args)} args.")
        elif min > len(args):
            raise ValueError(f"Expected arg count in range [{min},INF]. Found {len(args)} args.")
        return args
    
    '''DatasetClause ::= 'FROM' (DefaultGraphClause | NamedGraphClause) '''
    def dataset_clause(self, tokens: LookaheadQueue) -> DatasetClause:
        is_named: bool = False
        assert tokens.get_now().term is QueryTerm.FROM
        lookahead: Token = tokens.lookahead()
        if lookahead.term is QueryTerm.NAMED:
            is_named = True
            tokens.get_now()
        iri: str = self.iri(tokens)
        return DatasetClause(iri, is_named)
        
    '''Iri ::= IRIREF | PN_PREFIX? ':' | PN_PREFIX? ':' PN_LOCAL '''
    def iri(self, tokens: LookaheadQueue) -> str:
        expected: List[QueryTerm] = [QueryTerm.IRIREF, QueryTerm.PREFIXED_NAME_PREFIX, QueryTerm.COLON]
        lookahead: Token = tokens.lookahead()
        if lookahead.term is QueryTerm.IRIREF:
            return tokens.get_now().content
        prefix, local_name = "", ""
        if lookahead.term is QueryTerm.PREFIXED_NAME_PREFIX:
            prefix = tokens.get_now().content
            expected = [QueryTerm.COLON]
        next_tok: Token = tokens.get_now()
        if next_tok.term is not QueryTerm.COLON:
            self.throw_error(expected, next_tok)
        if tokens.lookahead().term is QueryTerm.PREFIXED_NAME_LOCAL:
            local_name: str = tokens.get_now().content
        return f"{prefix}:{local_name}"
    
    '''WhereClause ::= 'WHERE'? GroupGraphPattern '''
    def where_clause(self, tokens: LookaheadQueue) -> WhereClause:
        uses_keyword: bool = False
        lookahead: Token = tokens.lookahead()
        if lookahead.term is QueryTerm.WHERE:
            uses_keyword = True
            tokens.get_now()
        return WhereClause(self.group_graph_pattern(tokens, None), uses_keyword)
    
    ''' GroupGraphPattern ::= '{' ( SubSelect | GroupGraphPatternSub ) '}' '''
    def group_graph_pattern(self, tokens: LookaheadQueue, ggp_sub: GroupGraphPatternSub) -> GroupGraphPattern:
        assert tokens.get_now().term is QueryTerm.LBRACKET
        root_ggp: GroupGraphPattern = None

        if tokens.lookahead().term is QueryTerm.SELECT:
            if ggp_sub is None:
                root_ggp = self.sub_select(tokens)
            else:
                ggp_sub.add_pattern(self.sub_select(tokens))
        else:
            if ggp_sub is None:
                root_ggp = GroupGraphPatternSub()
                self.group_graph_pattern_sub(tokens, root_ggp)
            else:
                self.group_graph_pattern_sub(tokens, ggp_sub)
        assert tokens.get_now().term is QueryTerm.RBRACKET
        if root_ggp:
            return root_ggp
        return ggp_sub
    
    '''GroupGraphPatternSub ::= TriplesBlock? (GraphPatternNotTriples '.'? TriplesBlock?)* '''
    def group_graph_pattern_sub(self, tokens: LookaheadQueue, ggp_sub: GroupGraphPatternSub) -> None:
        triples_block_terms: List[QueryTerm] = [
            QueryTerm.VARIABLE, QueryTerm.PREFIXED_NAME_PREFIX, QueryTerm.IRIREF,
            QueryTerm.U_NUMBER_LITERAL, QueryTerm.STRING_LITERAL, QueryTerm.TRUE, QueryTerm.FALSE]
        not_triples_terms: List[QueryTerm] = [
            QueryTerm.OPTIONAL, QueryTerm.GRAPH, QueryTerm.SELECT, QueryTerm.MINUS,
            QueryTerm.FILTER, QueryTerm.BIND, QueryTerm.SERVICE, QueryTerm.LBRACKET]
        
        if tokens.lookahead().term in triples_block_terms:
            ggp_sub.add_triples_block(self.triples_block(tokens, TriplesBlock()))
        while tokens.lookahead().term in not_triples_terms:
            if tokens.lookahead().term in [QueryTerm.FILTER, QueryTerm.BIND]:
                ggp_sub.add_modifier(self.pattern_modifier(tokens))
            else:
                ggp_sub.add_pattern(self.graph_pattern_not_triples(tokens))
            if tokens.lookahead().term is QueryTerm.PERIOD:
                tokens.get_now()
            if tokens.lookahead().term in triples_block_terms:
                ggp_sub.add_triples_block(self.triples_block(tokens, TriplesBlock()))

    '''PatternModifier ::=  Filter | Bind '''
    def pattern_modifier(self, tokens: LookaheadQueue) -> PatternModifier:
        lookahead: Token = tokens.lookahead()
        modifier: PatternModifier = None
        if lookahead.term is QueryTerm.FILTER:
            tokens.get_now()
            modifier = Filter(self.constraint(tokens))
        elif lookahead.term is QueryTerm.BIND:
            tokens.get_now()
            var, expr = self.derived_var(tokens)
            modifier = Bind(expr, var)
        else:
            self.throw_error([QueryTerm.FILTER, QueryTerm.BIND], lookahead)
        return modifier
    
    '''GraphPatternNotTriples ::= GroupOrUnionGraphPattern | OptionalGraphPattern | MinusGraphPattern
                                  | GraphGraphPattern | ServiceGraphPattern '''
    def graph_pattern_not_triples(self, tokens: LookaheadQueue) -> GroupGraphPattern:
        lookahead: Token = tokens.lookahead()
        if lookahead.term is QueryTerm.OPTIONAL:
            tokens.get_now()
            return self.group_graph_pattern(tokens, OptionalGraphPattern())
        elif lookahead.term is QueryTerm.MINUS:
            tokens.get_now()
            return self.group_graph_pattern(tokens, MinusGraphPattern())
        elif lookahead.term is QueryTerm.GRAPH:
            tokens.get_now()
            if tokens.lookahead().term is QueryTerm.VARIABLE:
                return self.group_graph_pattern(tokens, GraphGraphPattern(tokens.get_now().content))
            else:
                return self.group_graph_pattern(tokens, GraphGraphPattern(self.iri(tokens)))
        elif lookahead.term is QueryTerm.SERVICE:
            tokens.get_now()
            is_silent: bool = False
            if tokens.lookahead().term is QueryTerm.SILENT:
                is_silent = True
                tokens.get_now()
            if tokens.lookahead().term is QueryTerm.VARIABLE:
                return self.group_graph_pattern(
                    tokens, ServiceGraphPattern(is_silent, tokens.get_now().content))
            else:
                return self.group_graph_pattern(
                    tokens, ServiceGraphPattern(is_silent, self.iri(tokens)))
        elif lookahead.term is QueryTerm.LBRACKET:
            unioned_ggp: List[GroupGraphPattern] = [self.group_graph_pattern(tokens, None)]
            while tokens.lookahead().term is QueryTerm.UNION:
                tokens.get_now()
                unioned_ggp.append(self.group_graph_pattern(tokens, None))
            if len(unioned_ggp) > 1:
                return UnionGraphPattern(patterns=unioned_ggp)
            else:
                return unioned_ggp[0]
        self.throw_error([QueryTerm.LBRACKET, QueryTerm.SERVICE, QueryTerm.GRAPH, QueryTerm.MINUS,
                          QueryTerm.OPTIONAL], lookahead)
            
    '''Constraint ::= '(' Expression ')' | BuiltInCall '''
    def constraint(self, tokens: LookaheadQueue) -> Expression:
        if tokens.lookahead().term is QueryTerm.LPAREN:
            tokens.get_now()
            ex: Expression = IdentityFunction(self.expression(tokens))
            assert tokens.get_now().term is QueryTerm.RPAREN
            return ex
        elif tokens.lookahead().term.value in QueryTerm.built_in_calls():
            return self.built_in_call(tokens.get_now().term, tokens)
        else:
            built_in_qts: List[QueryTerm] = [QueryTerm(qt_str) for qt_str in QueryTerm.built_in_calls()]
            self.throw_error([QueryTerm.LPAREN] + built_in_qts, tokens.lookahead())
    
    '''TriplesBlock ::= TriplesSameSubjectPath ('.' TriplesBlock?)? '''
    def triples_block(self, tokens: LookaheadQueue, triples_block: TriplesBlock) -> TriplesBlock:
        triples_block.add_triples_same_subj(self.triples_same_subj(tokens))
        if tokens.lookahead().term is QueryTerm.PERIOD:
            tokens.get_now()
            if tokens.lookahead().term in [QueryTerm.VARIABLE, QueryTerm.IRIREF,
                                           QueryTerm.STRING_LITERAL, QueryTerm.U_NUMBER_LITERAL,
                                           QueryTerm.TRUE, QueryTerm.FALSE, QueryTerm.PREFIXED_NAME_PREFIX]:
                self.triples_block(tokens, triples_block)
        return triples_block
    
    '''TriplesSameSubj ::= VarOrTerm PropertyListPathNotEmpty '''
    def triples_same_subj(self, tokens: LookaheadQueue) -> TriplesSameSubj:
        triples_same_subj: TriplesSameSubj = TriplesSameSubj(self.var_or_term(tokens))
        triples_same_subj.add_po_dict(self.property_list_path_not_empty(tokens))
        return triples_same_subj
    
    '''VarOrTerm ::= Var | iri | StringLiteral | NumericLiteral | BooleanLiteral '''
    def var_or_term(self, tokens: LookaheadQueue) -> str:
        lookahead: Token = tokens.lookahead()
        if lookahead.term is QueryTerm.VARIABLE:
            tokens.get_now()
            return lookahead.content
        elif lookahead.term is QueryTerm.STRING_LITERAL:
            tokens.get_now()
            return lookahead.content
        elif lookahead.term is QueryTerm.U_NUMBER_LITERAL:
            tokens.get_now()
            return lookahead.content
        elif lookahead.term is QueryTerm.TRUE:
            tokens.get_now()
            return "true"
        elif lookahead.term is QueryTerm.FALSE:
            tokens.get_now()
            return "false"
        elif lookahead.term in [QueryTerm.IRIREF, QueryTerm.PREFIXED_NAME_PREFIX, QueryTerm.COLON]:
            return self.iri(tokens)
        else:
            self.throw_error([QueryTerm.PREFIXED_NAME_PREFIX, QueryTerm.TRUE, QueryTerm.FALSE,
                              QueryTerm.VARIABLE, QueryTerm.IRIREF, QueryTerm.STRING_LITERAL,
                              QueryTerm.U_NUMBER_LITERAL], lookahead)

    '''PropertyListPathNotEmpty ::= ( VerbPath | Var ) ObjectList
                                    ( ';' ( ( VerbPath | Var ) ObjectList )? )*'''
    def property_list_path_not_empty(self, tokens: LookaheadQueue) -> Dict[Verb, Set[str]]:
        pred_to_objs: Dict[Verb, Set[str]] = defaultdict(set)
        verb, objs = self.property_list_path_not_empty_helper(tokens)
        pred_to_objs[verb] = objs

        verb_starters: List[QueryTerm] = [
            QueryTerm.VARIABLE, QueryTerm.LPAREN, QueryTerm.A, QueryTerm.IRIREF,
            QueryTerm.PREFIXED_NAME_PREFIX, QueryTerm.COLON]
        while tokens.lookahead().term is QueryTerm.SEMI_COLON:
            tokens.get_now()
            # Verb/Obj_list logic:
            if tokens.lookahead().term in verb_starters:
                verb, objs = self.property_list_path_not_empty_helper(tokens)
                pred_to_objs[verb] = pred_to_objs[verb].union(objs)
        return pred_to_objs
    
    def property_list_path_not_empty_helper(self, tokens: LookaheadQueue) -> Tuple[Verb, Set[str]]:
        verb_path_starters: List[QueryTerm] = [
            QueryTerm.LPAREN, QueryTerm.A, QueryTerm.IRIREF, QueryTerm.PREFIXED_NAME_PREFIX, QueryTerm.COLON]
        verb: Verb = None
        if tokens.lookahead().term is QueryTerm.VARIABLE:
            verb = VarVerb(tokens.get_now().content)
        elif tokens.lookahead().term in verb_path_starters:
            verb = self.verb_path(tokens)
        else:
            self.throw_error([QueryTerm.VARIABLE] + verb_path_starters, tokens.lookahead())
        objs = self.object_list(tokens)
        return (verb, objs)
        
    '''VerbPath ::= iri | 'a' | '(' VerbPath ')' '''
    def verb_path(self, tokens: LookaheadQueue) -> VerbPath:
        iri_terms: List[QueryTerm] = [QueryTerm.IRIREF, QueryTerm.PREFIXED_NAME_PREFIX, QueryTerm.COLON]
        vp: VerbPath = None

        is_inverse: bool = False
        if tokens.lookahead().term is QueryTerm.CARAT:
            is_inverse = True
            tokens.get_now()

        lookahead: Token = tokens.lookahead()
        if lookahead.term is QueryTerm.A:
            tokens.get_now()
            vp = TerminalVerbPath("a")
        elif lookahead.term in iri_terms:
            vp = TerminalVerbPath(self.iri(tokens))
        elif lookahead.term is QueryTerm.LPAREN:
            tokens.get_now()
            vp = IdentityVerbPath(self.verb_path(tokens))
            assert tokens.get_now().term is QueryTerm.RPAREN
        else:
            self.throw_error([QueryTerm.A, QueryTerm.LPAREN] + iri_terms, lookahead)
        
        if tokens.lookahead().term in [QueryTerm.QUESTION, QueryTerm.ADD, QueryTerm.ASTERISK]:
            vp = ElementVerbPath(vp, PathMod(tokens.get_now().term.value))
        if is_inverse:
            vp = InverseVerbPath(vp)
        if tokens.lookahead().term in [QueryTerm.PIPE, QueryTerm.DIV]:
            path_op: PathOp = PathOp(tokens.get_now().term.value)
            vp = MultiPathVerbPath(vp, self.verb_path(tokens), path_op)
        return vp
        
    '''ObjectListPath ::= VarOrTerm ( ',' VarOrTerm )* '''
    def object_list(self, tokens: LookaheadQueue) -> Set[str]:
        objs: Set[str] = set([self.var_or_term(tokens)])
        while tokens.lookahead().term is QueryTerm.COMMA:
            tokens.get_now()
            objs.add(self.var_or_term(tokens))
        return objs

    '''SubSelect ::= SelectClause WhereClause SolutionModifier '''
    def sub_select(self, tokens: LookaheadQueue) -> SubSelect:
        sub_select: SubSelect = SubSelect()
        sub_select.set_select_clause(self.select_clause(tokens))
        sub_select.set_where_clause(self.where_clause(tokens))
        sub_select.set_soln_modifier(self.solution_modifier(tokens))
        return sub_select
    
    '''SolutionModifier ::= GroupClause? HavingClause? OrderClause? LimitOffsetClauses? '''
    def solution_modifier(self, tokens: LookaheadQueue) -> SolnModifier:
        modifier: SolnModifier = SolnModifier()
        if tokens.lookahead().term is QueryTerm.GROUP:
            tokens.get_now()
            assert tokens.get_now().term is QueryTerm.BY
            modifier.set_group_clause(self.group_condition(tokens, GroupClause()))
        if tokens.lookahead().term is QueryTerm.HAVING:
            tokens.get_now()
            modifier.set_having_clause(self.having_condition(tokens, HavingClause()))
        if tokens.lookahead().term is QueryTerm.ORDER:
            tokens.get_now()
            assert tokens.get_now().term is QueryTerm.BY
            modifier.set_order_clause(self.order_condition(tokens, OrderClause()))
        if tokens.lookahead().term in [QueryTerm.LIMIT, QueryTerm.OFFSET]:
            modifier.set_limit_offset_clause(self.limit_offset_condition(tokens))
        return modifier

    def group_condition(self, tokens: LookaheadQueue, group_clause: GroupClause) -> GroupClause:
        lookahead: Token = tokens.lookahead()
        if lookahead.term is QueryTerm.VARIABLE:
            group_clause.add_var(tokens.get_now().content)
            self.group_condition(tokens, group_clause)
        elif lookahead.term is QueryTerm.LPAREN:
            tokens.get_now()
            expr = self.expression(tokens)
            if tokens.lookahead().term is QueryTerm.AS:
                tokens.get_now()
                var: Token = tokens.get_now()
                assert var.term is QueryTerm.VARIABLE
                group_clause.add_derived_var(var.content, expr)
            else:
                group_clause.add_expr(IdentityFunction(expr))
            assert tokens.get_now().term is QueryTerm.RPAREN
            self.group_condition(tokens, group_clause)
        elif lookahead.term.value in QueryTerm.built_in_calls():
            built_in_term: QueryTerm = tokens.get_now().term
            group_clause.add_expr(self.built_in_call(built_in_term, tokens))
            self.group_condition(tokens, group_clause)
        elif group_clause.is_empty():
            built_in_qts: List[QueryTerm] = [QueryTerm(qt_str) for qt_str in QueryTerm.built_in_calls()]
            self.throw_error([QueryTerm.VARIABLE, QueryTerm.LPAREN] + built_in_qts, lookahead)
        return group_clause
    
    def having_condition(self, tokens: LookaheadQueue, having_clause: HavingClause) -> HavingClause:
        having_clause.add_expr(self.constraint(tokens))
        built_in_qts: List[QueryTerm] = [QueryTerm(qt_str) for qt_str in QueryTerm.built_in_calls()]
        while tokens.lookahead().term in [QueryTerm.LPAREN] + built_in_qts:
            having_clause.add_expr(self.constraint(tokens))
        return having_clause

    def order_condition(self, tokens: LookaheadQueue, order_clause: OrderClause) -> OrderClause:
        lookahead: Token = tokens.lookahead()
        if lookahead.term is QueryTerm.VARIABLE:
            order_clause.add_expr(TerminalExpr(tokens.get_now().content))
            self.order_condition(tokens, order_clause)
        elif lookahead.term is QueryTerm.ASC:
            tokens.get_now()
            assert tokens.get_now().term is QueryTerm.LPAREN
            order_clause.add_expr(Function("ASC", [self.expression(tokens)]))
            assert tokens.get_now().term is QueryTerm.RPAREN
            self.order_condition(tokens, order_clause)
        elif lookahead.term is QueryTerm.DESC:
            tokens.get_now()
            assert tokens.get_now().term is QueryTerm.LPAREN
            order_clause.add_expr(Function("DESC", [self.expression(tokens)]))
            assert tokens.get_now().term is QueryTerm.RPAREN
            self.order_condition(tokens, order_clause)
        elif lookahead.term.value in [QueryTerm.LPAREN.value] + QueryTerm.built_in_calls():
            order_clause.add_expr(self.constraint(tokens))
            self.order_condition(tokens, order_clause)
        elif order_clause.is_empty():
            built_in_qts: List[QueryTerm] = [QueryTerm(qt_str) for qt_str in QueryTerm.built_in_calls()]
            self.throw_error(built_in_qts + [QueryTerm.LPAREN, QueryTerm.VARIABLE, QueryTerm.ASC, QueryTerm.DESC],
                             lookahead)
        return order_clause

    def limit_offset_condition(self, tokens: LookaheadQueue) -> LimitOffsetClause:
        next_tok: Token = tokens.get_now()
        if next_tok.term is QueryTerm.LIMIT:
            limit_int: Token = tokens.get_now()
            assert limit_int.term is QueryTerm.U_NUMBER_LITERAL
            if tokens.lookahead().term is QueryTerm.OFFSET:
                tokens.get_now()
                offset_int: Token = tokens.get_now()
                assert offset_int.term is QueryTerm.U_NUMBER_LITERAL
                return LimitOffsetClause(int(limit_int.content), int(offset_int.content), True)
            else:
                return LimitOffsetClause(int(limit_int.content), None, True)
        elif next_tok.term is QueryTerm.OFFSET:
            offset_int: Token = tokens.get_now()
            assert offset_int.term is QueryTerm.U_NUMBER_LITERAL
            if tokens.lookahead().term is QueryTerm.LIMIT:
                tokens.get_now()
                limit_int: Token = tokens.get_now()
                assert limit_int.term is QueryTerm.U_NUMBER_LITERAL
                return LimitOffsetClause(int(limit_int.content), int(offset_int.content), False)
            else:
                return LimitOffsetClause(None, int(offset_int.content), False)
    
    def throw_error(self, expected_terms: List[QueryTerm], actual_tok: Token) -> None:
        raise ValueError(f"Expected {', '.join([term.name for term in expected_terms])} "
                         f"but got {actual_tok.term.value}")
