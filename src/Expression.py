

class Expression:
    def __init__(self, expression) -> None:
        self.expression = expression

    def __str__(self) -> str:
        return self.expression
    
    def __format__(self, format_spec: str) -> str:
        return self.expression
