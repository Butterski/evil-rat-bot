from datetime import datetime, timedelta


def get_next_week_mondays_and_sundays():
    today = datetime.now()
    current_day_of_week = today.weekday()

    days_until_monday = (7 - current_day_of_week) % 7
    days_until_sunday = (6 - current_day_of_week) % 7

    next_monday = today + timedelta(days=days_until_monday)
    next_sunday = today + timedelta(days=days_until_sunday + 1)

    monday_timestamp = int(next_monday.timestamp())
    sunday_timestamp = int(next_sunday.timestamp())

    return monday_timestamp, sunday_timestamp

def transform_message(day_and_nicks, threshold):
    message = ""
    for day, nicks in day_and_nicks:
        if day != 'wyniki':
            emoji = '🔴'
            if len(nicks) >= threshold:
                emoji = '🟢'
            if nicks != {None}:
                line = f"{emoji} {day.capitalize()}: {', '.join(nicks)}\n"
                message += line
    return message
