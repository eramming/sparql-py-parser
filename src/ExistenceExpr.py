from .GroupGraphPattern import GroupGraphPattern
from .Expressions import Expression

class ExistenceExpr(Expression):

    def __init__(self, ggp: GroupGraphPattern, not_exists: bool = False):
        super().__init__()
        self.ggp: GroupGraphPattern = ggp
        self.not_exists: bool = not_exists

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        not_exists: str = "NOT " if self.not_exists else ""
        return f"{not_exists}EXISTS {self.ggp}"
