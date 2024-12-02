from main.tokens import QueryTerm, Token
from main import Query, SelectQuery, Prologue, LookaheadQueue

class QueryParser:

    def __init__(self) -> None:
        pass
    
    def parse(self, tokens: LookaheadQueue) -> Query:
        return self.query(tokens)

    ''' Query ::= Prologue
              ::= SelectQuery '''
    def query(self, tokens: LookaheadQueue) -> Query:
        prologue: Prologue = self.prologue(tokens, Prologue())
        select_query: SelectQuery = self.select_query(tokens)
        next_tok: Token = tokens.get(block=False)
        if next_tok.term is QueryTerm.EOF:
            return Query(prologue, select_query)
        else:
            raise ValueError(f"Expected EOF but got {next_tok.value}")

    ''' Prologue ::= (BaseDecl | PrefixDecl)* '''
    def prologue(self, tokens: LookaheadQueue, prologue: Prologue) -> Prologue:
        next_tok: Token = tokens.lookahead()

        if next_tok.term is QueryTerm.PREFIX:
            self.prefix_decl(tokens, prologue)
        elif next_tok.term is QueryTerm.BASE:
            self.base_decl(tokens, prologue)
        else:
            raise ValueError(f"Expected {QueryTerm.BASE.value} or {QueryTerm.PREFIX.value} but got {next_tok.term.value}")
        
        lookahead = tokens.lookahead()
        if lookahead is QueryTerm.BASE or lookahead is QueryTerm.PREFIX:
            return self.prologue(tokens, prologue)
        return prologue

    ''' BaseDecl ::= 'BASE' IRIREF '''
    def base_decl(self, tokens: LookaheadQueue, prologue: Prologue) -> None:
        assert tokens.get(block=False).term is QueryTerm.BASE
        iri_ref: Token = tokens.get(block=False)
        assert iri_ref.term is QueryTerm.IRI_REF
        prologue.set_base(iri_ref.content)

    ''' PrefixDecl ::= 'PREFIX' PNAME_NS IRIREF '''
    def prefix_decl(self, tokens: LookaheadQueue, prologue: Prologue) -> None:
        assert tokens.get(block=False).term is QueryTerm.PREFIX
        prefix_name: Token = tokens.get(block=False)
        assert prefix_name.term is QueryTerm.PREFIX_NAME


    ''' SelectQuery ::= SelectClause
                    ::= DatasetClause*
                    ::= WhereClause
    '''
    def select_query(self, tokens: LookaheadQueue) -> SelectQuery:
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