from SelectClause import SelectClause
from DatasetClause import DatasetClause
from WhereClause import WhereClause

class SelectQuery:
    
    def __init__(self) -> None:
        self.select_clause: SelectClause = None
        self.dataset_clause: DatasetClause = None
        self.where_clause: WhereClause = None
    
    