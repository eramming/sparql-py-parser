from .GroupGraphPattern import GroupGraphPattern

class WhereClause:

    # TODO: Figure out the datastructure for housing group graph patterns
    # and anything else the where clause contains
    def __init__(self, ggp: GroupGraphPattern, has_explicit_where_keyword: bool) -> None:
        self.ggp: GroupGraphPattern = ggp
        self.has_explicit_where_keyword = has_explicit_where_keyword

    def __str__(self):
        where: str = "WHERE " if self.has_explicit_where_keyword else ""
        return f"{where}{self.ggp}"
    
    def __format__(self, format_spec):
        return self.__str__()
