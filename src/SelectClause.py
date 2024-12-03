from typing import List, Tuple

class SelectClause:

    def __init__(self) -> None:
        self.explicit_vars: List[str] = None
        self.derived_vars: List[Tuple[str, str]]
        
