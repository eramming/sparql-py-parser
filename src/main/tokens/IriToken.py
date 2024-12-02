
from main.tokens import Token
import re

class IriToken(Token):
    def __init__(self, iri: str) -> None:
        super().__init__()
        self._is_valid(iri)
        self.iri = iri

    def _is_valid(self, iri: str) -> None:
        pattern: str = "^([a-z]|[A-Z]|[0-9]|[-])+$"
        if re.search(pattern, iri):
            return
        raise ValueError("Iri is invalid.")
    
    def __str__(self) -> str:
        return self.iri
    
    def __eq__(self, value: object) -> bool:
        if type(value) == type(self):
            return value.iri == self.iri
        return False
