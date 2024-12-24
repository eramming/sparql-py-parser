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
        matched: bool = self.tokenize_binary_identifiers(query_str, tokens)
        if not matched:
            matched = self.tokenize_unary_identifiers(query_str, tokens)
        if not matched:
            matched = self.tokenize_bool_literals(query_str, tokens)
        if not matched:
            matched = self.tokenize_keyword(query_str, tokens)
        if not matched:
            matched = self.tokenize_prefixed_name_prefix(query_str, tokens)
        if not matched:
            raise ValueError(f"Couldn't tokenize the remainder of the string:\n{query_str}")

    def tokenize_binary_identifiers(self, query_str: str, tokens: LookaheadQueue) -> bool:
        matched: bool = True
        binary_chars: str = query_str[0:2]
        if binary_chars == "||":
            tokens.put(Token(QueryTerm.LOGICAL_OR))
            remainder: str = query_str[2:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif binary_chars == ">=":
            tokens.put(Token(QueryTerm.G_OR_EQ))
            remainder: str = query_str[2:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif binary_chars == "<=":
            tokens.put(Token(QueryTerm.L_OR_EQ))
            remainder: str = query_str[2:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif binary_chars == "!=":
            tokens.put(Token(QueryTerm.NOT_EQ))
            remainder: str = query_str[2:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif binary_chars == "&&":
            tokens.put(Token(QueryTerm.LOGICAL_AND))
            remainder: str = query_str[2:].lstrip()
            self.tokenize_helper(remainder, tokens)
        else:
            matched = False
        return matched

    def tokenize_unary_identifiers(self, query_str: str, tokens: LookaheadQueue) -> bool:
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
        elif first_letter == "/":
            tokens.put(Token(QueryTerm.DIV))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "*":
            tokens.put(Token(QueryTerm.ASTERISK))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "+":
            tokens.put(Token(QueryTerm.ADD))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "-":
            tokens.put(Token(QueryTerm.SUB))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "|":
            tokens.put(Token(QueryTerm.PIPE))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "^":
            tokens.put(Token(QueryTerm.CARAT))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "<":
            remainder: str = None
            if re.search("^(<[^<>\"{}|^`\\]\\s]*>)", query_str):
                remainder = self.iri_ref_tokenizer(query_str, tokens)
            else:
                tokens.put(Token(QueryTerm.LT))
                remainder = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == ">":
            tokens.put(Token(QueryTerm.GT))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "?":
            remainder: str = None
            if re.search("[a-z0-9A-Z_]", query_str[1]): 
                remainder = self.variable_tokenizer(query_str[1:], tokens)
            else:
                tokens.put(Token(QueryTerm.QUESTION))
                remainder = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == "!":
            tokens.put(Token(QueryTerm.EXCLAMATION))
            remainder: str = query_str[1:].lstrip()
            self.tokenize_helper(remainder, tokens)
        elif first_letter == ":":
            tokens.put(Token(QueryTerm.COLON))
            remainder: str = query_str[1:].lstrip()
            pattern: str = "(^([a-zA-Z_:0-9]|%[0-9A-Fa-f]{2})"
            pattern += "(([a-zA-Z_:0-9\\-\\.]|%[0-9A-Fa-f]{2})*"
            pattern += "[a-zA-Z_:0-9\\-]|%[0-9A-Fa-f]{2})?)"
            match: Match = re.search(pattern, remainder)
            if match:
                self.prefixed_name_local_tokenizer(remainder, tokens)    
            else:
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
        elif first_letter == "=":
            tokens.put(Token(QueryTerm.EQUALS))
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
        elif re.search("^[0-9]+(\\.[0-9]*)?", query_str):
            remainder: str = self.number_literal_tokenizer(query_str, tokens)
            self.tokenize_helper(remainder, tokens)
        else:
            matched = False
        return matched
        
    def tokenize_bool_literals(self, query_str: str, tokens: LookaheadQueue) -> bool:
        matched: bool = False
        match: Match = re.search("^(true|false)(\\(|=|\\s|$|&|\\||\\))", query_str, flags=re.IGNORECASE)
        if not match:
            return False
        word: str = match.groups()[0].upper()
        tokens.put(Token(QueryTerm.from_keyword(word)))
        remainder: str = query_str[len(word):].lstrip()
        self.tokenize_helper(remainder, tokens)
        return True

    def tokenize_keyword(self, query_str: str, tokens: LookaheadQueue) -> bool:
        matched: bool = False
        match: Match = re.search("^([a-zA-Z][a-zA-Z_]*)(\\(|{|=|\\s|$)", query_str)
        if not match:
            return False
        word: str = match.groups()[0].upper()
        term: QueryTerm = None

        if Tokenizer.keyword_has_terminus(word):
            if Tokenizer.keyword_has_valid_terminus(word):
                term = QueryTerm.from_keyword(word[:len(word) - 1])
        else:
            term = QueryTerm.from_keyword(word)
        if term is not None:
            matched = True
            tokens.put(Token(term))
            remainder: str = query_str[len(term.value):].lstrip()
            self.tokenize_helper(remainder, tokens)
        return matched
    
    def keyword_has_valid_terminus(word: str) -> bool:
        return (
            word.endswith("(") and QueryTerm.parenable(word[:len(word) - 1])
            or word.endswith("{") and QueryTerm.bracketable(word[:len(word) - 1])
            or word.endswith("=") and QueryTerm.equalable(word[:len(word) - 1])
            or re.search("\\s", word[-1])                                                
        )
    
    def keyword_has_terminus(word: str) -> bool:
        return True if re.search("\\(|{|=|\\s", word[-1]) else False

    def iri_ref_tokenizer(self, query_str: str, tokens: LookaheadQueue) -> str:
        match: Match = re.search("^(<[^<>\"{}|^`\\]\\s]*>)", query_str)
        if not match:
            raise ValueError("Invalid IRIREF")
        iri_ref: str = match.groups()[0]
        tokens.put(Token(QueryTerm.IRIREF, iri_ref))
        return query_str[len(iri_ref):].lstrip()

    def variable_tokenizer(self, query_str: str, tokens: LookaheadQueue) -> str:
        match: Match = re.search("(^[a-z0-9A-Z_]+)", query_str)
        if not match:
            raise ValueError("Invalid variable")
        variable: str = match.groups()[0]
        tokens.put(Token(QueryTerm.VARIABLE, f"?{variable}"))
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
        match: Match = re.search("^([0-9]+(\\.[0-9]*)?)", query_str)
        if not match:
            raise ValueError("Invalid number literal")
        num_as_string: str = match.groups()[0]
        tokens.put(Token(QueryTerm.U_NUMBER_LITERAL, num_as_string))
        return query_str[len(num_as_string):].lstrip()
