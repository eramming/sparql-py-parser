from typing import Dict, List
from .TriplesBlock import TriplesBlock
from uuid import uuid4

class GroupGraphPattern:

    def __init__(self, enclosing_clause: str = "") -> None:
        self.id = uuid4()
        self.enclosing_clause: str = enclosing_clause
        self.triple_blocks: Dict[str, TriplesBlock] = {}
        self.other_clauses: Dict[str, GroupGraphPattern] = {}
        self.clause_order: List[str] = []

    def add_triple_block(self, triple_block: TriplesBlock) -> None:
        self.clause_order.append(triple_block.id)
        self.triple_blocks[triple_block.id] = triple_block

    def add_non_triple_clause(self, non_triple_clause: 'GroupGraphPattern') -> None:
        self.clause_order.append(non_triple_clause.id)
        self.other_clauses[id] = non_triple_clause