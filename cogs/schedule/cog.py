import json
import os
from datetime import datetime
from typing import Dict, List, Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from cogs.schedule.utils import (
    get_day_name_from_emoji,
    get_next_week_mondays_and_sundays,
    get_week_range,
    transform_message,
)
from utils.functions import try_delete


class Schedule(commands.Cog):
    """Modern scheduling system with day-of-week emojis"""

    def __init__(self, bot):
        self.bot = bot
        self.schedule_message_id = None
        self.current_schedule_data = {}

        # Day emojis mapping (customizable)
        self.day_emojis = {
            "poniedziałek": "🌙",  # Monday - Moon
            "wtorek": "🔥",  # Tuesday - Fire
            "środa": "⚡",  # Wednesday - Lightning
            "czwartek": "🌟",  # Thursday - Star
            "piątek": "🎉",  # Friday - Party
            "sobota": "🌅",  # Saturday - Sunrise
            "niedziela": "☀️",  # Sunday - Sun
            "wyniki": "📊",  # Results
        }

        try:
            self.llm = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.8,
                openai_api_base="https://api.deepseek.com",
                model="deepseek-chat",
                max_tokens=256,
            )
            self.channel_id = os.getenv("SCHEDULE_CHANNEL")
            self.threshold = int(
                os.getenv("SCHEDULE_THRESHOLD", "4")
            )  # Minimum players needed
        except Exception as e:
            print(f"Failed to initialize Schedule cog: {e}")
            self.llm = None
            self.threshold = 4

    def _get_day_emoji_ids(self) -> List[int]:
        """Get custom emoji IDs for days of the week"""
        # Your existing custom emoji IDs
        return [
            1020804462887043134,  # Monday
            1020804469274968115,  # Tuesday
            1020804467819552810,  # Wednesday
            1020804460450172968,  # Thursday
            1020804464875163781,  # Friday
            1020804465860825089,  # Saturday
            1020804461842677760,  # Sunday
            1166098516234485840,  # Results
        ]

    async def _generate_schedule_intro(self) -> str:
        """Generate AI intro message for schedule"""
        if not self.llm:
            return "🎲 **Czas zaplanować nasze przygody!** Zaznaczcie poniżej kiedy macie czas!"

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Jesteś Sławek - szczur-karczmarz planujący sesje RPG dla swoich gości.

