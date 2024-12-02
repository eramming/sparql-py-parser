from main import SelectClause, DatasetClause, WhereClause


class SelectQuery:
    
    def __init__(self) -> None:
        self.select_clause: SelectClause = None
        self.dataset_clause: DatasetClause = None
        self.where_clause: WhereClause = None
    
