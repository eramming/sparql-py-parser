from .tokens import QueryTerm, Token
from .Query import Query
from .SelectQuery import SelectQuery
from .SelectClause import SelectClause
from .Expressions import Expression, IdentityFunction, MultiExprExpr, \
    Function, AggregateFunction, NegationExpr, ExistenceExpr, TerminalExpr
from .ExprOp import ExprOp
from .GroupGraphPattern import GroupGraphPattern
from .GroupGraphPatternSub import GroupGraphPatternSub
from .GraphPatternNotTriples import OptionalGraphPattern, GraphGraphPattern, \
    MinusGraphPattern, UnionGraphPattern, Filter, Bind, ServiceGraphPattern
from .SolnModifier import SolnModifier
from .SubSelect import SubSelect
from .DatasetClause import DatasetClause
from .WhereClause import WhereClause
from .Prologue import Prologue
from .LookaheadQueue import LookaheadQueue
from typing import List

class QueryParser:

    PROLOGUE_STARTERS: List[QueryTerm] = [
        QueryTerm.BASE, QueryTerm.PREFIX
    ]

    def __init__(self) -> None:
        pass
    
    def parse(self, tokens: LookaheadQueue) -> Query:
        return self.query(tokens)

    ''' Query ::= Prologue SelectQuery '''
    def query(self, tokens: LookaheadQueue) -> Query:
        lookahead: Token = tokens.lookahead()
        prologue: Prologue = None
        select_query: SelectQuery = None
        if lookahead.term in QueryParser.PROLOGUE_STARTERS:
            prologue = self.prologue(tokens, Prologue())
        if tokens.lookahead().term is QueryTerm.SELECT:
            select_query: SelectQuery = self.select_query(tokens)
        elif prologue:
            self.throw_error([QueryTerm.SELECT.value], lookahead)
        else:
            self.throw_error(QueryParser.PROLOGUE_STARTERS + [QueryTerm.SELECT], lookahead)
        
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
            expected = []
            next_tok = tokens.get_now()
            if next_tok.term is not QueryTerm.IRIREF:
                expected = [QueryTerm.IRIREF]
            else:
                prologue.set_prefix(prefix, next_tok.content)
        if expected:
            self.throw_error(expected, next_tok)

    ''' SelectQuery ::= SelectClause DatasetClause* WhereClause '''
    def select_query(self, tokens: LookaheadQueue) -> SelectQuery:
        select_query: SelectQuery = SelectQuery()
        select_query.select_clause = self.select_clause(tokens, select_query.select_clause)
        if tokens.lookahead().term is QueryTerm.FROM:
            select_query.dataset_clause = self.dataset_clause(tokens, select_query.dataset_clause)
        select_query.where_clause = self.where_clause(tokens)
        return select_query
    
    ''' SelectClause ::= 'SELECT' 'DISTINCT'?
                         (SelectVarList | '*')
    '''
    def select_clause(self, tokens: LookaheadQueue, select_clause: SelectClause) -> SelectClause:
        assert tokens.get_now().term is QueryTerm.SELECT
        expected: List[QueryTerm] = [QueryTerm.DISTINCT, QueryTerm.ASTERISK, QueryTerm.VARIABLE, QueryTerm.LPAREN]

        next_tok: Token = tokens.get_now()
        if next_tok.term is QueryTerm.DISTINCT:
            select_clause.make_distinct()
            del expected[0]
            next_tok = tokens.get_now()
        if next_tok.term is QueryTerm.ASTERISK:
            select_clause.set_select_all()
            return select_clause
        if next_tok.term in [QueryTerm.VARIABLE, QueryTerm.LPAREN]:
            select_clause = self.select_var_list(tokens, select_clause)
            while tokens.lookahead().term in [QueryTerm.LPAREN, QueryTerm.VARIABLE]:
                select_clause = self.select_var_list(tokens, select_clause)
            return select_clause
        else:
            self.throw_error(expected, next_tok)

    ''' SelectVarList ::= (Var | '(' Expression 'AS' Var ')')+ '''
    def select_var_list(self, tokens: LookaheadQueue, select_clause: SelectClause) -> SelectClause:
        next_tok: Token = tokens.get_now()
        if next_tok.term is QueryTerm.VARIABLE:
            select_clause.add_explicit_var(next_tok.content)    
        elif next_tok.term is QueryTerm.LPAREN:
            ex: Expression = self.expression(tokens)
            assert tokens.get_now().term is QueryTerm.AS
            var: Token = tokens.get_now()
            assert var.term is QueryTerm.VARIABLE
            select_clause.set_derived_var(var.content, ex)
            assert tokens.get_now().term is QueryTerm.RPAREN
        else:
            self.throw_error([QueryTerm.VARIABLE, QueryTerm.LPAREN], next_tok)
        return select_clause

    ''' Expression ::= BracketedExpression | BuiltInCall | RDFLiteral | NumericLiteral | BoolLiteral | Var '''
    def expression(self, tokens: LookaheadQueue) -> Expression:
        next_tok: Token = tokens.get_now()
        if next_tok.term is QueryTerm.LPAREN:
            ex: Expression = IdentityFunction(self.expression(tokens))
            assert tokens.get_now().term is QueryTerm.RPAREN
            return ex
        elif next_tok.term is QueryTerm.VARIABLE:
            return TerminalExpr(f"?{next_tok.content}")
        elif next_tok.term.value in QueryTerm.built_in_calls():
            return self.built_in_call(next_tok.term, tokens)
        elif next_tok.term is QueryTerm.EXCLAMATION:
            return NegationExpr(self.expression())
        elif next_tok.term is QueryTerm.STRING_LITERAL:
            return TerminalExpr(f"'{next_tok.content}'")
        elif next_tok.term is QueryTerm.NUMBER_LITERAL:
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
                       | any_other_built_in '(' Expression ')' '''
    def built_in_call(self, built_in_term: QueryTerm, tokens: LookaheadQueue) -> Expression:
        if built_in_term is QueryTerm.NOT:
            assert tokens.get_now().term is QueryTerm.EXISTS
            return ExistenceExpr(self.group_graph_pattern(), True)
        elif built_in_term is QueryTerm.EXISTS:
            return ExistenceExpr(self.group_graph_pattern(), False)
        
        args: List[Expression] = None
        assert tokens.get_now().term is QueryTerm.LPAREN
        if built_in_term is QueryTerm.SUBSTR or built_in_term is QueryTerm.REGEX:
            args = self.expression_list(tokens, min=2, max=3)
        elif built_in_term is QueryTerm.REPLACE:
            args = self.expression_list(tokens, min=3, max=4)
        elif built_in_term is QueryTerm.CONCAT:
            args = self.expression_list(tokens, min=1, max=None)
        else:
            args = self.expression(tokens)
        assert tokens.get_now().term is QueryTerm.RPAREN
        return Function(built_in_term.value, args)

    '''ExpressionList ::= Expression (',' Expression)* '''
    def expression_list(self, tokens: LookaheadQueue, min: int, max: int) -> List[Expression]:
        if max is not None and min > max:
            raise ValueError("Min must be <= max")
        args: List[Expression] = []
        while tokens.lookahead().term is QueryTerm.COMMA:
            tokens.get_now()
            args.append(self.expression(tokens))

        if max is not None and min > len(args) > max:
            raise ValueError(f"Expected arg count in range [{min},{max}]. Found {len(args)} args.")
        elif min > len(args):
            raise ValueError(f"Expected arg count in range [{min},INF]. Found {len(args)} args.")
        return args
    
    '''DatasetClause ::= 'FROM' (DefaultGraphClause | NamedGraphClause) '''
    def dataset_clause(self, tokens: LookaheadQueue, dataset_clause: DatasetClause) -> DatasetClause:
        raise NotImplementedError()
    
    '''WhereClause ::= 'WHERE'? GroupGraphPattern '''
    def where_clause(self, tokens: LookaheadQueue) -> WhereClause:
        next_tok: Token = tokens.lookahead()
        if next_tok.term is QueryTerm.WHERE:
            tokens.get_now()
        ggp: GroupGraphPattern = self.group_graph_pattern(tokens)
        return WhereClause(ggp)
    
    '''old way:
    GroupGraphPattern ::= '{' GroupGraphPattern* (SubSelect | GroupGraphPatternSub)? '}'
    new way:
    GroupGraphPattern ::= '{' ( SubSelect | GroupGraphPatternSub ) '}' '''
    def group_graph_pattern(self, tokens: LookaheadQueue, encloser: GroupGraphPattern.Enclosers) -> GroupGraphPattern:
        ggp_sub_terms: List[QueryTerm] = [QueryTerm.VARIABLE, QueryTerm.IRIREF, QueryTerm.PREFIXED_NAME_PREFIX,
                                          QueryTerm.GRAPH, QueryTerm.OPTIONAL]
        expected: List[QueryTerm] = ggp_sub_terms + [QueryTerm.LBRACKET, QueryTerm.SELECT, QueryTerm.RBRACKET]
        ggp: GroupGraphPattern = GroupGraphPattern(encloser)
        assert tokens.get_now().term is QueryTerm.LBRACKET
        while tokens.lookahead().term is QueryTerm.LBRACKET:
            ggp.add_ggp(self.group_graph_pattern(tokens, GroupGraphPattern.Enclosers.NO_ENCLOSER))

        if tokens.lookahead().term is QueryTerm.SELECT:
            ggp.set_sub_select(self.subselect(tokens))
            expected = [QueryTerm.RBRACKET]
        elif tokens.lookahead().term in ggp_sub_terms:
            ggp.set_ggp_sub(self.group_graph_pattern_sub(tokens, GroupGraphPatternSub()))
            expected = ggp_sub_terms + [QueryTerm.RBRACKET]
        
        if tokens.lookahead().term is not QueryTerm.RBRACKET:
            self.throw_error(expected, tokens.lookahead())
        return ggp
    
    '''GroupGraphPatternSub ::= TriplesBlock? (('OPTIONAL' | 'GRAPH') '.'? TriplesBlock?)* '''
    '''GroupGraphPatternSub ::= TriplesBlock? (GraphPatternNotTriples '.'? TriplesBlock?)* '''
    def group_graph_pattern_sub(self, tokens: LookaheadQueue, ggp_sub: GroupGraphPatternSub) -> GroupGraphPatternSub:
        next_tok: Token = tokens.lookahead()
        
        if next_tok.term in [QueryTerm.VARIABLE, QueryTerm.PREFIXED_NAME_PREFIX, QueryTerm.IRIREF,
                             QueryTerm.NUMBER_LITERAL, QueryTerm.STRING_LITERAL, QueryTerm.TRUE,
                             QueryTerm.FALSE]:
            ggp_sub.add_triple_block(self.triples_block(tokens))
            return self.group_graph_pattern_sub(tokens, ggp_sub)
        elif next_tok.term in [QueryTerm.OPTIONAL, QueryTerm.GRAPH, QueryTerm.SELECT, QueryTerm.MINUS,
                               QueryTerm.UNION, QueryTerm.FILTER, QueryTerm.BIND, QueryTerm.SERVICE]:
            tokens.get_now()
            ggp_sub.add_other_pattern(self.group_graph_pattern(tokens, GroupGraphPattern.Enclosers.OPTIONAL))
            return self.group_graph_pattern_sub(tokens, ggp_sub)
        elif next_tok.term is QueryTerm.GRAPH:
            tokens.get_now()
            var_or_iri: Token = tokens.get_now()
            assert
        else:
            return ggp_sub

    '''GraphPatternNotTriples ::= GroupOrUnionGraphPattern | OptionalGraphPattern | MinusGraphPattern
                                  | GraphGraphPattern | ServiceGraphPattern | Filter | Bind '''
    def graph_pattern_not_triples(self, tokens: LookaheadQueue, ggp_sub: GroupGraphPatternSub) -> GroupGraphPatternSub:
        raise NotImplementedError()
    
    '''SubselectClause ::= tbd '''
    # TODO: Return type likely wrong
    def subselect(self, tokens: LookaheadQueue) -> SubSelect:
        raise NotImplementedError()
    
    def throw_error(self, expected_terms: List[QueryTerm], actual_tok: Token) -> None:
        raise ValueError(f"Expected {', '.join([term.name for term in expected_terms])} "
                         f"but got {actual_tok.term.value}")
