from typing import Dict


class Prologue:

    def __init__(self,
                 base_iri: str = None,
                 prefixes: Dict[str, str] = {}) -> None:
        self.base_iri = base_iri
        self.prefixes: Dict[str, str] = prefixes

    def set_base(self, base_iri: str) -> None:
        self.base_iri = base_iri

    def remove_base(self) -> None:
        self.base_iri = None

    def set_prefix(self, prefix: str, iri: str) -> None:
        self.prefixes[prefix] = iri

    def remove_prefix(self, prefix: str) -> None:
        del self.prefixes[prefix]

    def remove_all_prefixes(self) -> None:
        self.prefixes = {}