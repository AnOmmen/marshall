from typing import List


class Flag:
    name: str
    aliases: List[str]
    num_params: int

    def __init__(self, name: str, aliases: List[str], num_params: int):
        self.name = name
        self.aliases = aliases
        self.num_params = num_params
