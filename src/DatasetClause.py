

class DatasetClause:

    def __init__(self, dataset: str, is_named: bool) -> None:
        self.dataset: str = dataset
        self.is_named: bool = is_named
