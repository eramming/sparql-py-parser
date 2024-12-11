from typing import Dict, List
from .TriplesBlock import TriplesBlock
from .GroupGraphPattern import GroupGraphPattern
from uuid import uuid4

class GroupGraphPatternSub:

    def __init__(self) -> None:
        self.id = uuid4()
        self.triple_blocks: Dict[str, TriplesBlock] = {}
        self.other_clauses: Dict[str, GroupGraphPattern] = {}
        self.clause_order: List[str] = []

    def add_triple_block(self, triple_block: TriplesBlock) -> None:
        self.clause_order.append(triple_block.id)
        self.triple_blocks[triple_block.id] = triple_block

    def add_enclosed_ggp(self, enclosed_ggp: GroupGraphPattern) -> None:
        self.clause_order.append(enclosed_ggp.id)
        self.other_clauses[id] = enclosed_ggp
