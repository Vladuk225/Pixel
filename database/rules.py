import aiosqlite


class RulesDB:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    async def _create_table(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS rules (
                    rule TEXT NOT NULL
                )
            """)
            await db.commit()

    async def set_rule(self, rule_text: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM rules")
            await db.execute("INSERT INTO rules (rule) VALUES (?)", (rule_text,))
            await db.commit()

    async def get_rule(self) -> str | None:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT rule FROM rules LIMIT 1") as cursor:
                row = await cursor.fetchone()
                return row[0] if row else None

    async def delete_rule(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM rules")
            await db.commit()