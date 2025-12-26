import aiosqlite


class LinksDB:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    async def _create_table(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS links (
                    link TEXT NOT NULL
                )
            """)
            await db.commit()

    async def set_link(self, link_text: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM links")
            await db.execute("INSERT INTO links (link) VALUES (?)", (link_text,))
            await db.commit()

    async def get_link(self) -> str | None:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT link FROM links LIMIT 1") as cursor:
                row = await cursor.fetchone()
                return row[0] if row else None

    async def delete_link(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM links")
            await db.commit()