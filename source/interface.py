from psycopg2._psycopg import connection


class SourceInterface:
    _conn: connection

    def __init__(self):
        self._conn = self._connect()
        pass

    def _connect(self) -> connection:
        raise NotImplementedError

    def close(self):
        self._conn.close()

    def deactivate_guild(self, guild_id):
        raise NotImplementedError

    def register_guild(self, guild_id) -> bool:
        raise NotImplementedError
