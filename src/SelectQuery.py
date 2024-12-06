from .SelectClause import SelectClause
from .DatasetClause import DatasetClause
from .WhereClause import WhereClause


class SelectQuery:
    
    def __init__(self) -> None:
        self.select_clause: SelectClause = SelectClause()
        self.dataset_clause: DatasetClause = DatasetClause()
        self.where_clause: WhereClause = WhereClause()
    
