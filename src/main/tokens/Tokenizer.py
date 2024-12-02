from main.tokens.Token import Token
from main.tokens.QueryTerm import QueryTerm
from main import LookaheadQueue
import re


class Tokenizer:

    def __init__(self) -> None:
        pass

    def tokenize(self, query_str: str) -> LookaheadQueue:
        tokens: LookaheadQueue = LookaheadQueue()
        self.tokenize_helper(query_str, tokens)
        return tokens

    def tokenize_helper(self, query_str: str, tokens: LookaheadQueue) -> None:
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
        elif first_letter == ":":
            tokens.put(Token(QueryTerm.COLON))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        # Regex ensures there's some kind of whitespace after the keyword
        elif re.search("^DISTINCT\\s$", query_str[0:9].upper()):
            tokens.put(Token(QueryTerm.DISTINCT))
            remainder: str = query_str[8:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif re.search("^SELECT\\s$", query_str[0:7].upper()):
            tokens.put(Token(QueryTerm.SELECT))
            remainder: str = query_str[6:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif re.search("^FROM\\s$", query_str[0:5].upper()):
            tokens.put(Token(QueryTerm.FROM))
            remainder: str = query_str[4:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif re.search("^BASE\\s$", query_str[0:5].upper()):
            tokens.put(Token(QueryTerm.BASE))
            remainder: str = query_str[4:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif re.search("^PREFIX\\s$", query_str[0:7].upper()):
            tokens.put(Token(QueryTerm.PREFIX))
            remainder: str = query_str[6:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif re.search("^AS\\s$", query_str[0:3].upper()):
            tokens.put(Token(QueryTerm.AS))
            remainder: str = query_str[2:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif re.search("^NAMED\\s$", query_str[0:6].upper()):
            tokens.put(Token(QueryTerm.NAMED))
            remainder: str = query_str[5:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif re.search("^WHERE(\\s|{)$", query_str[0:6].upper()):
            tokens.put(Token(QueryTerm.WHERE))
            remainder: str = query_str[5:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif re.search("^OPTIONAL(\\s|{)$", query_str[0:9].upper()):
            tokens.put(Token(QueryTerm.OPTIONAL))
            remainder: str = query_str[8:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif re.search("^GRAPH\\s$", query_str[0:6].upper()):
            tokens.put(Token(QueryTerm.GRAPH))
            remainder: str = query_str[5:].lstrip()
            self.tokenize_helper(remainder, tokens)
        else:
            raise ValueError(f"---Can't handle input:---\n{query_str}")

    def iri_ref_tokenizer(self, query_str: str, tokens: LookaheadQueue) -> str:
        iri_ref: str = re.search("^<[a-z0-9A-Z:_\\-#%\\.\\/]+>", query_str)
        if not iri_ref:
            raise ValueError("Invalid IRIREF")
        tokens.put(Token(QueryTerm.IRIREF, iri_ref[1:len(iri_ref) - 1]))
        return query_str[len(iri_ref):].lstrip()

    def variable_tokenizer(self, query_str: str, tokens: LookaheadQueue) -> str:
        variable: str = re.search("^\\?[a-z0-9A-Z_]+", query_str)
        if not variable:
            raise ValueError("Invalid variable")
        tokens.put(Token(QueryTerm.VARIABLE, variable))
        return query_str[len(variable):].lstrip()
