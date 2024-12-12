from typing import Dict, List
from .TriplesBlock import TriplesBlock
from .GroupGraphPattern import GroupGraphPattern
from .GraphPatternNotTriples import GraphPatternNotTriples

class GroupGraphPatternSub:

    def __init__(self) -> None:
        self.triple_blocks: Dict[str, TriplesBlock] = {}
        self.other_patterns: Dict[str, GraphPatternNotTriples] = {}
        self.clause_order: List[str] = []

    def add_triple_block(self, triple_block: TriplesBlock) -> None:
        self.clause_order.append(triple_block.id)
        self.triple_blocks[triple_block.id] = triple_block

    def add_other_pattern(self, pattern: GraphPatternNotTriples) -> None:
        self.clause_order.append(pattern.id)
        self.other_patterns[pattern.id] = pattern
