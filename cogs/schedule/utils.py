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

def get_week_range(monday_timestamp: int, sunday_timestamp: int) -> str:
    """Get formatted week range string."""
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
    total_participants: Set[str] = None
) -> str:
    """Transforms collected reactions into an enhanced formatted message."""
    try:
        if not day_and_nicks:
            return "❌ Brak dostępnych terminów."
        
        # Enhanced day mapping with emojis
        day_mapping = {
            "poniedzialek": ("🌙", "Poniedziałek"),
            "wtorek": ("🔥", "Wtorek"),
            "sroda": ("⚡", "Środa"),
            "czwartek": ("🌟", "Czwartek"),
            "piatek": ("🎉", "Piątek"),
            "sobota": ("🌅", "Sobota"),
            "niedziela": ("☀️", "Niedziela"),
        }
        
        results = []
        available_days = []
        
        header = f"## 📊 Wyniki głosowania\n"
        header += f"**🎯 Próg**: {threshold} graczy\n\n"
        
        for day, nicks in day_and_nicks:
            day_lower = day.lower()
            
            # Skip results emoji
            if day_lower == 'wyniki' or day == 'wyniki':
                continue
            
            # Get day info
            if day_lower in day_mapping:
                emoji, display_name = day_mapping[day_lower]
            else:
                # Fallback for unknown days
                emoji = "�"
                display_name = day.capitalize()
            
            # Filter out None values and empty strings
            valid_nicks = {nick for nick in nicks if nick and nick.strip()}
            
            if valid_nicks:
                # Determine status
                player_count = len(valid_nicks)
                status_emoji = '🟢' if player_count >= threshold else '�'
                
                # Format player list
                players_str = ', '.join(sorted(valid_nicks))
                
                # Create day result
                day_result = f"{status_emoji} {emoji} **{display_name}** ({player_count}): {players_str}"
                results.append(day_result)
                
                if player_count >= threshold:
                    available_days.append(display_name)
        
        if not results:
            return header + "❌ Brak głosów na żaden dzień."
        
        # Assemble final message
        message = header + "\n".join(results)
        
        # Add summary
        if available_days:
            message += f"\n\n✅ **Dostępne terminy**: {', '.join(available_days)}"
        else:
            message += f"\n\n❌ **Brak terminów** z wystarczającą liczbą graczy (min. {threshold})"
        
        # Add participant count if available
        if total_participants:
            unique_count = len(total_participants)
            message += f"\n👥 **Łącznie głosujących**: {unique_count}"
        
        # Add timestamp
        now = datetime.now().strftime("%d.%m.%Y %H:%M")
        message += f"\n🕐 *Ostatnia aktualizacja: {now}*"
        
        return message
        
    except Exception as e:
        print(f"Error in transform_message: {e}")
        return f"❌ Wystąpił błąd podczas formatowania wyników: {str(e)}"

def get_day_name_from_emoji(emoji_name: str) -> str:
    """Convert emoji name to readable day name."""
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

def calculate_best_days(day_and_nicks: List[Tuple[str, Set[str]]], threshold: int) -> List[str]:
    """Calculate which days meet the threshold requirement."""
    best_days = []
    
    for day, nicks in day_and_nicks:
        if day.lower() != 'wyniki':
            valid_nicks = {nick for nick in nicks if nick and nick.strip()}
            if len(valid_nicks) >= threshold:
                best_days.append(get_day_name_from_emoji(day))
    
    return best_days
