import random
from database.emojis_manager import EmojiDB


db = EmojiDB()


async def random_win_emojis():
    good, _ = await db.get_emoji_packs()
    return random.choice(good) if good else random.choice(['🙂', '😋', '😄', '🤑', '😃', '😇'])


async def random_lose_emojis():
    _, bad = await db.get_emoji_packs()
    return random.choice(bad) if bad else random.choice(['😔', '😕', '😣', '😞', '😢', '🤡'])


def get_num_user(num, user_position):
    if user_position is not None and user_position <= 999:
        emojis = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        return ''.join(emojis[int(d)] for d in str(num))
    return '➡️9️⃣9️⃣9️⃣'