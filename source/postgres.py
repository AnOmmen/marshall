import os
import psycopg2

from datetime import datetime
from discord import Guild
from discord.ext.commands import Context
from psycopg2._psycopg import connection
from psycopg2._psycopg import cursor
from psycopg2.extras import RealDictCursor
from source.exception.guild_not_found import GuildNotFoundError
from source.interface import SourceInterface
from typing import Optional


class PostgresSource(SourceInterface):
    _conn: connection
    table_guild_registry = 'guild_registry'

    def __init__(self):
        self._conn = psycopg2.connect(
            dbname=os.environ['DB_DATABASE'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'])

    def _get_guild_attribute(self, guild_id, attribute: str):
        return self._get_guild_attributes(guild_id, [attribute])

    def _get_guild_attributes(self, guild_id, attributes: [str]):
        curs: cursor = self._conn.cursor(cursor_factory=RealDictCursor)
        statement = 'SELECT'
        for attribute in attributes:
            statement += ' ' + attribute + ','
        statement = statement[:-1] + ' FROM ' + self.table_guild_registry + ' WHERE guild_id = %s'
        curs.execute(statement, [guild_id])
        if curs.rowcount == 0:
            raise GuildNotFoundError(guild_id)
        result = curs.fetchone()
        curs.close()
        if len(attributes) == 1:
            return result[attributes[0]]
        return result

    def deactivate_guild(self, guild: Guild):
        curs: cursor = self._conn.cursor()
        curs.execute(
            'UPDATE ' + self.table_guild_registry + ' SET active = %s, deactivated_at = %s WHERE guild_id = %s',
            [False, datetime.now(), guild.id])
        self._conn.commit()
        curs.close()

    def get_guild_guest_role(self, ctx: Context) -> str:
        return self._get_guild_attribute(ctx.guild.id, 'guest_role')

    def get_guild_guest_role_id(self, ctx: Context) -> Optional[int]:
        return self._get_guild_attribute(ctx.guild.id, 'guest_role_id')

    def register_guild(self, guild: Guild) -> bool:
        curs: cursor = self._conn.cursor()
        try:
            active = self._get_guild_attribute(guild.id, 'active')
            if not active:
                curs.execute(
                    'UPDATE ' + self.table_guild_registry + ' SET active = %s WHERE guild_id = %s',
                    [True, guild.id])
            else:
                curs.close()
                return False
        except GuildNotFoundError:
            curs.execute('INSERT INTO ' + self.table_guild_registry + ' (guild_id) VALUES (%s)', [guild.id])
        self._conn.commit()
        curs.close()
        return True

    def set_guild_guest_role_comp(self, ctx: Context, name: str, id: int):
        curs: cursor = self._conn.cursor()
        curs.execute(
            'UPDATE ' + self.table_guild_registry + ' SET guest_role = %s,  guest_role_id = %s WHERE guild_id = %s',
            [name, id, ctx.guild.id])
        self._conn.commit()
        curs.close()

    def set_guild_guest_role_id(self, ctx: Context, id: int):
        curs: cursor = self._conn.cursor()
        curs.execute(
            'UPDATE ' + self.table_guild_registry + ' SET guest_role_id = %s WHERE guild_id = %s',
            [id, ctx.guild.id])
        self._conn.commit()
        curs.close()

    def set_guild_member_role_comp(self, ctx: Context, name: str, id: int):
        curs: cursor = self._conn.cursor()
        curs.execute(
            'UPDATE ' + self.table_guild_registry + ' SET member_role = %s, member_role_id = %s WHERE guild_id = %s',
            [name, id, ctx.guild.id])
        self._conn.commit()
        curs.close()
