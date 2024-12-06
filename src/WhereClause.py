from .SelectClause import SelectClause
from .GroupGraphPattern import GroupGraphPattern
from typing import List, Tuple

class WhereClause:

    # TODO: Figure out the datastructure for housing group graph patterns
    # and anything else the where clause contains
    def __init__(self) -> None:
        self.sub_select: SelectClause = None
        self.initial_triple_block: List[Tuple[int, GroupGraphPattern]] = None

    # TODO: Figure out how to add to where clause
    def add(self, something_to_add) -> None:
        pass
