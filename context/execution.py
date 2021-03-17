from context.application import ApplicationContext
from data.flag import Flag
from typing import Dict, List


class ExecutionContext(ApplicationContext):
    flags: Dict[Flag, List[str]]
    params: List[str]

    def __init__(self, ctx: ApplicationContext, flags: Dict[Flag, List[str]], params: List[str]):
        super().__init__(ctx, ctx._source)
        self.flags = flags
        self.params = params

    def has_flag(self, flag_name) -> bool:
        for flag in self.flags.keys():
            if flag.name == flag_name:
                return True
        return False
