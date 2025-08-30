import json
import os
import re
from collections import deque
from datetime import datetime
from typing import Any, Dict, List, Optional


def remove_xml_tags(input_string):
    """
    Removes all content enclosed in XML tags, including the tags themselves, from the input string.

    Args:
        input_string (str): The input string containing XML tags and content.

    Returns:
        str: The string with XML tags and their contents removed.
    """
    try:
        pattern = r"<[^>]+>.*?</[^>]+>|<[^/>]+/>"
        return re.sub(pattern, "", input_string, flags=re.DOTALL).strip()
    except re.error as e:
        print(f"Regex error: {e}")
        return input_string
    except Exception as e:
        print(f"Unexpected error: {e}")
        return input_string


class MemoryManager:
    """Manages both short-term and long-term memory for the bartender bot"""

    def __init__(self, memory_file_path: str = "cogs/askRat/memory.json"):
        self.memory_file_path = memory_file_path
        self.short_term_memory: Dict[str, deque] = {}  # channel_id -> deque of messages
        self.long_term_memory: Dict[str, Any] = {}  # persistent memory
        self.max_short_term = 10
        self.load_long_term_memory()

    def load_long_term_memory(self):
        """Load long-term memory from file"""
        try:
            if os.path.exists(self.memory_file_path):
                with open(self.memory_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.long_term_memory = data.get("long_term", {})
        except Exception as e:
            print(f"Error loading long-term memory: {e}")
            self.long_term_memory = {}

    def save_long_term_memory(self):
        """Save long-term memory to file"""
        try:
            os.makedirs(os.path.dirname(self.memory_file_path), exist_ok=True)
            data = {
                "long_term": self.long_term_memory,
                "last_updated": datetime.now().isoformat(),
            }
            with open(self.memory_file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving long-term memory: {e}")

    def add_message_to_short_term(self, channel_id: str, author: str, content: str):
        """Add a message to short-term memory"""
        if channel_id not in self.short_term_memory:
            self.short_term_memory[channel_id] = deque(maxlen=self.max_short_term)

        message_data = {
            "author": author,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        }
        self.short_term_memory[channel_id].append(message_data)

    def get_short_term_context(self, channel_id: str) -> str:
        """Get formatted short-term context for the channel"""
        if channel_id not in self.short_term_memory:
            return "Brak ostatnich rozmów w pamięci."

        messages = list(self.short_term_memory[channel_id])
        if not messages:
            return "Brak ostatnich rozmów w pamięci."

        context = "Ostatnie rozmowy w tej karczmie:\n"
        for msg in messages[-10:]:  # Last 10 messages
            context += f"- {msg['author']}: {msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}\n"

        return context

    def remember_forever(self, key: str, value: Any, category: str = "general"):
        """Store something in long-term memory"""
        if category not in self.long_term_memory:
            self.long_term_memory[category] = {}

        self.long_term_memory[category][key] = {
            "value": value,
            "stored_at": datetime.now().isoformat(),
        }
        self.save_long_term_memory()

    def recall_memory(self, key: str, category: str = "general") -> Optional[Any]:
        """Recall something from long-term memory"""
        if category in self.long_term_memory and key in self.long_term_memory[category]:
            return self.long_term_memory[category][key]["value"]
        return None

    def get_memory_summary(self, category: str = None) -> str:
        """Get a summary of stored memories"""
        if not self.long_term_memory:
            return "Nie mam żadnych długotrwałych wspomnień."

        if category and category in self.long_term_memory:
            memories = self.long_term_memory[category]
            summary = f"Wspomnienia z kategorii '{category}':\n"
        else:
            summary = "Wszystkie moje wspomnienia:\n"
            memories = {}
            for cat, mem_dict in self.long_term_memory.items():
                memories.update({f"{cat}/{k}": v for k, v in mem_dict.items()})

        for key, data in list(memories.items())[:20]:  # Limit to 20 items
            summary += f"- {key}: {str(data['value'])[:100]}{'...' if len(str(data['value'])) > 100 else ''}\n"

        return summary

    def search_memories(self, query: str) -> List[tuple]:
        """Search through long-term memories"""
        results = []
        query_lower = query.lower()

        for category, memories in self.long_term_memory.items():
            for key, data in memories.items():
                value_str = str(data["value"]).lower()
                if query_lower in key.lower() or query_lower in value_str:
                    results.append((category, key, data["value"]))

        return results
