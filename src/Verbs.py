from uuid import uuid4

class Verb:

    def __init__(self):
        self._id = uuid4()

    def get_verb(self) -> str:
        raise NotImplementedError("Only implemented in subclasses")

    def __hash__(self) -> int:
        return hash(self._id)

    def __eq__(self, value) -> bool:
        if isinstance(value, Verb):
            return value._id == self._id
        return False
    

class VerbPath(Verb):

    def __init__(self, verb: str = None, verb_path: 'VerbPath' = None):
        super().__init__()
        if verb is not None and verb_path is not None:
            raise ValueError("Can only have 1 of [verb, VerbPath]")
        self.verb_path: VerbPath = verb_path
        self.verb: str = verb

    def get_verb(self) -> str:
        return self.verb

    def set_verb_path(self, verb_path: 'VerbPath') -> None:
        self.verb_path = verb_path
        self.verb = None

    def set_verb(self, verb: str) -> None:
        self.verb = verb
        self.verb_path = None

    def __str__(self):
        if self.verb:
            return self.verb
        else:
            return f"( {self.verb_path} )"
    
    def __format__(self, format_spec):
        return self.__str__()


class VarVerb(Verb):

    def __init__(self, verb: str):
        super().__init__()
        self.verb: str = verb

    def get_verb(self) -> str:
        return self.verb
    
    def __str__(self):
        return self.verb
    
    def __format__(self, format_spec):
        return self.__str__()
