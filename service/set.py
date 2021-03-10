from context.marshall_context import MarshallContext
from service.interface import ServiceInterface
from typing import Any, Dict, List


class SetService(ServiceInterface):

    async def _execute(self, ctx: MarshallContext, arg_map: Dict[Any, List[str]]):
        await ctx.send("Meow")

