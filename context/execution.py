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
