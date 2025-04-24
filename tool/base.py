from typing import Callable, Dict

class Tool:
    def __init__(self, name: str, description: str, schema: Dict, function: Callable):
        self.name = name
        self.description = description
        self.schema = schema
        self.function = function

    def Operation(self, **kwargs):
        return self.function(**kwargs)