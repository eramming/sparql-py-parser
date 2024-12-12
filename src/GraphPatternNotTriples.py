from .SelectClause import SelectClause
from .WhereClause import WhereClause
from .SolnModifier import SolnModifier
from .GroupGraphPattern import GroupGraphPattern
from .Expressions import Function, Expression
from uuid import uuid4

class GraphPatternNotTriples:

    def __init__(self):
        self.id = uuid4()


class GraphGraphPattern(GraphPatternNotTriples):

    def __init__(self, var_or_iri: str, ggp: GroupGraphPattern):
        super().__init__()
        self.var_or_iri: str = var_or_iri
        self.ggp: GroupGraphPattern = ggp

    def __str__(self):
        return f"GRAPH {self.var_or_iri} {self.ggp}"
    
    def __format__(self, format_spec):
        return self.__str__()


class OptionalGraphPattern(GraphPatternNotTriples):

    def __init__(self, ggp: GroupGraphPattern):
        super().__init__()
        self.ggp: GroupGraphPattern = ggp

    def __str__(self):
        return f"OPTIONAL {self.ggp}"
    
    def __format__(self, format_spec):
        return self.__str__()
    

class UnionGraphPattern(GraphPatternNotTriples):

    def __init__(self, l_ggp: GroupGraphPattern, r_ggp: GroupGraphPattern):
        super().__init__()
        self.l_ggp: GroupGraphPattern = l_ggp
        self.r_ggp: GroupGraphPattern = r_ggp

    def __str__(self):
        return f"{self.l_ggp} UNION {self.r_ggp}"
    
    def __format__(self, format_spec):
        return self.__str__()
    

class MinusGraphPattern(GraphPatternNotTriples):

    def __init__(self, ggp: GroupGraphPattern):
        super().__init__()
        self.ggp: GroupGraphPattern = ggp

    def __str__(self):
        return f"MINUS {self.ggp}"
    
    def __format__(self, format_spec):
        return self.__str__()
    

class ServiceGraphPattern(GraphPatternNotTriples):

    def __init__(self, is_silent: bool, var_or_iri: str, ggp: GroupGraphPattern):
        super().__init__()
        self.is_silent: bool = is_silent
        self.var_or_iri: str = var_or_iri
        self.ggp: GroupGraphPattern = ggp

    def __str__(self):
        silent: str = "SILENT " if self.is_silent else ""
        return f"SERVICE {silent}{self.var_or_iri} {self.ggp}"
    
    def __format__(self, format_spec):
        return self.__str__()
    

class Filter(GraphPatternNotTriples):

    def __init__(self, expr: Expression):
        super().__init__()
        self.expr: Expression = expr

    def __str__(self):
        return f"FILTER {self.expr}"
    
    def __format__(self, format_spec):
        return self.__str__()
    

class Bind(GraphPatternNotTriples):

    def __init__(self, expr: Expression, var: str):
        super().__init__()
        self.expr: Expression = expr
        self.var: str = var

    def __str__(self):
        return f"BIND {self.expr} AS ?{self.var}"
    
    def __format__(self, format_spec):
        return self.__str__()