Napisz krótką, kreatywną wiadomość (max 150 znaków) zachęcającą do głosowania na terminy gier.
- Bądź entuzjastyczny i przyjazny
- Użyj tematyki karczmianej/przygodowej
- Zakończ zachętą do zaznaczania terminów
- Nie używaj ``` bloków kodu
- Pisz w naturalnym stylu Markdown""",
                ),
                ("user", "Napisz zachętę do głosowania na terminy sesji RPG"),
            ]
        )

        try:
            output_parser = StrOutputParser()
            chain = prompt | self.llm | output_parser
            return chain.invoke({})
        except Exception as e:
            print(f"Error generating intro: {e}")
            return "🎲 **Nowe przygody czekają!** Zaznaczcie kiedy macie czas na epickie sesje!"

    @commands.command(
        name="kiedy_gramy",
        aliases=["kiedyGramy", "kiedy-gramy", "kiedygramy", "schedule", "harmonogram"],
    )
    async def schedule_cmd(self, ctx):
        """Create a new schedule poll for the week"""
        try:
            if ctx.channel.id != int(self.channel_id):
                return

            await try_delete(ctx.message)
            channel = self.bot.get_channel(int(self.channel_id))

            # Reset schedule message ID for new schedule
            self.schedule_message_id = None

            # Generate intro message
            intro_text = await self._generate_schedule_intro()

            # Get week dates
            monday, sunday = get_next_week_mondays_and_sundays()
            week_range = get_week_range(monday, sunday)

            # Create enhanced embed message
            poll_embed = discord.Embed(
                title="🗓️ Kiedy gramy?",
                description=f"*{intro_text}*",
                color=0xEB459E,  # A nice vibrant color
                timestamp=datetime.now(),
            )
            poll_embed.add_field(
                name="📅 Tydzień", value=f"`{week_range}`", inline=True
            )
            poll_embed.add_field(
                name="🎯 Próg", value=f"`{self.threshold}` graczy", inline=True
            )
            poll_embed.set_footer(text="Reaguj na dni kiedy możesz grać poniżej!")

            msg = await channel.send(content="|| @everyone ||", embed=poll_embed)

            # Add day reactions with custom emojis
            emoji_ids = self._get_day_emoji_ids()
            added_reactions = 0

            for emoji_id in emoji_ids:
                try:
                    emoji = self.bot.get_emoji(emoji_id)
                    if emoji:
                        await msg.add_reaction(emoji)
                        added_reactions += 1
                except Exception as e:
                    print(f"Failed to add reaction {emoji_id}: {e}")
                    continue

            if added_reactions == 0:
                # Fallback to standard emojis if custom ones fail
                fallback_emojis = ["🌙", "🔥", "⚡", "🌟", "🎉", "🌅", "☀️", "📊"]
                for emoji in fallback_emojis:
                    try:
                        await msg.add_reaction(emoji)
                    except Exception as e:
                        print(f"Failed to add fallback reaction {emoji}: {e}")
                        continue

            # Store message data
            self.current_schedule_data = {
                "message_id": msg.id,
                "created_at": datetime.now().isoformat(),
                "week_start": monday,
                "week_end": sunday,
                "threshold": self.threshold,
            }

            await channel.send(
                f"✅ Ankieta utworzona! Minimum **{self.threshold}** graczy potrzebnych do zielonych dat."
            )

        except Exception as e:
            if ctx.channel:
                await ctx.channel.send(f"❌ Wystąpił błąd: {str(e)}")
            print(f"Error in schedule_cmd: {e}")

    @commands.command(name="schedule_info", aliases=["info_harmonogram"])
    async def schedule_info(self, ctx):
        """Show current schedule information"""
        try:
            if ctx.channel.id != int(self.channel_id):
                return

            if not self.current_schedule_data:
                await ctx.send("ℹ️ Brak aktywnej ankiety harmonogramu.")
                return

            data = self.current_schedule_data
            created_date = datetime.fromisoformat(data["created_at"]).strftime(
                "%d.%m.%Y %H:%M"
            )

            embed = discord.Embed(
                title="📊 Informacje o harmonogramie",
                color=0x3498DB,
                timestamp=datetime.now(),
            )
            embed.add_field(name="📅 Data utworzenia", value=created_date, inline=True)
            embed.add_field(
                name="🎯 Próg graczy", value=str(data["threshold"]), inline=True
            )
            embed.add_field(
                name="🆔 ID wiadomości", value=str(data["message_id"]), inline=True
            )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Błąd podczas pobierania informacji: {str(e)}")

    @commands.command(name="schedule_threshold", aliases=["prog_harmonogram"])
    async def set_threshold(self, ctx, new_threshold: int):
        """Set the minimum number of players needed"""
        try:
            if ctx.channel.id != int(self.channel_id):
                return

            if new_threshold < 1 or new_threshold > 20:
                await ctx.send("❌ Próg musi być między 1 a 20.")
                return

            self.threshold = new_threshold
            if self.current_schedule_data:
                self.current_schedule_data["threshold"] = new_threshold

            await ctx.send(f"✅ Próg ustawiony na **{new_threshold}** graczy.")

        except ValueError:
            await ctx.send("❌ Podaj prawidłową liczbę.")
        except Exception as e:
            await ctx.send(f"❌ Błąd: {str(e)}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload, is_add=True):
        """Handle reactions to schedule messages"""
        try:
            # Ignore bot reactions
            if payload.user_id == 824970912382189571:
                return

            channel = self.bot.get_channel(payload.channel_id)
            if not channel:
                return

            # Check if this is the correct channel
            if channel.id != int(self.channel_id):
                return

            message = await channel.fetch_message(payload.message_id)
            if not message:
                return

            # Check if this is a schedule message (has the right reactions)
            emoji_ids = self._get_day_emoji_ids()
            has_schedule_reactions = any(
                reaction.emoji.id in emoji_ids
                for reaction in message.reactions
                if hasattr(reaction.emoji, "id")
            )

            # Only process if this message has schedule reactions or if reaction is results emoji
            if not has_schedule_reactions and payload.emoji.id != 1166098516234485840:
                return

            # Additional check: only process if this is the current schedule message or has all day reactions
            if (
                self.current_schedule_data
                and message.id != self.current_schedule_data.get("message_id")
                and not has_schedule_reactions
            ):
                return

            # Collect all reaction data
            day_and_nicks = []
            total_participants = set()
            newly_reached_5 = None

            for reaction in message.reactions:
                try:
                    users = set()
                    async for user in reaction.users():
                        if user.bot:
                            continue
                        display_name = user.display_name or user.name
                        users.add(display_name)
                        total_participants.add(display_name)

                    if users:  # Only add if there are users
                        day_and_nicks.append((reaction.emoji.name, users))

                    # If this is the reaction just added, and it exactly reached 5 people
                    if (
                        is_add
                        and len(users) == 5
                        and payload.emoji.name == reaction.emoji.name
                    ):
                        newly_reached_5 = reaction.emoji.name

                except Exception as e:
                    print(f"Failed to process reaction {reaction}: {e}")
                    continue

            if newly_reached_5:
                # E.g., translates "poniedziałek" to "Poniedziałek" or whatever the standard is
                day_name = get_day_name_from_emoji(newly_reached_5)
                await channel.send(f"🎉 **Zdobyliśmy 5 osób na dzień: {day_name}!** 🎲")

            if day_and_nicks:
                try:
                    # Generate enhanced results message
                    transformed_message = transform_message(
                        day_and_nicks,
                        self.threshold,
                        total_participants=total_participants,
                    )

                    # Update or create results message
                    if self.schedule_message_id:
                        try:
                            schedule_message = await channel.fetch_message(
                                self.schedule_message_id
                            )
                            await schedule_message.edit(
                                content=None, embed=transformed_message
                            )
                        except discord.NotFound:
                            # Message was deleted, create new one
                            schedule_message = await channel.send(
                                embed=transformed_message
                            )
                            self.schedule_message_id = schedule_message.id
                    else:
                        schedule_message = await channel.send(embed=transformed_message)
                        self.schedule_message_id = schedule_message.id

                except Exception as e:
                    await channel.send(
                        f"❌ Błąd podczas aktualizacji wyników: {str(e)}"
                    )

        except Exception as e:
            print(f"Error in reaction handler: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Handle reaction removal (trigger update)"""
        # Reuse the same logic as reaction_add for updates
        await self.on_raw_reaction_add(payload, is_add=False)


async def setup(bot):
    await bot.add_cog(Schedule(bot))
