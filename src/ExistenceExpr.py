from GroupGraphPattern import GroupGraphPatternSub
from Expressions import Expression

class ExistenceExpr(Expression):

    def __init__(self, pattern: GroupGraphPatternSub, not_exists: bool = False):
        super().__init__()
        self.pattern: GroupGraphPatternSub = pattern
        self.not_exists: bool = not_exists
