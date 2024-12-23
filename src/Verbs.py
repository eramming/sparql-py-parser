from uuid import uuid4
from typing import List
from .PathEnums import PathOp, PathMod

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
    

class VerbPath:

    def __init__(self):
        pass


class UnaryVerbPath(VerbPath):

    def __init__(self, verb_path: VerbPath):
        super().__init__()
        self.verb_path: VerbPath = verb_path


class IdentityVerbPath(UnaryVerbPath):

    def __init__(self, verb_path: VerbPath):
        super().__init__(verb_path)

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        return f"({self.verb_path})"

    
class MultiPathVerbPath(VerbPath):

    def __init__(self, l_path: VerbPath, r_path: VerbPath, path_op: PathOp):
        super().__init__()
        self.l_path: VerbPath = l_path
        self.r_path: VerbPath = r_path
        self.path_op: PathOp = path_op

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        return f"{self.l_path} {self.path_op.value} {self.r_path}"


class InverseVerbPath(UnaryVerbPath):

    def __init__(self, verb_path: VerbPath):
        super().__init__(verb_path)

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        return f"^{self.verb_path}"


class ElementVerbPath(UnaryVerbPath):

    def __init__(self, verb_path: VerbPath, path_mod: PathMod):
        super().__init__(verb_path)
        self.path_mod: PathMod = path_mod

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        return f"{self.verb_path}{self.path_mod.value}"


# Covers Iri and 'a'
class TerminalVerbPath(VerbPath):

    def __init__(self, stringified_val: str):
        super().__init__()
        self.stringified_val: str = stringified_val

    def __format__(self, format_spec):
        return self.__str__()
    
    def __str__(self):
        return self.stringified_val


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
