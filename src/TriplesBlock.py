from typing import List
from .TriplesSameSubj import TriplesSameSubj

class TriplesBlock:

    def __init__(self) -> None:
        self.unique_subj_triples: List[TriplesSameSubj] = []

    def add_same_subj_triples(self, triples: TriplesSameSubj) -> None:
        self.unique_subj_triples.append(triples)

    def add_unique_subj_triples(self, unique_subj_triples: List[TriplesSameSubj]) -> None:
        self.unique_subj_triples += unique_subj_triples
