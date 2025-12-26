import aiosqlite
from datetime import datetime, timedelta
import time
from utils.emojis import get_num_user
from utils.transform import transform_int


DB_PATH = "database.db"


async def init_tables():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            game_id INTEGER,
            nickname TEXT,
            gender TEXT,
            balance INTEGER,
            last_active TIMESTAMP
        )""")
        await db.execute("""CREATE TABLE IF NOT EXISTS bans (
            user_id INTEGER PRIMARY KEY,
            reason TEXT,
            until INTEGER
        )""")
        await db.execute("""CREATE TABLE IF NOT EXISTS hidden_users (
            telegram_id INTEGER PRIMARY KEY
        )""")
        await db.execute("""CREATE TABLE IF NOT EXISTS notifications (
            telegram_id INTEGER PRIMARY KEY,
            allow_transfers INTEGER DEFAULT 1,
            FOREIGN KEY (telegram_id) REFERENCES users (telegram_id) ON DELETE CASCADE
        )""")
        await db.commit()


class User:
    def __init__(self, telegram_id, game_id=None, nickname=None, gender=None, balance=0):
        self.telegram_id = telegram_id
        self.game_id = game_id
        self.nickname = nickname
        self.gender = gender
        self.balance = balance

    async def save(self):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                INSERT OR REPLACE INTO users (telegram_id, game_id, nickname, gender, balance)
                VALUES (?, ?, ?, ?, ?)
            """, (self.telegram_id, self.game_id, self.nickname, self.gender, self.balance))
            await db.commit()

    @classmethod
    async def get(cls, telegram_id):
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("""
                SELECT telegram_id, game_id, nickname, gender, balance
                FROM users WHERE telegram_id = ?
            """, (telegram_id,))
            row = await cursor.fetchone()
            if row:
                return cls(*row)
            return None

    @classmethod
    async def get_nickname(cls, telegram_id):
        user = await cls.get(telegram_id)
        return user.nickname if user else None

    @classmethod
    async def generate_new_game_id(cls):
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT MAX(game_id) FROM users")
            max_id = (await cursor.fetchone())[0]
            return 1 if max_id is None else max_id + 1

    async def set_balance(self, amount):
        if amount < 0:
            raise ValueError("Баланс не может быть отрицательным.")
        self.balance = amount
        await self.save()

    async def add_balance(self, amount):
        if amount < 0:
            raise ValueError("Нельзя добавить отрицательное количество средств.")
        self.balance += amount
        await self.save()

    async def subtract_balance(self, amount):
        if amount < 0:
            raise ValueError("Нельзя списать отрицательное количество средств.")
        if self.balance < amount:
            raise ValueError("Недостаточно средств.")
        self.balance -= amount
        await self.save()

    def __str__(self):
        return f"User(telegram_id={self.telegram_id}, game_id={self.game_id}, nickname='{self.nickname}', gender={self.gender}, balance={self.balance})"


class Leaderboard:
    @staticmethod
    async def top_users(limit=10):
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT telegram_id FROM hidden_users")
            hidden_ids = {row[0] async for row in cursor}

            cursor = await db.execute("""
                SELECT telegram_id, game_id, nickname, gender, balance
                FROM users
                ORDER BY balance DESC
            """)
            rows = await cursor.fetchall()

            visible_users = [User(*row) for row in rows if row[0] not in hidden_ids]
            return visible_users[:limit]

    @staticmethod
    async def get_user_position(user_id):
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT telegram_id FROM users ORDER BY balance DESC")
            rows = await cursor.fetchall()
            for i, row in enumerate(rows, start=1):
                if row[0] == user_id:
                    return i
            return None

    @staticmethod
    async def format_top_users(limit=10, current_user_id=None, _=None):
        users = await Leaderboard.top_users(limit)
        result = f"🏆 <b>{_('top_text')}</b>\n\n"

        for i, user in enumerate(users, start=1):
            place = get_num_user(i, i)
            nickname = f'<a href="tg://user?id={user.telegram_id}">{user.nickname}</a>'
            result += f"{place} {nickname} — {transform_int(user.balance)}ℙ\n"

        if current_user_id:
            position = await Leaderboard.get_user_position(current_user_id)
            user = await User.get(current_user_id)
            if user and position:
                emoji_place = get_num_user(position, position)
                nickname = f'<a href="tg://user?id={user.telegram_id}">{user.nickname}</a>'
                result += '➖➖➖➖➖➖➖➖➖➖➖➖➖'
                result += f"\n{emoji_place} {nickname} — {transform_int(user.balance)}ℙ"

        return result


