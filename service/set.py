from context.execution import ExecutionContext
from data.flag import Flag
from service.base import Service
from typing import List


class SetService(Service):

    async def _execute(self, ctx: ExecutionContext):
        pass

    def _flags(self) -> List[Flag]:
        return [
            Flag('c', ['create'], 0),
            Flag('rg', ['guest-role', 'role-guest'], 1),
            Flag('rm', ['member-role', 'role-member'], 1)
        ]

    def _num_params(self) -> int:
        return 0
