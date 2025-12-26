from datetime import datetime
import random
from typing import Callable


def get_greeting(_: Callable[[str], str]) -> str:
    now = datetime.now().hour

    greetings_day = [
        _("greeting_day_1"), _("greeting_day_2"), _("greeting_day_3"),
        _("greeting_day_4"), _("greeting_day_5"), _("greeting_day_6"),
        _("greeting_day_7"), _("greeting_day_8"),
    ]

    greetings_evening = [
        _("greeting_evening_1"), _("greeting_evening_2"), _("greeting_evening_3"),
        _("greeting_evening_4"), _("greeting_evening_5"),
    ]

    greetings_night = [
        _("greeting_night_1"), _("greeting_night_2"), _("greeting_night_3"),
        _("greeting_night_4"), _("greeting_night_5"),
    ]

    if 12 <= now < 18:
        return random.choice(greetings_day)
    elif 18 <= now < 23:
        return random.choice(greetings_evening)
    else:
        return random.choice(greetings_night)