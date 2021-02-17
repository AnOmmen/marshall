import os
import psycopg2

from datetime import datetime
from psycopg2._psycopg import connection
from psycopg2._psycopg import cursor
from psycopg2.extras import RealDictCursor
from source.interface import SourceInterface


class DefaultSource(SourceInterface):
    table_guild_registry = 'guild_registry'

    def _connect(self) -> connection:
        return psycopg2.connect(
            dbname=os.environ['DB_DATABASE'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'])

    def deactivate_guild(self, guild_id):
        curs: cursor = self._conn.cursor()
        curs.execute(
            'UPDATE ' + self.table_guild_registry + ' SET active = %s, deactivated_at = %s WHERE id = %s',
            [False, datetime.now(), guild_id])
        self._conn.commit()
        curs.close()

    def register_guild(self, guild_id) -> bool:
        registered = True
        curs: cursor = self._conn.cursor(cursor_factory=RealDictCursor)
        curs.execute('SELECT id, active FROM ' + self.table_guild_registry + ' WHERE id = %s', [guild_id])
        if curs.rowcount == 0:
            curs.execute('INSERT INTO ' + self.table_guild_registry + ' (id) VALUES (%s)', [guild_id])
        else:
            result = curs.fetchone()
            if result['active'] is False:
                curs.execute('UPDATE ' + self.table_guild_registry + ' SET active = %s WHERE id = %s', [True, guild_id])
            else:
                registered = False
        self._conn.commit()
        curs.close()
        return registered
