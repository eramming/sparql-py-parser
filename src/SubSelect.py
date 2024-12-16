from .SelectClause import SelectClause
from .WhereClause import WhereClause
from .SolnModifier import SolnModifier
from .GroupGraphPattern import GroupGraphPattern


class SubSelect(GroupGraphPattern):

    def __init__(self):
        self.select_clause: SelectClause = None
        self.where_clause: WhereClause = None
        self.soln_modifier: SolnModifier = None

    def set_select_clause(self, select_clause: SelectClause) -> None:
        self.select_clause = select_clause

    def set_where_clause(self, where_clause: WhereClause) -> None:
        self.where_clause = where_clause

    def set_soln_modifier(self, soln_modifier: SolnModifier) -> None:
        self.soln_modifier = soln_modifier
