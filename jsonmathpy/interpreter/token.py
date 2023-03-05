from dataclasses import dataclass
from jsonmathpy.interpreter.types import TokenType


@dataclass
class Token:
    """ Represents a token with a TokenType and an optional value. """

    type: TokenType
    "Enum type representing the type of the token."

    value: any
    "Represents the actual value of the token, which can be of any type."


    def __repr__(self):
        return self.type.name + (f":{self.value}" if self.value != None else "")