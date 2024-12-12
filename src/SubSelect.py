from .SelectClause import SelectClause
from .WhereClause import WhereClause
from .SolnModifier import SolnModifier


class SubSelect:

    def __init__(self):
        self.select_clause: SelectClause = SelectClause()
        self.where_clause: WhereClause = WhereClause()
        self.soln_modifier: SolnModifier = SolnModifier()
