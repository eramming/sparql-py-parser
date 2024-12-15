from .SelectClause import SelectClause
from .DatasetClause import DatasetClause
from .WhereClause import WhereClause
from .SolnModifier import SolnModifier


class SelectQuery:
    
    def __init__(self) -> None:
        self.select_clause: SelectClause = None
        self.dataset_clause: DatasetClause = None
        self.where_clause: WhereClause = None
        self.soln_modifier: SolnModifier = None

    def set_select_clause(self, select_clause: SelectClause) -> None:
        self.select_clause = select_clause

    def set_dataset_clause(self, dataset_clause: DatasetClause) -> None:
        self.dataset_clause = dataset_clause

    def set_where_clause(self, where_clause: WhereClause) -> None:
        self.where_clause = where_clause

    def set_soln_modifier(self, soln_modifier: SolnModifier) -> None:
        self.soln_modifier = soln_modifier
    
