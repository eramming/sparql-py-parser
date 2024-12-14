from GroupGraphPattern import GroupGraphPattern

class WhereClause:

    def __init__(self, ggp: GroupGraphPattern, uses_keyword: bool) -> None:
        self.ggp: GroupGraphPattern = ggp
        self.uses_keyword = uses_keyword

    def __str__(self):
        where: str = "WHERE " if self.uses_keyword else ""
        return f"{where}{self.ggp}"
    
    def __format__(self, format_spec):
        return self.__str__()
