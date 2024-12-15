from typing import List
from .TriplesSameSubj import TriplesSameSubj

class TriplesBlock:

    def __init__(self) -> None:
        self.triples_same_subj: List[TriplesSameSubj] = []

    def add_triples_same_subj(self, triples: TriplesSameSubj) -> None:
        self.triples_same_subj.append(triples)
