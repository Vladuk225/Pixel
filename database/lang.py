import aiosqlite

class UserLanguageDB:
    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS language (
                    user_id INTEGER PRIMARY KEY,
                    language TEXT DEFAULT 'ru'
                )
            """)
            await db.commit()

    async def get_language(self, user_id: int) -> str:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT language FROM language WHERE user_id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else "en"

    async def set_language(self, user_id: int, lang_code: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO language (user_id, language)
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET language=excluded.language
            """, (user_id, lang_code))
            await db.commit()