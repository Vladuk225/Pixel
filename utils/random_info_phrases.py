import random
from typing import Callable


def get_wallet_phrase(balance: int, _: Callable[[str], list[str]]) -> str:
    phrases = _("wallet_phrase")
    phrase = random.choice(phrases).replace('[balance]', balance)
    return phrase