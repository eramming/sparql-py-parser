from uuid import uuid4
from typing import List, Dict, Any
from .TriplesBlock import TriplesBlock
from .PatternModifiers import PatternModifier


class GroupGraphPattern:

    def __init__(self):
        pass


class GroupGraphPatternSub:

    def __init__(self, patterns: List['GroupGraphPattern'] = None):
        self.triples_blocks: Dict[str, TriplesBlock] = {}
        self.modifiers: Dict[str, PatternModifier] = {}
        self.patterns: Dict[str, GroupGraphPattern] = {}
        self.order_of_elements: List[str] = []

        if patterns:
            self.order_of_elements = [uuid4() for _ in patterns]
            self.patterns = {uuid: p for (uuid, p) in zip(self.order_of_elements, patterns)}
    
    def add_triples_block(self, triples_block: TriplesBlock) -> None:
        uuid: str = uuid4()
        self.order_of_elements.append(uuid)
        self.triples_blocks[uuid] = triples_block
    
    def add_modifier(self, modifier: PatternModifier) -> None:
        uuid: str = uuid4()
        self.order_of_elements.append(uuid)
        self.modifiers[uuid] = modifier

    def add_pattern(self, pattern: 'GroupGraphPattern') -> None:
        uuid: str = uuid4()
        self.order_of_elements.append(uuid)
        self.patterns[uuid] = pattern

    def elements_in_order(self) -> List[Any]:
        all_elements: Dict[str, Any] = self.triples_blocks | self.modifiers | self.patterns
        return [all_elements[uuid] for uuid in self.order_of_elements]

    def __str__(self):
        ggp_interior: str = "\n\t".join([str(ele) for ele in self.elements_in_order()])
        if ggp_interior == "":
            return "{ }"
        return f"{{\n\t{ggp_interior}\n}}"
    
    def __format__(self, format_spec):
        return self.__str__()


class GraphGraphPattern(GroupGraphPatternSub):

    def __init__(self, var_or_iri: str):
        super().__init__()
        self.var_or_iri: str = var_or_iri

    def __str__(self):
        return f"GRAPH {self.var_or_iri} {super().__str__()}"
    
    def __format__(self, format_spec):
        return self.__str__()


class OptionalGraphPattern(GroupGraphPatternSub):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"OPTIONAL {super().__str__()}"
    
    def __format__(self, format_spec):
        return self.__str__()
    

class UnionGraphPattern(GroupGraphPatternSub):

    def __init__(self, patterns: List[GroupGraphPattern]):
        super().__init__(patterns=patterns)
    
    def add_triples_block(self, triples_block: TriplesBlock) -> None:
        raise ValueError("Can't set TriplesBlock in a UnionGraphPattern!")
    
    def add_modifier(self, modifier: PatternModifier) -> None:
        raise ValueError("Can't set PatternModifier in a UnionGraphPattern!")

    def __str__(self):
        return " UNION ".join([str(ele) for ele in self.elements_in_order()])
    
    def __format__(self, format_spec):
        return self.__str__()
    

class MinusGraphPattern(GroupGraphPatternSub):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"MINUS {super().__str__()}"
    
    def __format__(self, format_spec):
        return self.__str__()
    

class ServiceGraphPattern(GroupGraphPatternSub):

    def __init__(self, is_silent: bool, var_or_iri: str):
        super().__init__()
        self.is_silent: bool = is_silent
        self.var_or_iri: str = var_or_iri

    def __str__(self):
        silent: str = "SILENT " if self.is_silent else ""
        return f"SERVICE {silent}{self.var_or_iri} {super().__str__()}"
    
    def __format__(self, format_spec):
        return self.__str__()
