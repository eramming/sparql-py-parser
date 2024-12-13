from SubSelect import SubSelect
from GroupGraphPatternSub import GroupGraphPatternSub
import GraphPatternNotTriples


class GroupGraphPattern(GraphPatternNotTriples.GraphPatternNotTriples):

    def __init__(self):
        super().__init__()
        self.ggp_sub: GroupGraphPatternSub = None
        self.sub_select: SubSelect = None
    
    def set_ggp_sub(self, ggp_sub: GroupGraphPatternSub) -> None:
        self.sub_select = None
        self.ggp_sub = ggp_sub

    def set_sub_select(self, sub_select: SubSelect) -> None:
        self.ggp_sub = None
        self.sub_select = sub_select
