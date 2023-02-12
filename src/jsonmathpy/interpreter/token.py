from dataclasses import dataclass
from jsonmathpy.interpreter.types import TokenType


@dataclass
class Token:
    type: TokenType
    value: any

    def __repr__(self):
        return self.type.name + (f":{self.value}" if self.value != None else "")