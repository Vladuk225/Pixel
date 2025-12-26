import aiosqlite


class ChannelDB:
    @staticmethod
    async def init_db():
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS channels (
                    channel_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    subscribers INTEGER DEFAULT 0,
                    likes INTEGER DEFAULT 0,
                    last_ad INTEGER,
                    last_video INTEGER,
                    last_like INTEGER
                )
            """)
            await db.commit()

    @staticmethod
    async def add_channel(user_id: int, name: str,
                          subscribers: int = 0, likes: int = 0,
                          last_ad: int = None, last_video: int = None,
                          last_like: int = None):
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("""
                INSERT INTO channels (user_id, name, subscribers, likes, last_ad, last_video, last_like)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, name, subscribers, likes, last_ad, last_video, last_like))
            await db.commit()
            return cursor.lastrowid

    @staticmethod
    async def get_channel(channel_id: int):
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute(
                "SELECT * FROM channels WHERE channel_id = ?", (channel_id,))
            return await cursor.fetchone()

    @staticmethod
    async def get_user_channels(user_id: int):
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute(
                "SELECT * FROM channels WHERE user_id = ?", (user_id,))
            return await cursor.fetchall()

    @staticmethod
    async def update_channel_name(channel_id: int, name: str):
        async with aiosqlite.connect('database.db') as db:
            await db.execute(
                'UPDATE channels SET name = ? WHERE channel_id = ?', (name, channel_id))
            await db.commit()

    @staticmethod
    async def delete_channel(channel_id: int):
        async with aiosqlite.connect('database.db') as db:
            await db.execute(
                "DELETE FROM channels WHERE channel_id = ?", (channel_id,))
            await db.commit()

    @staticmethod
    async def get_channel_id(user_id: int):
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute(
                "SELECT channel_id FROM channels WHERE user_id = ?", (user_id,))
            res = await cursor.fetchone()
            return res[0] if res else None

    @staticmethod
    async def update_subscribers(channel_id: int, new_subs: int):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""
                UPDATE channels
                SET subscribers = subscribers + ?, last_video = strftime('%s','now')
                WHERE channel_id = ?
            """, (new_subs, channel_id))
            await db.commit()

    @staticmethod
    async def update_likes(channel_id: int, user_id, like_change: int = 1):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""
                UPDATE channels
                SET likes = likes + ?
                WHERE channel_id = ?
            """, (like_change, channel_id))
            await db.execute("""
                UPDATE channels
                SET last_like = strftime('%s','now')
                WHERE user_id = ?
            """, (user_id,))
            await db.commit()

    @staticmethod
    async def update_last_ad(channel_id: int):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("UPDATE channels SET last_ad = strftime('%s','now') WHERE channel_id = ?", (channel_id,))
            await db.commit()