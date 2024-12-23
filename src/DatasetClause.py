

class DatasetClause:

    def __init__(self, dataset: str, is_named: bool) -> None:
        self.dataset: str = dataset
        self.is_named: bool = is_named

    def __format__(self, format_spec):
        self.__str__()
    
    def __str__(self):
        named: str = "NAMED " if self.is_named else ""
        return f"FROM {named}{self.dataset}\n"
