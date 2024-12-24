from .SelectClause import SelectClause
from .DatasetClause import DatasetClause
from .WhereClause import WhereClause
from .SolnModifier import SolnModifier
from .GroupGraphPattern import GroupGraphPatternSub


class SelectQuery:
    
    def __init__(self) -> None:
        self.select_clause: SelectClause = SelectClause()
        self.dataset_clause: DatasetClause = None
        self.where_clause: WhereClause = WhereClause(GroupGraphPatternSub(), True)
        self.soln_modifier: SolnModifier = SolnModifier()

    def set_select_clause(self, select_clause: SelectClause) -> None:
        self.select_clause = select_clause

    def set_dataset_clause(self, dataset_clause: DatasetClause) -> None:
        self.dataset_clause = dataset_clause

    def set_where_clause(self, where_clause: WhereClause) -> None:
        self.where_clause = where_clause

    def set_soln_modifier(self, soln_modifier: SolnModifier) -> None:
        self.soln_modifier = soln_modifier

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        ds_clause: str = ""
        if self.dataset_clause:
            ds_clause = str(self.dataset_clause)
        return f"{self.select_clause}{ds_clause}{self.where_clause}{self.soln_modifier}"      
