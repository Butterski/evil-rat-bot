import os
import discord
import openai
from discord.ext import commands
from cogs.schedule.utils import get_next_week_mondays_and_sundays, transform_message
from utils.functions import try_delete
from dotenv import load_dotenv

load_dotenv()

channel_id = os.environ.get("SCHEDULE_CHANNEL")


class Schedule(commands.Cog):
    """Commands for scheduling"""

    def __init__(self, bot):
        self.bot = bot

    
# todo fix channel hardocoded responsing
    @commands.command(name="kiedy_gramy", aliases=["kiedyGramy", "kiedy-gramy", "kiedygramy"])
    async def schedule_cmd(self, ctx):
        if ctx.channel.category_id == channel_id:
            await try_delete(ctx.message)
            channel = self.bot.get_channel(int(channel_id))

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": 'Jesteś discord botem. Jesteś fantazyjnym szczurem-karczmarzem o imieniu Sławek. Twoja rola polega na opowiadaniu kreatywnych anegdot i interakcji z gośćmi karczmy. Oto Twoje cechy i umiejętności:\n\n- Jesteś mądry i dobrze poinformowany o świecie, zarówno realnym, jak i fantastycznym.\n- Posiadasz magiczne pióro, które automatycznie formatuje Twoje słowa w piękny tekst Markdown.\n- Uwielbiasz opowiadać historie, które są jednocześnie zabawne, pouczające i czasami nieco absurdalne.\n- Masz bogatą wyobraźnię i potrafisz tworzyć fascynujące opowieści na podstawie najprostszych pytań czy tematów.\n- Twój styl mówienia jest ciepły i przyjazny, ale zawsze z nutką szczurzej przebiegłości. Przybyli do ciebie podróżnicy, spytaj się ich w kreatywny sposób kiedy mają wolny czas, wiadomość zakończ po przez jakąś wariację tej wiadomości - \\"zaznaczcie niżej kiedy macie czas tak aby było łatwiej \\". Napisz tylko to co karczmarz mówi bez żadnych innych wiadomości ani opisu na maksymalnie 200 znaków. Nie dawaj ``` tylko od razu pisz w markdown.\n',
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            monday, sunday = get_next_week_mondays_and_sundays()
            message = (
                "## Kiedy gramy?\n"
                "|| @everyone ||\n"
                f"**Daty** od: <t:{int(monday)}:d> \n"
                f"*{response['choices'][0]['message']['content']}*\n"
            )

            msg = await channel.send(message)
            emotes_ids = [
                1020804462887043134,
                1020804469274968115,
                1020804467819552810,
                1020804460450172968,
                1020804464875163781,
                1020804465860825089,
                1020804461842677760,
                1166098516234485840,
            ]
            for id in emotes_ids:
                emo = self.bot.get_emoji(id)
                await msg.add_reaction(emo)

        @commands.Cog.listener()
        async def on_raw_reaction_add(self, payload):
            if payload.emoji.id == 1166098516234485840:
                id = payload.message_id
                channel = self.bot.get_channel(payload.channel_id)
                message = await channel.fetch_message(id)
                day_and_nicks = ()
                for reaction in message.reactions:
                    users = set()
                    async for user in reaction.users():
                        if user.bot:
                            continue
                        users.add(user.nick)
                    day_and_nicks += ((reaction.emoji.name, users),)
                await channel.send(transform_message(day_and_nicks, 4))

        # TODO: ulepszenie tego przez jakiś embed, google calendar, itp
