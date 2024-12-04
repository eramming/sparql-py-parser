from .SelectClause import SelectClause
from .GroupGraphPattern import GroupGraphPattern
from typing import List, Tuple

class WhereClause:

    def __init__(self) -> None:
        self.sub_select: SelectClause = None
        self.initial_triple_block: List[Tuple[int, GroupGraphPattern]] = None