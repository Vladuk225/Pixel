import aiosqlite


class Chat:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    async def create_table(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id INTEGER PRIMARY KEY
                )
            ''')
            await db.commit()

    async def add_chat(self, chat_id: int):
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('INSERT INTO chats (chat_id) VALUES (?)', (chat_id,))
                await db.commit()
        except aiosqlite.IntegrityError:
            pass

    async def chat_exists(self, chat_id: int) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT 1 FROM chats WHERE chat_id = ?', (chat_id,)) as cursor:
                result = await cursor.fetchone()
                return result is not None

    @staticmethod
    def is_valid_chat_id(chat_id) -> bool:
        return isinstance(chat_id, int) and chat_id >= 0