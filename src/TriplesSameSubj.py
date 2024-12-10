from typing import Dict, List, Tuple
from collections import defaultdict

class TriplesSameSubj:

    def __init__(self, subj: str):
        self.subj: str = subj
        self.po: Dict[str, List[str]] = defaultdict(list)

    def add_p_with_o_list(self, p: str, many_o: List[str]) -> None:
        self.po[p] += many_o

    def add_po(self, p: str, o: str) -> None:
        self.po[p].append(o)

    def add_po_list(self, many_po: List[Tuple[str, str]]) -> None:
        for (p, o) in many_po:
            self.po[p].append(o)
