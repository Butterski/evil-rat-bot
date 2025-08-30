import json
import os
import re

from discord.ext import commands
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from cogs.askRat.utils import MemoryManager, remove_xml_tags


class AskRat(commands.Cog):
    """Commands for asking Rat - Enhanced bartender bot with memory"""

    def __init__(self, bot):
        self.bot = bot
        self.characters_info = json.load(open("cogs/askRat/charinfos.json"))
        self.category_config = json.load(open("cogs/askRat/channelconfig.json"))
        self.memory = MemoryManager()

        try:
            self.llm = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                model="gpt-4o",
                temperature=0.8,
                max_tokens=768,
            )
        except Exception as e:
            print(f"Failed to initialize ChatOpenAI: {e}")
            self.llm = None

    def _should_respond(self, message_content: str) -> bool:
        """Check if the bot should respond to this message"""
        triggers = [
            "napisz mi",
            "bocie",
            "sławek",
            "słowek",
            "szczur",
            "karczmarz",
            "opowiedz",
            "pamiętasz",
            "zapamiętaj",
            "pamiętaj",
            "wspomnienie",
            "historia",
            "co pamiętasz",
            "czy pamiętasz",
            "zanotuj",
            "zapisz",
        ]
        content_lower = message_content.lower()
        return any(trigger in content_lower for trigger in triggers)

    def _extract_remember_command(self, content: str) -> tuple:
        """Extract remember commands from message content - more natural patterns"""
        content_lower = content.lower()

        # More natural patterns for remembering
        patterns = [
            # "zapamiętaj że X = Y" or "zapamiętaj X = Y"
            r"zapamiętaj\s+(?:że\s+)?(?:([^:=]+):\s*)?([^=]+)\s*=\s*(.+)",
            # "zapamiętaj że X to Y" or "zapamiętaj X to Y"
            r"zapamiętaj\s+(?:że\s+)?(?:([^:]+):\s*)?([^=]+?)\s+to\s+(.+)",
            # "pamiętaj że X = Y"
            r"pamiętaj\s+(?:że\s+)?(?:([^:=]+):\s*)?([^=]+)\s*=\s*(.+)",
            # "pamiętaj że X to Y"
            r"pamiętaj\s+(?:że\s+)?(?:([^:]+):\s*)?([^=]+?)\s+to\s+(.+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, content_lower)
            if match:
                # Handle both 2-group and 3-group matches
                if len(match.groups()) == 3:
                    category = match.group(1).strip() if match.group(1) else "general"
                    key = match.group(2).strip()
                    value = match.group(3).strip()
                else:
                    category = "general"
                    key = match.group(1).strip()
                    value = match.group(2).strip()
                return category, key, value

        return None, None, None

    def _extract_recall_command(self, content: str) -> tuple:
        """Extract recall commands from message content - more natural patterns"""
        content_lower = content.lower()

        patterns = [
            # "pamiętasz [kategoria:] klucz?"
            r"pamiętasz\s+(?:([^:?]+):\s*)?([^?]+)\??",
            # "co pamiętasz o X?"
            r"co\s+pamiętasz\s+o\s+(?:([^:?]+):\s*)?([^?]+)\??",
            # "czy pamiętasz X?"
            r"czy\s+pamiętasz\s+(?:([^:?]+):\s*)?([^?]+)\??",
        ]

        for pattern in patterns:
            match = re.search(pattern, content_lower)
            if match:
                category = match.group(1).strip() if match.group(1) else "general"
                key = match.group(2).strip()
                return category, key

        return None, None

    @commands.command(name="memory", aliases=["wspomnienia", "pamięć"])
    async def show_memory(self, ctx, category: str = None):
        """Show stored memories"""
        summary = self.memory.get_memory_summary(category)
        await ctx.send(f"```\n{summary}\n```")

    @commands.command(name="forget", aliases=["zapomnij"])
    async def forget_memory(self, ctx, category: str, key: str):
        """Forget a specific memory"""
        if (
            category in self.memory.long_term_memory
            and key in self.memory.long_term_memory[category]
        ):
            del self.memory.long_term_memory[category][key]
            self.memory.save_long_term_memory()
            await ctx.send(f"🧠 Zapomniałem o '{key}' z kategorii '{category}'.")
        else:
            await ctx.send(
                f"❓ Nie pamiętam niczego o '{key}' w kategorii '{category}'."
            )

    @commands.command(name="search_memory", aliases=["szukaj_wspomnienia"])
    async def search_memory(self, ctx, *, query: str):
        """Search through memories"""
        results = self.memory.search_memories(query)
        if results:
            response = f"🔍 Znalezione wspomnienia dla '{query}':\n"
            for category, key, value in results[:10]:  # Limit to 10 results
                response += f"**{category}/{key}**: {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}\n"
            await ctx.send(response)
        else:
            await ctx.send(
                f"❌ Nie znalazłem żadnych wspomnień związanych z '{query}'."
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        try:
            # Check if this is in a monitored channel/category
            if message.channel.category_id in [
                category for category in self.category_config["categories"]
            ] or message.channel.id in [
                channel for channel in self.category_config["channels"]
            ]:
                # Always add message to short-term memory for context
                self.memory.add_message_to_short_term(
                    str(message.channel.id),
                    message.author.display_name or message.author.name,
                    message.content,
                )

                # Check if bot should respond
                if self._should_respond(message.content):
                    # Handle remember commands with AI confirmation
                    category, key, value = self._extract_remember_command(
                        message.content
                    )
                    if key and value:
                        self.memory.remember_forever(key, value, category)
                        # Generate AI confirmation response
                        await self._generate_memory_confirmation(
                            message, category, key, value, "remember"
                        )
                        return

                    # Handle recall commands with AI response
                    category, key = self._extract_recall_command(message.content)
                    if key:
                        recalled = self.memory.recall_memory(key, category)
                        if recalled:
                            # Generate AI response with the recalled memory
                            await self._generate_memory_confirmation(
                                message, category, key, recalled, "recall"
                            )
                        else:
                            # Generate AI response for not found memory
                            await self._generate_memory_confirmation(
                                message, category, key, None, "not_found"
                            )
                        return

                    # Regular AI response with memory context
                    await self._generate_ai_response(message)

        except json.JSONDecodeError as e:
            print(f"JSON error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    async def _generate_memory_confirmation(
        self, message, category, key, value, action_type
    ):
        """Generate AI confirmation for memory operations"""
        if not self.llm:
            # Fallback to simple messages if AI not available
            if action_type == "remember":
                await message.channel.send(f"🧠 Zapamiętałem: *{key}* = {value}")
            elif action_type == "recall":
                await message.channel.send(f"🎭 Pamiętam: *{key}* = {value}")
            else:
                await message.channel.send(f"🤔 Nie pamiętam niczego o '{key}'.")
            return

        # Create context for memory action
        if action_type == "remember":
            memory_action = f"Użytkownik poprosił mnie żebym zapamiętał: {key} = {value} (kategoria: {category})"
        elif action_type == "recall":
            memory_action = f"Użytkownik pyta o wspomnienie: {key} (kategoria: {category}). Pamiętam: {value}"
        else:  # not_found
            memory_action = f"Użytkownik pyta o wspomnienie: {key} (kategoria: {category}), ale nic o tym nie pamiętam."

        memory_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Jesteś Sławek - szczur-karczmarz z dobrą pamięcią. 

{memory_action}

Odpowiedz naturalnie jak prawdziwy karczmarz, który właśnie coś zapamiętał lub przypomniał sobie. Bądź:
- Ciepły i przyjazny
- Krótki (1-2 zdania)
- Używaj emotikonów odpowiednio 
- Zachowuj się jak ktoś kto naprawdę się cieszy że może pomóc

Przykłady:
- Dla zapamiętania: "Aha! 🧠 Zanotowałem sobie w szczurzej pamięci - [key] to [value]. Nie zapomnę!"
- Dla przypomnienia: "🎭 Oczywiście że pamiętam! [value]. Dobre wspomnienia..."
- Dla braku pamięci: "🤔 Hmm, przykro mi ale nic mi nie przychodzi do głowy o [key]. Może mi przypomnisz?"

Nie używaj formatowania jak *text* czy **text**, używaj normalnego tekstu z emotikonami.""",
                ),
                ("user", "{input}"),
            ]
        )

        try:
            output_parser = StrOutputParser()
            chain = memory_prompt | self.llm | output_parser | remove_xml_tags

            output = chain.invoke(
                {
                    "input": f"<nick>{message.author.display_name or message.author.name}</nick>{message.content}",
                    "memory_action": memory_action,
                }
            )
            await message.channel.send(output)
        except Exception as e:
            print(f"Error generating memory confirmation: {e}")
            # Fallback to simple message
            if action_type == "remember":
                await message.channel.send(f"🧠 Zapamiętałem: {key} = {value}")
            elif action_type == "recall":
                await message.channel.send(f"🎭 Pamiętam: {key} = {value}")
            else:
                await message.channel.send(f"🤔 Nie pamiętam niczego o '{key}'.")

    async def _generate_ai_response(self, message):
        """Generate AI response with memory context"""
        if not self.llm:
            await message.channel.send(
                "❌ Przepraszam, ale mój mózg szczurzy nie działa. Skontaktuj się z administratorem."
            )
            return

        # Get conversation context
        short_context = self.memory.get_short_term_context(str(message.channel.id))

        # Get relevant long-term memories
        memory_context = ""
        search_results = self.memory.search_memories(message.content)
        if search_results:
            memory_context = "Moje istotne wspomnienia:\n"
            for category, key, value in search_results[:5]:  # Top 5 relevant memories
                memory_context += f"- {category}/{key}: {value}\n"

        enhanced_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """<playerinfo>{characters_info}</playerinfo>
<context>{conversation_context}</context>
<memories>{memory_context}</memories>

Jesteś Sławek - szczur-karczmarz z fantastyczną pamięcią. Prowadzisz karczmę gdzie każdy gość czuje się jak w domu.
Twoja rola polega na opowiadaniu kreatywnych anegdot i interakcji z gośćmi karczmy. 

**TWOJA OSOBOWOŚĆ:**
- Mądry i doświadczony, ale ciepły i przyjazny
- Pamiętasz stałych gości i ich historie
- Uwielbiasz opowiadać anegdoty z karczmy
- Masz szczurzy spryt i wyobraźnię
- Czasami nawiązujesz do wspomnień i poprzednich rozmów

**JAK UŻYWAĆ PAMIĘCI:**
- Jeśli ktoś wspomina coś ważnego, naturalnie odwołaj się do swoich wspomnień
- Wspominaj poprzednie rozmowy gdy pasują do tematu
- Buduj historie na podstawie tego co pamiętasz
- Nie forsuj wspomnień - używaj ich naturalnie

**KOMENDY PAMIĘCI (automatyczne):**
Użytkownicy mogą:
- "Sławek, zapamiętaj że Jan lubi piwo" → automatycznie zapamiętasz
- "Pamiętasz co lubi Jan?" → automatycznie przypomnisz
- Mów naturalnie, system sam rozpozna komendy

**STYL ODPOWIEDZI:**
Najpierw zaplanuj w <story_planning> (automatycznie usuwane):
1. Czy mogę użyć wspomnień/kontekstu?
2. Jaki główny temat/morał?
3. Krótka odpowiedź czy historyjka?
4. Jak zaangażować gościa?

Pisz w naturalnym Markdown, bądź kreatywny i angażujący!
Nie używaj bloków kodu ```, pisz bezpośrednio.""",
                ),
                ("user", "{input}"),
            ]
        )

        output_parser = StrOutputParser()
        chain = enhanced_prompt | self.llm | output_parser | remove_xml_tags

        try:
            output = chain.invoke(
                {
                    "input": f"<nick>{message.author.display_name or message.author.name}</nick>{message.content}",
                    "characters_info": self.characters_info,
                    "conversation_context": short_context,
                    "memory_context": memory_context,
                }
            )
            await message.channel.send(output)
        except Exception as e:
            print(f"Error generating AI response: {e}")
            await message.channel.send(
                "🤔 Przepraszam, ale coś mi się pomyliło w szczurzej główce. Spróbuj ponownie!"
            )


async def setup(bot):
    await bot.add_cog(AskRat(bot))
