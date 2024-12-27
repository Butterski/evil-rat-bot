from datetime import datetime, timedelta
from typing import Tuple, Dict, Set, List

def get_next_week_mondays_and_sundays() -> Tuple[int, int]:
    """Returns timestamps for next Monday and Sunday."""
    try:
        today = datetime.now()
        current_day_of_week = today.weekday()

        days_until_monday = (7 - current_day_of_week) % 7
        days_until_sunday = (6 - current_day_of_week) % 7

        next_monday = today + timedelta(days=days_until_monday)
        next_sunday = today + timedelta(days=days_until_sunday + 1)

        return int(next_monday.timestamp()), int(next_sunday.timestamp())
    except Exception as e:
        return int(datetime.now().timestamp()), int(datetime.now().timestamp())

def transform_message(day_and_nicks: List[Tuple[str, Set[str]]], threshold: int) -> str:
    """Transforms collected reactions into a formatted message."""
    try:
        message = ""
        for day, nicks in day_and_nicks:
            if day != 'wyniki':
                emoji = '🔴' if len(nicks) < threshold else '🟢'
                if nicks and None not in nicks:
                    line = f"{emoji} {day.capitalize()}: {', '.join(nicks)}\n"
                    message += line
        return message or "Brak dostępnych terminów :("
    except Exception as e:
        return "Wystąpił błąd podczas formatowania wiadomości."
