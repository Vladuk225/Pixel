import aiosqlite


class GameSettingsDB:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    async def create_table(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS game_settings (
                    chat_id INTEGER PRIMARY KEY,
                    coin INTEGER DEFAULT 1,
                    slots INTEGER DEFAULT 1,
                    spin INTEGER DEFAULT 1
                )
            ''')
            await db.commit()

    async def ensure_chat_exists(self, chat_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT chat_id FROM game_settings WHERE chat_id = ?', (chat_id,)) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    await db.execute('INSERT INTO game_settings (chat_id) VALUES (?)', (chat_id,))
                    await db.commit()

    async def get_statuses(self, chat_id: int) -> dict:
        await self.ensure_chat_exists(chat_id)
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT * FROM game_settings WHERE chat_id = ?', (chat_id,)) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return {}
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))

    async def toggle_game(self, chat_id: int, game_name: str) -> int | None:
        await self.ensure_chat_exists(chat_id)
        statuses = await self.get_statuses(chat_id)
        if game_name not in statuses:
            return None
        new_value = 0 if statuses[game_name] == 1 else 1
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                f'UPDATE game_settings SET {game_name} = ? WHERE chat_id = ?',
                (new_value, chat_id)
            )
            await db.commit()
        return new_value

    async def is_game_enabled(self, chat_id: int, game_name: str) -> bool:
        await self.ensure_chat_exists(chat_id)
        statuses = await self.get_statuses(chat_id)
        return statuses.get(game_name, 0) == 1