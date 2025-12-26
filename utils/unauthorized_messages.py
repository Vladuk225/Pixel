import random
from typing import Callable


def get_random_unauthorized_message(_: Callable[[str], list[str]]) -> str:
    messages = _("unauthorized_messages")
    return random.choice(messages)