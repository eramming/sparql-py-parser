from .Token import Token
from .QueryTerm import QueryTerm
from src.LookaheadQueue import LookaheadQueue
import re


class Tokenizer:

    def __init__(self) -> None:
        pass

    def tokenize(self, query_str: str) -> LookaheadQueue:
        tokens: LookaheadQueue = LookaheadQueue()
        self.tokenize_helper(query_str.lstrip(), tokens)
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
            remainder: str = self.variable_tokenizer(query_str[1:], tokens)
            self.tokenize_helper(remainder, tokens)
        elif first_letter == ":":
            tokens.put(Token(QueryTerm.COLON))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "#":
            indx: int = re.search("(\r\n|\n)", query_str).end()
            if indx == -1:
                tokens.put(Token(QueryTerm.EOF))
                return
            self.tokenize_helper(query_str[indx:].lstrip(), tokens)
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
            remainder: str = self.prefixed_name_prefix_tokenizer(query_str, tokens)
            self.tokenize_helper(remainder, tokens)

    def iri_ref_tokenizer(self, query_str: str, tokens: LookaheadQueue) -> str:
        iri_ref: str = re.search("(^<[a-z0-9A-Z:_\\-#%\\.\\/]+>)", query_str).__getitem__(0)
        if not iri_ref:
            raise ValueError("Invalid IRIREF")
        tokens.put(Token(QueryTerm.IRIREF, iri_ref[1:len(iri_ref) - 1]))
        return query_str[len(iri_ref):].lstrip()

    def variable_tokenizer(self, query_str: str, tokens: LookaheadQueue) -> str:
        variable: str = re.search("(^[a-z0-9A-Z_]+)", query_str).__getitem__(0)
        if not variable:
            raise ValueError("Invalid variable")
        tokens.put(Token(QueryTerm.VARIABLE, variable))
        return query_str[len(variable):].lstrip()
    
    # Always before a colon
    def prefixed_name_prefix_tokenizer(self, query_str: str, tokens: LookaheadQueue) -> str:
        prefix_name: str = re.search("(^[a-zA-Z_][a-zA-Z_0-9//.//-]*[a-zA-Z_0-9//-]?:)", query_str).__getitem__(0)
        if not prefix_name:
            raise ValueError("Invalid prefixed name prefix")
        tokens.put(Token(QueryTerm.PREFIXED_NAME_PREFIX, prefix_name[0:len(prefix_name) - 1]))
        tokens.put(Token(QueryTerm.COLON))

        remainder: str = query_str[len(prefix_name):]
        first_letter: str = remainder[0]
        if first_letter == "<":
            return remainder
        elif first_letter == " ":
            return remainder.lstrip()
        else:
            return self.prefixed_name_local_tokenizer(remainder, tokens)
    
    # Always after a colon
    def prefixed_name_local_tokenizer(self, query_str: str, tokens: LookaheadQueue) -> str:
        pattern: str = "(^([a-zA-Z_:0-9]|%[0-9A-Fa-f]{2})"
        pattern += "([a-zA-Z_:0-9//-//.]|%[0-9A-Fa-f]{2})*"
        pattern += "([a-zA-Z_:0-9//-]|%[0-9A-Fa-f]{2})?)"
        local_name: str = re.search(pattern, query_str).__getitem__(0)
        if not local_name:
            raise ValueError("Invalid prefixed_name_local")
        tokens.put(Token(QueryTerm.PREFIXED_NAME_LOCAL, local_name))
        return query_str[len(local_name):].lstrip()
