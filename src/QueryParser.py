from .tokens import QueryTerm, Token
from .Query import Query
from .SelectQuery import SelectQuery
from .SelectClause import SelectClause
from .Expressions import Expression
from .GroupGraphPattern import GroupGraphPattern
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

    ''' Query ::= Prologue
              ::= SelectQuery '''
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

    ''' SelectQuery ::= SelectClause
                    ::= DatasetClause*
                    ::= WhereClause
    '''
    def select_query(self, tokens: LookaheadQueue) -> SelectQuery:
        select_query: SelectQuery = SelectQuery()
        select_query.select_clause = self.select_clause(tokens, select_query.select_clause)
        if tokens.lookahead().term is QueryTerm.FROM:
            select_query.dataset_clause = self.dataset_clause(tokens, select_query.dataset_clause)
        select_query.where_clause = self.where_clause(tokens, select_query.where_clause)
        return select_query
    
    ''' SelectClause ::= 'SELECT' 'DISTINCT'?
                     ::= SelectVarList | '*'
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
            select_clause.set_derived_var(ex, var.content)
            assert tokens.get_now().term is QueryTerm.RPAREN
        else:
            self.throw_error([QueryTerm.VARIABLE, QueryTerm.LPAREN], next_tok)
        return select_clause

    ''' Expression ::= BracketedExpression | BuiltInCall | Var '''
    def expression(self, tokens: LookaheadQueue) -> Expression:
        next_tok: Token = tokens.get_now()
        if next_tok.term is QueryTerm.LPAREN:
            ex: Expression = self.expression(tokens)
            assert tokens.get_now().term is QueryTerm.RPAREN
            return ex
        elif next_tok.term is QueryTerm.VARIABLE:
            return Expression(f"?{next_tok.content}")
        elif next_tok.term.value in QueryTerm.built_in_calls():
            return self.built_in_call(next_tok.term, tokens)
        else:
            built_in_qts: List[QueryTerm] = [QueryTerm(qt_str) for qt_str in QueryTerm.built_in_calls()]
            self.throw_error([QueryTerm.LPAREN, QueryTerm.VARIABLE] + built_in_qts, next_tok)
    
    def built_in_call(self, built_in_term: QueryTerm, tokens: LookaheadQueue) -> Expression:
        # TODO:
        # Group built_ins by use of parens and number of internal expressions.
        # What's below is not fully correct. Rework according to above.
        if built_in_term is QueryTerm.NOT:
            assert tokens.get_now().term is QueryTerm.EXISTS
            return Expression(f"NOT EXISTS {self.group_graph_pattern(tokens)}")
        elif built_in_term is QueryTerm.EXISTS:
            return Expression(f"EXISTS {self.group_graph_pattern(tokens)}")
        elif built_in_term is QueryTerm.CONCAT:
            # TODO: Think about Expression class model. Do I want expression_list
            # as a str or list. This thinking extends to the others in this function too.
            return Expression(f"CONCAT {self.expression_list(tokens)}")
        
        args: Expression = None
        assert tokens.get_now().term is QueryTerm.LPAREN
        if built_in_term is QueryTerm.SUBSTR or built_in_term is QueryTerm.REGEX or built_in_term is QueryTerm.REPLACE:
            ex1: Expression = self.expression(tokens)
            assert tokens.get_now().term is QueryTerm.COMMA
            ex2: Expression = self.expression(tokens)
            arg_str: str = f"{ex1}, {ex2}"
            if built_in_term is QueryTerm.REPLACE:
                assert tokens.get_now().term is QueryTerm.COMMA
                ex3: Expression = self.expression(tokens)
                arg_str += f", {ex3}"
            if tokens.lookahead().term is QueryTerm.COMMA:
                tokens.get_now()
                ex_extra: Expression = self.expression(tokens)
                arg_str += f", {ex_extra}"
            args = Expression(arg_str)
        else:
            args = self.expression(tokens)
        assert tokens.get_now().term is QueryTerm.RPAREN
        return Expression(f"{built_in_term.value}({args})")

    def dataset_clause(self, tokens: LookaheadQueue, dataset_clause: DatasetClause) -> DatasetClause:
        raise NotImplementedError()
    
    def where_clause(self, tokens: LookaheadQueue, where_clause: WhereClause) -> WhereClause:
        next_tok: Token = tokens.get_now()
        if next_tok.term is QueryTerm.WHERE:
            next_tok = tokens.get_now()
        assert next_tok.term is QueryTerm.LBRACKET
        # TODO: Figure out the where_clause model and methods
        where_clause.add(self.group_graph_pattern(tokens))
        assert tokens.get_now().term is QueryTerm.RBRACKET
        # TODO: Logic to check if we should call .group_graph_pattern() again
        return where_clause
    
    def group_graph_pattern(self, tokens: LookaheadQueue) -> GroupGraphPattern:
        # TODO: Implement this method
        return None
    
    def expression_list(self, tokens: LookaheadQueue) -> List[Expression]:
        raise NotImplementedError()
    
    def throw_error(self, expected_terms: List[QueryTerm], actual_tok: Token) -> None:
        raise ValueError(f"Expected {', '.join([term.name for term in expected_terms])} "
                         f"but got {actual_tok.term.value}")

# class ParseResult:

#     def __init__(self,
#                  query_type: str,
#                  query: Query) -> None:
#         self.query_type: str = query_type
#         self.query: Query = query


# class QueryManager:
#     def __init__(self) -> None:
#         self.ordered_clauses: List[IndexedClause] = []


#     def add_named_graph_to_all_where_clauses(self) -> None:


# class IndexedClause:
#     def __init__(self,
#                  start: int,
#                  end: int,
#                  clause_type: str) -> None:
#         self.start: int = start
#         self.end: int = end
#         self.clause_type: str = clause_type

#     def update_indices(self, adjustment: int) -> None:
#         self.start += adjustment
#         self.end += adjustment
