from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple, Union

import discord


def get_next_week_mondays_and_sundays() -> Tuple[int, int]:
    try:
        today = datetime.now()
        current_day_of_week = today.weekday()

        days_until_monday = (7 - current_day_of_week) % 7

        next_monday = today + timedelta(days=days_until_monday)
        next_sunday = next_monday + timedelta(days=6)

        return int(next_monday.timestamp()), int(next_sunday.timestamp())
    except Exception as e:
        return int(datetime.now().timestamp()), int(datetime.now().timestamp())


def get_week_range(monday_timestamp: int, sunday_timestamp: int) -> str:
    try:
        monday_date = datetime.fromtimestamp(monday_timestamp)
        sunday_date = datetime.fromtimestamp(sunday_timestamp)

        monday_str = monday_date.strftime("%d.%m")
        sunday_str = sunday_date.strftime("%d.%m.%Y")

        return f"{monday_str} - {sunday_str}"
    except Exception:
        return "Nieznany zakres dat"


def transform_message(
    day_and_nicks: List[Tuple[str, Set[str]]],
    threshold: int,
    total_participants: Set[str] = None,
) -> discord.Embed:
    embed = discord.Embed(
        title="📊 Wyniki głosowania",
        color=0x2B2D31,
        description=f"**🎯 Próg do gry:** `{threshold}` graczy",
    )

    try:
        if not day_and_nicks:
            embed.description += "\n\n❌ Brak głosów."
            embed.color = 0xED4245
            return embed

        day_mapping = {
            "poniedzialek": ("🌙", "Poniedziałek"),
            "poniedziałek": ("🌙", "Poniedziałek"),
            "wtorek": ("🔥", "Wtorek"),
            "sroda": ("⚡", "Środa"),
            "środa": ("⚡", "Środa"),
            "czwartek": ("🌟", "Czwartek"),
            "piatek": ("🎉", "Piątek"),
            "piątek": ("🎉", "Piątek"),
            "sobota": ("🌅", "Sobota"),
            "niedziela": ("☀️", "Niedziela"),
        }

        available_days = []
        has_any_votes = False

        for day, nicks in day_and_nicks:
            day_lower = day.lower()

            if day_lower in ["wyniki", "bar_chart"]:
                continue

            if day_lower in day_mapping:
                emoji, display_name = day_mapping[day_lower]
            else:
                emoji = "📅"
                display_name = day.capitalize()

            valid_nicks = {nick for nick in nicks if nick and nick.strip()}

            if valid_nicks:
                has_any_votes = True
                player_count = len(valid_nicks)
                is_meeting = player_count >= threshold

                status_emoji = "🟢" if is_meeting else "🔴"
                players_list = "\n".join([f"• {nick}" for nick in sorted(valid_nicks)])
                if not players_list:
                    players_list = "Brak"

                embed.add_field(
                    name=f"{status_emoji} {emoji} {display_name} ({player_count}/{threshold})",
                    value=f">>> {players_list}",
                    inline=True,
                )

                if is_meeting:
                    available_days.append(f"{emoji} **{display_name}**")

        if not has_any_votes:
            embed.description += "\n\n❌ Brak głosów na konkretne dni."
            embed.color = 0xED4245
            return embed

        summary_text = ""
        if available_days:
            summary_text += f"✅ **Gramy w:** {', '.join(available_days)}\n"
            embed.color = 0x57F287
        else:
            summary_text += f"❌ **Brak dni** spełniających próg ({threshold})\n"
            embed.color = 0xFEE75C

        if total_participants:
            summary_text += f"👥 **Zgłoszeń:** `{len(total_participants)}`"

        if summary_text:
            embed.add_field(name="📋 Podsumowanie", value=summary_text, inline=False)

        now = datetime.now().strftime("%d.%m.%Y %H:%M")
        embed.set_footer(text=f"🕐 Ostatnia aktualizacja: {now}")

        return embed

    except Exception as e:
        print(f"Error in transform_message: {e}")
        return discord.Embed(
            title="❌ Błąd",
            description=f"Wystąpił błąd podczas formatowania wyników:\n`{str(e)}`",
            color=0xED4245,
        )


def get_day_name_from_emoji(emoji_name: str) -> str:
    mapping = {
        "poniedzialek": "Poniedziałek",
        "wtorek": "Wtorek",
        "sroda": "Środa",
        "czwartek": "Czwartek",
        "piatek": "Piątek",
        "sobota": "Sobota",
        "niedziela": "Niedziela",
    }
    return mapping.get(emoji_name.lower(), emoji_name.capitalize())


def calculate_best_days(
    day_and_nicks: List[Tuple[str, Set[str]]], threshold: int
) -> List[str]:
    best_days = []
    for day, nicks in day_and_nicks:
        if day.lower() != "wyniki":
            valid_nicks = {nick for nick in nicks if nick and nick.strip()}
            if len(valid_nicks) >= threshold:
                best_days.append(get_day_name_from_emoji(day))
    return best_days
