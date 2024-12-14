from GroupGraphPattern import GroupGraphPattern
from Expressions import Expression

class ExistenceExpr(Expression):

    def __init__(self, pattern: GroupGraphPattern, not_exists: bool = False):
        super().__init__()
        self.pattern: GroupGraphPattern = pattern
        self.not_exists: bool = not_exists
