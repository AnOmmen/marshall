from source.exception.source_error import SourceError


class GuildNotFoundError(SourceError):
    _guild_not_found = 'Guild not found for ID of {id}.'

    def __init__(self, guild_id):
        super().__init__(self._guild_not_found.replace('{id}', str(guild_id)))
