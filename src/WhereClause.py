from .GroupGraphPattern import GroupGraphPattern

class WhereClause:

    def __init__(self, ggp: GroupGraphPattern, uses_keyword: bool) -> None:
        self.ggp: GroupGraphPattern = ggp
        self.uses_keyword = uses_keyword

    def __str__(self):
        where: str = "WHERE " if self.uses_keyword else ""
        if not str(self.ggp).startswith("{"):
            formatted_interior: str = ""
            for line in str(self.ggp).splitlines(keepends=True):
                formatted_interior += f"\t{line}"
            return f"{where}{{\n{formatted_interior}\n}}\n"
        return f"{where}{self.ggp}\n"
    
    def __format__(self, format_spec):
        return self.__str__()
