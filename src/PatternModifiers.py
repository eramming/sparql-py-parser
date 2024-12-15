from .Expressions import Expression


class PatternModifier:

    def __init__(self):
        pass


class Bind(PatternModifier):

    def __init__(self, expr: Expression, var: str):
        super().__init__()
        self.expr: Expression = expr
        self.var: str = var

    def __str__(self):
        return f"BIND {self.expr} AS ?{self.var}"
    
    def __format__(self, format_spec):
        return self.__str__()
    

class Filter(PatternModifier):

    def __init__(self, expr: Expression):
        super().__init__()
        self.expr: Expression = expr

    def __str__(self):
        return f"FILTER {self.expr}"
    
    def __format__(self, format_spec):
        return self.__str__()
