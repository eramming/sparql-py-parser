from SelectClause import SelectClause
from WhereClause import WhereClause
from SolnModifier import SolnModifier
from GroupGraphPattern import GroupGraphPattern


class SubSelect(GroupGraphPattern):

    def __init__(self):
        self.select_clause: SelectClause = SelectClause()
        self.where_clause: WhereClause = WhereClause()
        self.soln_modifier: SolnModifier = SolnModifier()
