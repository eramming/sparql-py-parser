from .GroupGraphPattern import GroupGraphPattern
from .Expressions import Expression

class ExistenceExpr(Expression):

    def __init__(self, ggp: GroupGraphPattern, not_exists: bool = False):
        super().__init__()
        self.ggp: GroupGraphPattern = ggp
        self.not_exists: bool = not_exists
