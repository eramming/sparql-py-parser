from typing import List
from .SelectClause import SelectClause
from .GroupGraphPatternSub import GroupGraphPatternSub
from enum import Enum


class GroupGraphPattern:

    class Enclosers(Enum):
        WHERE = "WHERE"
        OPTIONAL = "OPTIONAL"
        GRAPH = "GRAPH"
        NO_ENCLOSER = ""

    def __init__(self, enclosing_clause: Enclosers):
        self.enclosing_clause: GroupGraphPattern.Enclosers = enclosing_clause
        self.ggp_list: List[GroupGraphPattern] = []
        self.ggp_sub: GroupGraphPatternSub = None
        self.sub_select: SelectClause = None
    
    def set_ggp_sub(self, ggp_sub: GroupGraphPatternSub) -> None:
        self.sub_select = None
        self.ggp_sub = ggp_sub

    def set_sub_select(self, sub_select: SelectClause) -> None:
        self.ggp_sub = None
        self.sub_select = sub_select

    def add_ggp(self, ggp: 'GroupGraphPattern') -> None:
        self.ggp_list.append(ggp)
