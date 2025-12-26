import aiosqlite


class EmojiDB:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    async def _init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS emoji_packs (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    good_emojis TEXT,
                    bad_emojis TEXT
                )
            """)
            await db.execute("INSERT OR IGNORE INTO emoji_packs (id, good_emojis, bad_emojis) VALUES (1, '', '')")
            await db.commit()

    async def set_emoji_pack(self, kind: str, emojis: str):
        async with aiosqlite.connect(self.db_path) as db:
            if kind == "good":
                await db.execute("UPDATE emoji_packs SET good_emojis = ? WHERE id = 1", (emojis,))
            elif kind == "bad":
                await db.execute("UPDATE emoji_packs SET bad_emojis = ? WHERE id = 1", (emojis,))
            await db.commit()

    async def get_emoji_packs(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT good_emojis, bad_emojis FROM emoji_packs WHERE id = 1") as cursor:
                row = await cursor.fetchone()
                if row:
                    good = row[0].split() if row[0] else []
                    bad = row[1].split() if row[1] else []
                    return good, bad
        return [], []

    async def delete_emoji_packs(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE emoji_packs SET good_emojis = '', bad_emojis = '' WHERE id = 1")
            await db.commit()