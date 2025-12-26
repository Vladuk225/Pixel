import asyncio
import time
from typing import Optional, Dict, Any
import aiosqlite


class BonusDB:
    def __init__(self, path: str = "bonuses.sqlite3"):
        self.path = path

    async def setup(self) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS user_bonuses (
                user_id INTEGER,
                b1_last_at INTEGER,              
                b2_last_at INTEGER,              
                b3_last_at INTEGER,              
                has_b2 INTEGER NOT NULL DEFAULT 0,  
                has_b3 INTEGER NOT NULL DEFAULT 0,  
                b1_money INTEGER NOT NULL DEFAULT 0,  
                b2_money INTEGER NOT NULL DEFAULT 0, 
                b3_money INTEGER NOT NULL DEFAULT 0,  
                b1_count INTEGER NOT NULL DEFAULT 0,  
                b2_count INTEGER NOT NULL DEFAULT 0,  
                b3_count INTEGER NOT NULL DEFAULT 0   
            );
            """)
            await db.commit()

    async def ensure_user(self, user_id: int) -> None:
        async with aiosqlite.connect(self.path) as db:
            cur = await db.execute("SELECT 1 FROM user_bonuses WHERE user_id = ?", (user_id,))
            row = await cur.fetchone()
            if not row:
                await db.execute("INSERT INTO user_bonuses (user_id) VALUES (?)", (user_id,))
                await db.commit()

    async def set_bonus_flags(self, user_id: int, has_b2: Optional[bool] = None, has_b3: Optional[bool] = None) -> None:
        await self.ensure_user(user_id)
        parts = []
        args = []
        if has_b2 is not None:
            parts.append("has_b2 = ?")
            args.append(1 if has_b2 else 0)
        if has_b3 is not None:
            parts.append("has_b3 = ?")
            args.append(1 if has_b3 else 0)
        if not parts:
            return
        args.append(user_id)
        async with aiosqlite.connect(self.path) as db:
            await db.execute(f"UPDATE user_bonuses SET {', '.join(parts)} WHERE user_id = ?", args)
            await db.commit()

    async def get_user(self, user_id: int) -> Dict[str, Any]:
        await self.ensure_user(user_id)
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM user_bonuses WHERE user_id = ?", (user_id,))
            row = await cur.fetchone()
            return dict(row)

    async def record_bonus(self, user_id: int, bonus_num: int, amount: float, ts: Optional[int] = None) -> None:
        if bonus_num not in (1, 2, 3):
            raise ValueError("bonus_num должен быть 1, 2 или 3")
        await self.ensure_user(user_id)
        ts = ts or int(time.time())
        last_at_col = f"b{bonus_num}_last_at"
        money_col = f"b{bonus_num}_money"
        count_col = f"b{bonus_num}_count"
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                f"UPDATE user_bonuses "
                f"SET {last_at_col} = ?, {money_col} = {money_col} + ?, {count_col} = {count_col} + 1 "
                f"WHERE user_id = ?",
                (ts, amount, user_id)
            )
            await db.commit()

    async def set_last_time(self, user_id: int, bonus_num: int, ts: int) -> None:
        if bonus_num not in (1, 2, 3):
            raise ValueError("bonus_num должен быть 1, 2 или 3")
        await self.ensure_user(user_id)
        col = f"b{bonus_num}_last_at"
        async with aiosqlite.connect(self.path) as db:
            await db.execute(f"UPDATE user_bonuses SET {col} = ? WHERE user_id = ?", (ts, user_id))
            await db.commit()

    async def add_money(self, user_id: int, bonus_num: int, amount: float) -> None:
        if bonus_num not in (1, 2, 3):
            raise ValueError("bonus_num должен быть 1, 2 или 3")
        await self.ensure_user(user_id)
        col = f"b{bonus_num}_money"
        async with aiosqlite.connect(self.path) as db:
            await db.execute(f"UPDATE user_bonuses SET {col} = {col} + ? WHERE user_id = ?", (amount, user_id))
            await db.commit()

    async def inc_count(self, user_id: int, bonus_num: int, step: int = 1) -> None:
        if bonus_num not in (1, 2, 3):
            raise ValueError("bonus_num должен быть 1, 2 или 3")
        await self.ensure_user(user_id)
        col = f"b{bonus_num}_count"
        async with aiosqlite.connect(self.path) as db:
            await db.execute(f"UPDATE user_bonuses SET {col} = {col} + ? WHERE user_id = ?", (step, user_id))
            await db.commit()