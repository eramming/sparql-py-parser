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

    def is_empty(self) -> bool:
        return len(self.prefixes) == 0 and self.base_iri is None

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        base: str = ""
        if self.base_iri:
            base = f"BASE {self.base_iri}\n"
        prefixes: str = ""
        for prefix, iri in self.prefixes.items():
            prefixes += f"PREFIX {prefix}: {iri}\n"
        return f"{base}{prefixes}"
