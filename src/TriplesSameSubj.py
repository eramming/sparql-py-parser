from typing import Dict, List, Set
from collections import defaultdict
from .Verbs import Verb

class TriplesSameSubj:

    def __init__(self, subj: str):
        self.subj: str = subj
        self.po_dict: Dict[Verb, Set[str]] = defaultdict(set)

    def add_po_dict(self, po_dict: Dict[Verb, List[str]]) -> None:
        self.po_dict.update(po_dict)

    def add_p_with_many_o(self, p: Verb, many_o: Set[str]) -> None:
        self.po_dict[p].union(many_o)

    def add_po(self, p: Verb, o: str) -> None:
        self.po_dict[p].add(o)
