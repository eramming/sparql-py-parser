from tokens import QueryTerm

class Validators:

    def __init__(self) -> None:
        self.validators = {QueryTerm.IRI: self._iri_validator,
                           QueryTerm.PREFIX_NAME: self._prefix_name_validator,
                           QueryTerm.FULL_IRI: self._full_iri_validator,
                           QueryTerm.VARIABLE: self.variable_validator}
        
    def _iri_validator(self, iri: str) -> bool:
        raise NotImplementedError()
    
    def _prefix_name_validator(self, prefix_name: str) -> bool:
        raise NotImplementedError()
    
    def _full_iri_validator(self, full_iri: str) -> bool:
        raise NotImplementedError()
    
    def _variable_validator(self, variable: str) -> bool:
        raise NotImplementedError()
