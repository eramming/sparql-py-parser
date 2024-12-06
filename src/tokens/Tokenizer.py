from .Token import Token
from .QueryTerm import QueryTerm
from src.LookaheadQueue import LookaheadQueue
import re
from re import Match
from typing import List


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
        matched: bool = self.tokenize_single_char_identifiers(query_str, tokens)
        if not matched:
            matched = self.tokenize_keyword(query_str, tokens)
        if not matched:
            matched = self.tokenize_prefixed_name_prefix(query_str, tokens)
        if not matched:
            raise ValueError(f"Couldn't tokenize the remainder of the string:\n{query_str}")
            
    def tokenize_single_char_identifiers(self, query_str: str, tokens: LookaheadQueue) -> bool:
        matched: bool = True
        first_letter: str = query_str[0]
        if first_letter == "{":
            tokens.put(Token(QueryTerm.LBRACKET))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "}":
            tokens.put(Token(QueryTerm.RBRACKET))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "(":
            tokens.put(Token(QueryTerm.LPAREN))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == ")":
            tokens.put(Token(QueryTerm.RPAREN))
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
        elif first_letter == ".":
            tokens.put(Token(QueryTerm.PERIOD))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == ",":
            tokens.put(Token(QueryTerm.COMMA))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == ";":
            tokens.put(Token(QueryTerm.SEMI_COLON))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "*":
            tokens.put(Token(QueryTerm.ASTERISK))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == '"' or first_letter == "'":
            remainder: str = self.string_literal_tokenizer(query_str, tokens)
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "#":
            indx: int = re.search("(\r\n|\n)", query_str).end()
            if indx == -1:
                tokens.put(Token(QueryTerm.EOF))
                return
            self.tokenize_helper(query_str[indx:].lstrip(), tokens)
        elif re.search("^(\\+?|-?)[0-9]+(\\.[0-9]*)?", query_str):
            remainder: str = self.number_literal_tokenizer(query_str, tokens)
            self.tokenize_helper(remainder, tokens)
        else:
            matched = False
        return matched
        
    def tokenize_keyword(self, query_str: str, tokens: LookaheadQueue) -> None:
        match: Match = re.search("(\\S+)\\s", query_str)
        if not match:
            return False
        word: str = match.groups()[0]

        if "(" in word:
            return self.tokenize_keyword_helper("^(\\S+)\\(", query_str, tokens)
        elif "{" in word:
            return self.tokenize_keyword_helper("^(\\S+){", query_str, tokens)
        else:
            return self.tokenize_keyword_helper("^(\\S+)\\s", query_str, tokens)

    def tokenize_keyword_helper(self, pattern: str, query_str: str, tokens: LookaheadQueue) -> str:
        match: Match = re.search(pattern, query_str)
        if not match:
            return False
        keyword: str = match.groups()[0].upper()
        qt: QueryTerm = QueryTerm.from_keyword(keyword)
        if qt:
            tokens.put(Token(qt))
            remainder: str = query_str[len(keyword):].lstrip()
            self.tokenize_helper(remainder, tokens)
            return True
        return False

    def iri_ref_tokenizer(self, query_str: str, tokens: LookaheadQueue) -> str:
        match: Match = re.search("(^<[a-z0-9A-Z:_\\-#%\\.\\/]+>)", query_str)
        if not match:
            raise ValueError("Invalid IRIREF")
        iri_ref: str = match.groups()[0]
        tokens.put(Token(QueryTerm.IRIREF, iri_ref[1:len(iri_ref) - 1]))
        return query_str[len(iri_ref):].lstrip()

    def variable_tokenizer(self, query_str: str, tokens: LookaheadQueue) -> str:
        match: Match = re.search("(^[a-z0-9A-Z_]+)", query_str)
        if not match:
            raise ValueError("Invalid variable")
        variable: str = match.groups()[0]
        tokens.put(Token(QueryTerm.VARIABLE, variable))
        return query_str[len(variable):].lstrip()
    
    # Always before a colon
    def tokenize_prefixed_name_prefix(self, query_str: str, tokens: LookaheadQueue) -> str:
        match: Match = re.search("(^[a-zA-Z_][a-zA-Z_0-9\\.\\-]*[a-zA-Z_0-9\\-]?:)", query_str)
        if not match:
            return False
        prefix_name: str = match.groups()[0]
        tokens.put(Token(QueryTerm.PREFIXED_NAME_PREFIX, prefix_name[0:len(prefix_name) - 1]))
        tokens.put(Token(QueryTerm.COLON))

        remainder: str = query_str[len(prefix_name):]
        first_letter: str = remainder[0]
        if first_letter == "<" or first_letter == " ":
            self.tokenize_helper(remainder.lstrip(), tokens)
            return True
        else:
            return self.prefixed_name_local_tokenizer(remainder, tokens)
    
    # Always after a colon
    def prefixed_name_local_tokenizer(self, query_str: str, tokens: LookaheadQueue) -> str:
        pattern: str = "(^([a-zA-Z_:0-9]|%[0-9A-Fa-f]{2})"
        pattern += "(([a-zA-Z_:0-9\\-\\.]|%[0-9A-Fa-f]{2})*"
        pattern += "[a-zA-Z_:0-9\\-]|%[0-9A-Fa-f]{2})?)"
        match: Match = re.search(pattern, query_str)
        if not match:
            raise ValueError("Invalid prefixed_name_local")
        local_name: str = match.groups()[0]
        tokens.put(Token(QueryTerm.PREFIXED_NAME_LOCAL, local_name))
        self.tokenize_helper(query_str[len(local_name):].lstrip(), tokens)
        return True
    
    def string_literal_tokenizer(self, query_str: str, tokens: LookaheadQueue) -> str:
        pattern: str = ""
        quote_count: int = None
        if query_str[0:3] == "'''":
            pattern = "^'''([^']+)'''"
            quote_count = 6
        elif query_str[0] == "'":
            pattern = "^'([^'\\n\\r]+)'"
            quote_count = 2
        elif query_str[0:3] == '"""':
            pattern = '^"""([^"]+)"""'
            quote_count = 6
        else:
            pattern = '^"([^"\\n\\r]+)"'
            quote_count = 2
        match: Match = re.search(pattern, query_str)
        if not match:
            raise ValueError("Invalid string literal")
        literal: str = match.groups()[0]
        tokens.put(Token(QueryTerm.STRING_LITERAL, literal))
        return query_str[len(literal) + quote_count:].lstrip()
    
    def number_literal_tokenizer(self, query_str: str, tokens: LookaheadQueue) -> str:
        match: Match = re.search("^((\\+?|-?)[0-9]+(\\.[0-9]*)?)", query_str)
        if not match:
            raise ValueError("Invalid number literal")
        num_as_string: str = match.groups()[0]
        tokens.put(Token(QueryTerm.NUMBER_LITERAL, num_as_string))
        return query_str[len(num_as_string):].lstrip()
