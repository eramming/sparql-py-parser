from tokens import Token, QueryTerm
from src.main.python import LookaheadQueue
class Tokenizer:

    def __init__(self) -> None:
        pass

    def tokenize(self, query_str: str) -> LookaheadQueue[Token]:
        tokens: LookaheadQueue = LookaheadQueue()
        self.tokenize_helper(query_str, tokens)
        return tokens

    def tokenize_helper(self, query_str: str, tokens: LookaheadQueue[Token]) -> None:
        # Base Case:
        if len(query_str) == 0:
            tokens.put(Token(QueryTerm.EOF))
            return
        
        first_letter: str = query_str[0]
        if first_letter == "{":
            tokens.put(Token(QueryTerm.LBRACKET))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "}":
            tokens.put(Token(QueryTerm.RBRACKET))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "<":
            remainder: str = self.iri_ref_tokenizer(query_str, tokens)
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "?":
            remainder: str = self.variable_tokenizer(query_str, tokens)
            self.tokenize_helper(remainder, tokens)
        elif "DISTINCT" == query_str[0:8].upper():
            tokens.put(Token(QueryTerm.DISTINCT))
            remainder: str = query_str[8:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif "SELECT" == query_str[0:6].upper():
            tokens.put(Token(QueryTerm.SELECT))
            remainder: str = query_str[6:].lstrip()
            self.tokenize_helper(remainder, tokens)

    def iri_ref_tokenizer(self, query_str: str, tokens: LookaheadQueue[Token]) -> str:
        # validate then consume the IRIREF. Add to queue.
        # Return the remaining query_str
        raise NotImplementedError()
    
    def variable_tokenizer(self, query_str: str, tokens: LookaheadQueue[Token]) -> str:
        # validate then consume the variable. Add to queue.
        # Return the remaining query_str
        raise NotImplementedError()
