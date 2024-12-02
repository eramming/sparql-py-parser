from tokens import TokenLiteral, Token
from . import Query, SelectQuery, Prologue, LookaheadQueue

class QueryParser:

    def __init__(self) -> None:
        pass
    
    def parse(self, tokens: LookaheadQueue[Token]) -> Query:
        return self.query(tokens)

    ''' Query ::= Prologue
              ::= SelectQuery '''
    def query(self, tokens: LookaheadQueue[Token]) -> Query:
        prologue: Prologue = self.prologue(tokens, Prologue())
        select_query: SelectQuery = self.select_query(tokens)
        next_tok: Token = tokens.get(block=False)
        if next_tok is TokenLiteral.EOF:
            return Query(prologue, select_query)
        else:
            raise ValueError(f"Expected EOF but got {next_tok.value}")

    ''' Prologue ::= (BaseDecl | PrefixDecl)* '''
    def prologue(self, tokens: LookaheadQueue[Token], prologue: Prologue) -> Prologue:
        next_tok: Token = tokens.get(block=False)
        if next_tok is not TokenLiteral.BASE or next_tok is not TokenLiteral.PREFIX:
            raise ValueError(f"Expected {TokenLiteral.BASE.value} or {TokenLiteral.PREFIX.value} but got {next_tok}")
        elif next_tok is TokenLiteral.PREFIX:
            # Validate that the following token is an iri
            prologue.set_prefix()
        else: # if BASE:
            assert tokens.get(block=False) is Token.COLON
            iri_tok: Token = tokens.get(block=False)
            assert instanceof(
            # Validate that the following token is an iri
            prologue.set_base()
        lookahead = tokens.lookahead()
        if lookahead is Token.BASE or lookahead is Token.PREFIX:
            return self.prologue(tokens, prologue)
        return prologue

    ''' SelectQuery ::= SelectClause
                    ::= DatasetClause*
                    ::= WhereClause
    '''
    def select_query(self, tokens: Queue[Token]) -> SelectQuery:
        raise NotImplementedError()

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