class TopVisibilityManager:
    @staticmethod
    async def hide_user(telegram_id: int):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("INSERT OR IGNORE INTO hidden_users (telegram_id) VALUES (?)", (telegram_id,))
            await db.commit()

    @staticmethod
    async def unhide_user(telegram_id: int):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("DELETE FROM hidden_users WHERE telegram_id = ?", (telegram_id,))
            await db.commit()

    @staticmethod
    async def is_hidden(telegram_id: int) -> bool:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT 1 FROM hidden_users WHERE telegram_id = ?", (telegram_id,))
            return await cursor.fetchone() is not None

    @staticmethod
    async def get_hidden_users() -> list:
        users = []
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT telegram_id FROM hidden_users")
            ids = [row[0] async for row in cursor]
            for uid in ids:
                user = await User.get(uid)
                if user:
                    users.append(user)
        return users

    @staticmethod
    async def format_hidden_users() -> str:
        users = await TopVisibilityManager.get_hidden_users()
        if not users:
            return "👤 Нет скрытых пользователей в топе."
        result = "🙈 <b>Скрытые пользователи из топа:</b>\n\n"
        for user in users:
            nickname = user.nickname or f"Пользователь {user.telegram_id}"
            result += f"• <a href='tg://user?id={user.telegram_id}'>{nickname}</a> — {user.balance}ℙ\n"
        return result


class Stats:
    @staticmethod
    async def total_users():
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM users")
            count = (await cursor.fetchone())[0]
            return count

    @staticmethod
    async def total_chats():
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM chats")
            count = (await cursor.fetchone())[0]
            return count

    @staticmethod
    async def banned_users():
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM bans")
            count = (await cursor.fetchone())[0]
            return count

    @staticmethod
    async def count_active_users_24h():
        now = datetime.now()
        day_ago = now - timedelta(hours=24)
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM users WHERE last_active >= ?", (day_ago,))
            result = await cursor.fetchone()
            return result[0] if result else 0

    @staticmethod
    async def get_all_chats():
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute('SELECT chat_id FROM chats')
            return [row[0] async for row in cursor]

    @staticmethod
    async def get_all_users():
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute('SELECT telegram_id FROM users')
            return [row[0] async for row in cursor]


class NotificationSettings:
    def __init__(self, telegram_id, allow_transfers=1):
        self.telegram_id = telegram_id
        self.allow_transfers = allow_transfers

    async def save(self):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                INSERT OR REPLACE INTO notifications (telegram_id, allow_transfers)
                VALUES (?, ?)
            """, (self.telegram_id, self.allow_transfers))
            await db.commit()

    @classmethod
    async def get(cls, telegram_id):
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("""
                SELECT telegram_id, allow_transfers FROM notifications WHERE telegram_id = ?
            """, (telegram_id,))
            row = await cursor.fetchone()
            if row:
                return cls(*row)
            return cls(telegram_id)

    async def update_allow_transfers(self, status: bool):
        self.allow_transfers = 1 if status else 0
        await self.save()

    def __str__(self):
        return f"NotificationSettings(telegram_id={self.telegram_id}, allow_transfers={self.allow_transfers})"


class BanDatabase:
    @staticmethod
    async def ban_user(user_id: int, reason: str, duration_seconds: int):
        until = int(time.time()) + duration_seconds
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                INSERT INTO bans (user_id, reason, until)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    reason=excluded.reason,
                    until=excluded.until
            """, (user_id, reason, until))
            await db.commit()

    @staticmethod
    async def unban_user(user_id: int):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("DELETE FROM bans WHERE user_id = ?", (user_id,))
            await db.commit()

    @staticmethod
    async def get_ban(user_id: int):
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT reason, until FROM bans WHERE user_id = ?", (user_id,))
            return await cursor.fetchone()

    @staticmethod
    async def get_all_bans():
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT user_id, reason, until FROM bans")
            return await cursor.fetchall()